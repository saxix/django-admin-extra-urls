
develop:
	pip install -U pip setuptools
	pip install -e .[dev]

clean:
	# cleaning
	@rm -fr dist '~build'
	@find . -name __pycache__ -o -name .eggs | xargs rm -rf
	@find . -name "*.py?" -o -name ".DS_Store" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf

fullclean:
	@rm -rf .tox .cache
	$(MAKE) clean
