test:
	nosetests -d

medium-test:
	nosetests -a '!large' -d

small-test:
	nosetests -A 'not (medium or large)' -d
