clean:
	# cleaning
	@find . -name __pycache__ -o -name .eggs | xargs rm -rf
	@find . -name "*.py?" -o -name ".DS_Store" -o -name "*.orig" -o -name "*.min.min.js" -o -name "*.min.min.css" -prune | xargs rm -rf
	@rm -f coverage.xml flake.out pep8.out pytest.xml

fullclean:
	@rm -rf .tox .cache dist build '~build'
	$(MAKE) clean
