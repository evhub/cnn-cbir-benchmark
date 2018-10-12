export PYTHONPATH := ${CURDIR}/yael

.PHONY: setup
setup:
	python2 -m pip install numpy h5py scikit-learn opencv-python
	-mkdir ./opencv_models
	-mkdir ./opencv_sifts
	-mkdir ./hesaff_sifts
	echo "You need to run both of the following commands:"
	echo "source activate py2"
	echo "export PYTHONPATH=\"${PYTHONPATH}\""

.PHONY: yael
yael:
	svn checkout https://scm.gforge.inria.fr/anonscm/svn/yael/trunk yael
	cp ./makefile.inc ./yael/makefile.inc
	cd yael; make

.PHONY: opencv
opencv:
	cd ~; git clone https://github.com/Itseez/opencv.git
	cd ~/opencv; git checkout 3.0.0
	cd ~; git clone https://github.com/Itseez/opencv_contrib.git
	cd ~/opencv_contrib; git checkout 3.0.0
	mkdir ~/opencv/build
	cd ~/opencv/build; cmake -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=/usr/local -DOPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules -Wno-dev ..
	cd ~/opencv/build; make -j4
	cd ~/opencv/build; sudo make install
	sudo ldconfig
	cd /usr/lib/python2.7/site-packages/; ln -s /usr/local/lib/python2.7/site-packages/cv2.so ~/opencv/build/cv2.so

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
	python2 ./fv_retrieval/src/extract_opencvsift.py
	python2 ./fv_retrieval/src/gmm.py
	python2 ./fv_retrieval/src/fv.py
	python2 ./fv_retrieval/src/brute.py

.PHONY: fc
fc:
	python2 ./fc_retrieval/src/oxford5k_feats_extract.py
	python2 ./fc_retrieval/src/brute.py

.PHONY: vlad
vlad:
	python2 ./fv_retrieval/src/extract_hesaff.py
	python2 ./vlad_retrieval/src/kmeans.py
	python2 ./vlad_retrieval/src/vlad.py
	python2 ./vlad_retrieval/src/brute.py

.PHONY: all
all: fv fc vlad
