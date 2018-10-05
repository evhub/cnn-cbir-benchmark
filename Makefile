.PHONY: activate
activate:
	export PYTHONPATH = "~/yael"
	source activate py2

.PHONY: yael
yael:
	cd ~
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cd yael
	./configure.sh
	make

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv:
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py
