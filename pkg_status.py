import re
from typing import List, Optional

from _collections import defaultdict
from fastapi import FastAPI, HTTPException

from model_with_properties import PropertyBaseModel

app = FastAPI(
    title="PKG Status", description="A code for an interview.", version="11.0.0"
)


class Dependency(PropertyBaseModel):
    name: str

    @property
    def url(self, *args, **kwargs):
        return get_package_url(self.name)


class Package(PropertyBaseModel):
    name: str
    description: str
    deps: Optional[List[Dependency]]
    altdeps: Optional[List[List[Dependency]]]
    revdeps: Optional[List[Dependency]]


packages = {}


class Error404(HTTPException):
    def __init__(self, detail):
        super().__init__(status_code=404, detail=detail)


@app.get("/")
async def list_of_all_packages():
    result = []
    for pkg_name in sorted(list(packages)):
        url = get_package_url(pkg_name)
        result.append({"name": pkg_name, "url": url})
    return result


@app.get("/{pkg_name}")
async def view_package_details(pkg_name):
    if pkg_name not in packages:
        raise Error404("package not found")

    package = packages[pkg_name]
    return package


def parse_status_file(path="/var/lib/dpkg/status"):
    with open(path, "rt") as f:
        content = f.read()

    # parse description and dependencies
    packages = {}
    for raw_pkg in content.split("\n\n"):
        if raw_pkg == "":
            break
        package = parse_package(raw_pkg)
        packages[package.name] = package

    # reverse dependencies
    for pkg_name, package in packages.items():
        for dependency in iterate_all_dependencies(package):
            dependency_package = packages.get(dependency.name)
            if dependency_package is None:  # package not installed
                continue
            reverse_dependency = Dependency(name=pkg_name)
            dependency_package.revdeps.append(reverse_dependency)

    return packages


def parse_package(raw_pkg):
    fields = {"Package", "Description", "Depends"}

    d = defaultdict(str)
    for line in raw_pkg.splitlines():
        if line.startswith(" "):
            continue
        key, value = line.split(":", maxsplit=1)
        if key in fields:
            d[key] = value.strip()

    fixed_deps, alternative_deps = parse_dependencies(d["Depends"])
    package = Package(
        name=d["Package"],
        description=d["Description"],
        deps=fixed_deps,
        altdeps=alternative_deps,
        revdeps=set(),  # populated elsewhere
    )

    return package


def iterate_all_dependencies(package):
    for dependency in package.deps:
        yield dependency
    for alternative_dependencies in package.altdeps:
        for dependency in alternative_dependencies:
            yield dependency


def parse_dependencies(raw_deps):
    fixed_deps = set()
    alternative_deps = set()

    if raw_deps == "":
        return fixed_deps, alternative_deps

    for raw_dep in raw_deps.split(", "):
        if raw_dep.find("|") != -1:
            alternatives = []
            for raw_dep in raw_dep.split(" | "):
                raw_dep = _remove_version_info(raw_dep)
                dependency = Dependency(name=raw_dep)
                alternatives.append(dependency)
            alternative_deps.add(tuple(alternatives))
        else:
            raw_dep = _remove_version_info(raw_dep)
            dependency = Dependency(name=raw_dep)
            fixed_deps.add(dependency)
    return fixed_deps, alternative_deps


def _remove_version_info(dep):
    return re.sub(r"\s\(.+\)", "", dep)


def get_package_url(pkg_name):
    if pkg_name not in packages:
        return None
    url = app.url_path_for("view_package_details", pkg_name=pkg_name)
    return url


packages = parse_status_file(path="dpkg_status_example")
