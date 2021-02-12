
develop:
	pip install -U pip setuptools
	pip install -e .[dev]

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


.PHONY: build docs


