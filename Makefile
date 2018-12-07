export PYTHONPATH := "${CURDIR}/yael"
export LD_LIBRARY_PATH := "/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:/usr/lib/x86_64-linux-gnu:/usr/lib64:/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64:/data/mirlab/miniconda3/envs/py2/lib"

.PHONY: setup
setup:
	python2 -m pip install numpy h5py scikit-learn opencv-contrib-python==3.4.2.16
	-mkdir opencv_models
	-mkdir opencv_sifts
	-mkdir hesaff_sifts
	-mkdir feats
	-mkdir models
	echo "You need to run all of the following commands:"
	echo "source activate py2"
	echo "export PYTHONPATH=\"${PYTHONPATH}\""
	echo "export LD_LIBRARY_PATH=\"${LD_LIBRARY_PATH}\""

.PHONY: minidataset
minidataset:
	python ./create_txt.py

.PHONY: yael
yael:
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cp ./makefile.inc ./yael/makefile.inc
	cd yael; make

.PHONY: hesaff
hesaff:
	-git clone https://github.com/evhub/hesaff.git
	cd hesaff; make

.PHONY: gcc
gcc:
	sudo update-alternatives --config gcc

.PHONY: clean
clean:
	rm -rf ./yael ./hesaff
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete

.PHONY: fv
fv: minidataset
	python2 ./fv_retrieval/src/extract_opencvsift.py
	python2 ./fv_retrieval/src/gmm.py
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py

.PHONY: vlad
vlad: minidataset
	python2 ./fv_retrieval/src/extract_opencvsift.py
	python2 ./vlad_retrieval/src/kmeans.py
	python2 ./vlad_retrieval/src/vlad.py
	python2 ./vlad_retrieval/src/brute.py

.PHONY: fc
fc: minidataset
	python2 ./fc_retrieval/src/oxford5k_feats_extract.py
	python2 ./fc_retrieval/src/brute.py
