.PHONY: reqs
reqs:
	sort-requirements requirements/*.in
	ls ./requirements/*.in | xargs -L1 pip-compile
	ls ./requirements/*.txt | xargs -L1 pip install -r

.PHONY: status
status:
	docker run --rm ubuntu cat /var/lib/dpkg/status > dpkg_status_example

.PHONY: format
format:
	isort *.py && black *.py && flake8 *.py

.PHONY: run
run:
	uvicorn pkg_status:app --workers 1 --reload
