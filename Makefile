SHELL := /bin/bash
export PYTHONPATH := ${CURDIR}/yael

.PHONY: setup
setup:
	mkdir ./opencv_models
	echo "You need to run:"
	echo "export PYTHONPATH=\"${PYTHONPATH}\""

.PHONY: yael
yael:
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cp ./makefile.inc ./yael/makefile.inc
	cd yael; make

.PHONY: gcc
gcc:
	sudo update-alternatives --config gcc

.PHONY: clean
clean:
	rm -rf ./yael
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv:
	python2 ./fv_retrieval/src/gmm.py
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py
