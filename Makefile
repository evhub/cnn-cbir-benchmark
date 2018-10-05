SHELL := /bin/bash
export PYTHONPATH := ${CURDIR}/yael

.PHONY: setup
setup:
	echo ${PYTHONPATH}

.PHONY: yael
yael:
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cd yael; source activate py2; ./configure.sh --enable-numpy; source deactivate
	cd yael; make

.PHONY: clean
clean:
	rm -rf ./yael
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv:
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py
