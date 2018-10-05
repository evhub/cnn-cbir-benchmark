SHELL := /bin/bash
export PYTHONPATH := ${CURDIR}/yael

.PHONY: setup
setup:
	source activate py2
	echo ${PYTHONPATH}

.PHONY: yael
yael: setup
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cd yael; ./configure.sh --enable-numpy
	cd yael; make

.PHONY: clean
clean:
	rm -rf ./yael
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv: setup
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py
