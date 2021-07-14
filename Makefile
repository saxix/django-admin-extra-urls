
develop:
	python3 -m venv .venv
	.venv/bin/pip install -U pip setuptools
	.venv/bin/pip install -e .[dev]

clean:
	# cleaning
	@rm -fr dist '~build' .pytest_cache .coverage src/admin_extra_urls.egg-info
	@find . -name __pycache__ -o -name .eggs | xargs rm -rf
	@find . -name "*.py?" -o -name ".DS_Store" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf

fullclean:
	@rm -rf .tox .cache
	$(MAKE) clean

docs:
	rm -fr ~build/docs/
	sphinx-build -n docs/ ~build/docs/

lint:
	@flake8 src/
	@isort src/

release:
	tox
	rm -fr dist/
	./setup.py sdist
	#PACKAGE_NAME=django-admin-extra-buttons ./setup.py sdist
	twine upload dist/


.PHONY: build docs


