import textwrap

import pytest
from fastapi.testclient import TestClient

from pkg_status import Dependency, Package, app, parse_dependencies, parse_package


def test_get_package_details(client):
    ...


def test_parse_pkg_descr():
    raw_description = textwrap.dedent(
        """\
        Package: adduser
        Maintainer: Ubuntu Core Developers <ubuntu-devel-discuss@lists.ubuntu.com>
        Depends: passwd, debconf (>= 0.5) | debconf-2.0
        Conffiles:
         /etc/deluser.conf 773fb95e98a27947de4a95abb3d3f2a2
        Description: add and remove users and groups
         This package includes the 'adduser' and 'deluser' commands for creating
         and removing users.
         [cut]
        Original-Maintainer: Debian Adduser Developers <adduser@packages.debian.org>
    """
    )
    result = parse_package(raw_description)
    assert result == Package(
        name="adduser",
        description="add and remove users and groups",
        deps=[Dependency(name="passwd")],
        altdeps=[[Dependency(name="debconf"), Dependency(name="debconf-2.0")]],
        revdeps=[],
    )


def test_parse_deps():
    # TODO: moar use cases
    fixed_deps, alternative_deps = parse_dependencies(
        "passwd, debconf (>= 0.5) | debconf-2.0"
    )
    assert fixed_deps == {Dependency(name="passwd")}
    assert alternative_deps == {
        (Dependency(name="debconf"), Dependency(name="debconf-2.0"))
    }


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
