export PYTHONPATH := ${CURDIR}

.PHONY: setup
setup:
	echo ${PYTHONPATH}

.PHONY: yael
yael:
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cd yael; ./configure.sh
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
