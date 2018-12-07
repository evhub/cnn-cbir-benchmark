## Benchmark for Image Retrieval (BKIR)

[![License](https://img.shields.io/badge/license-BSD-blue.svg)](../LICENSE)

This project tries to build a benchmark for image retrieval, particularly for Instance-level image retrieval.

## Running on Scores Dataset

Fisher vector and VLAD are both currently working on the scores dataset. To run them,

1. install `score-retrieval`,
2. run `make`, follow the instructions, then run `make` again,
3. run `make yael`,
4. run `make hesaff`,
5. run `make minidataset`,
6. run the commands in the `fv` or `vlad` make target manually (`make fv`/`make vlad` isn't working right now for some reason).

Note: The training parameters in `gmm.py` (for FV) and `kmeans.py` (for VLAD) have been massively reduced for ease of testing. If you want a real training run, increase them.

## Methods

<!-- The following methods are evaluated on [Oxford Building dataset](http://www.robots.ox.ac.uk/~vgg/data/oxbuildings/). The evaluation adopts mean Average Precision (mAP), which is computed using the code provided by [compute_ap.cpp](http://www.robots.ox.ac.uk/~vgg/data/oxbuildings/compute_ap.cpp). -->

method | feature |  mAP (best) | status | links
:---:|:---:|:---:|:---:|:---:
fc_retrieval | CNN | 60.2% | finished | [fc_retrieval](https://github.com/willard-yuan/cnn-cbir-benchmark/tree/master/fc_retrieval)
rmac_retrieval | CNN | to be tested | finished | [rmac_retrieval](https://github.com/willard-yuan/cnn-cbir-benchmark/tree/master/rmac_retrieval)
crow_retrieval | CNN | to be tested | finished | [crow_retrieval](https://github.com/willard-yuan/cnn-cbir-benchmark/tree/master/crow_retrieval)
fv_retrieval | SIFT | 67.29% | finished | [fv_retrieval](https://github.com/willard-yuan/cnn-cbir-benchmark/tree/master/fv_retrieval)
vlad_retrieval | SIFT | 63.13% | finished | [vlad_retrieval](https://github.com/willard-yuan/cnn-cbir-benchmark/tree/master/vlad_retrieval)

the methods on above have the following characteristics:

- **Low dimension**
- **Time - tested**
- **Used in industry**

## Contr<!-- ibution

If you are interested in this project, feel free to contribute your code. Only Python and --> C++ code are accepted.
