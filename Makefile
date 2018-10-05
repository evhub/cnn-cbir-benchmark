SHELL := /bin/bash
export PYTHONPATH := /home/mirlab/miniconda3/envs/py2/lib/python2.7/site-packages;${CURDIR}/yael

.PHONY: setup
setup:
	source activate py2
	echo "You need to run:"
	echo "export PYTHONPATH=\"${PYTHONPATH}\""

.PHONY: yael
yael: setup
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cd yael; ./configure.sh --enable-numpy --numpy-cflags "/home/mirlab/miniconda3/envs/py2/lib/python2.7/site-packages/numpy/core/include/"
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
fv: setup
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py
