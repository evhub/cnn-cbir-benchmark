.PHONY: install
install:
	python2 -m pip install scikit-learn

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv:
	python2 fv.py
	python2 brute.py
