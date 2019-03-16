#!/usr/bin/env python
# encoding: utf-8
# Author: yongyuan.name

import os
import numpy as np
from yael import ynumpy

from score_retrieval.data import datasets_str
txt_path = './data/{}.txt'.format(datasets_str)
sift_dir = './opencv_sifts'

with open(txt_path, 'r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]


desc_path = "./descs/{}.npy".format(datasets_str)
if os.path.exists(desc_path):
    all_desc = np.load(desc_path)

else:
    all_desc = []
    for i, line in enumerate(content):

        # exclude query images
        from score_retrieval.data import query_paths
        if line in query_paths:
            continue

        print "%d(%d): %s" %(i+1, len(content), line)
        hesaff_path = os.path.join(sift_dir, os.path.splitext(os.path.basename(line))[0] + '.opencv.sift')
        hesaff_info = np.loadtxt(hesaff_path, skiprows=2)
        if hesaff_info.shape[0] == 0:
           continue
        elif hesaff_info.shape[0] > 0 and len(hesaff_info.shape) == 1:
            desc = hesaff_info[5:]
            all_desc.append(desc)
        elif hesaff_info.shape[0] > 0 and len(hesaff_info.shape) > 1:
            desc = hesaff_info[:, 5:]
            all_desc.append(desc)


    # make a big matrix with all image descriptors
    all_desc = np.sqrt(np.vstack(all_desc))
    #n_sifts = all_desc.shape[0]
    #for i in range(n_sifts):
    #    if np.linalg.norm(all_desc[i], ord=2) == 0.0:
    #        continue
    #    all_desc[i] = all_desc[i]/np.linalg.norm(all_desc[i], ord=2)

    # sift: root-sift
    #n_sifts = all_desc.shape[0]
    #for i in range(n_sifts):
        #if np.linalg.norm(all_desc[i], ord=1) == 0.0:
        #    continue
        #all_desc[i] = np.sqrt(all_desc[i]/np.linalg.norm(all_desc[i], ord=1))

    # sift: sign(x)log(1 + |x|)
    #n_sifts = all_desc.shape[0]
    #for i in range(n_sifts):
    #    all_desc[i] = np.sign(all_desc[i]) * np.log(1.0 + np.abs(all_desc[i]))

    np.save(desc_path, all_desc)


k = 128
# k = 32  # for ease of testing
# n_sample = 256 * 1000  # original
n_sample = 256 * 100  # fixes memory issues

# choose n_sample descriptors at random
np.random.seed(1024)
sample_indices = np.random.choice(all_desc.shape[0], n_sample)
sample = all_desc[sample_indices]

# until now sample was in uint8. Convert to float32
sample = sample.astype('float32')

# compute mean and covariance matrix for the PCA
mean = sample.mean(axis = 0)
sample = sample - mean
cov = np.dot(sample.T, sample)

# compute PCA matrix and keep only 64 dimensions
eigvals, eigvecs = np.linalg.eig(cov)
perm = eigvals.argsort()                   # sort by increasing eigenvalue
print("perm.shape = {}".format(perm.shape))
pca_transform = eigvecs[:, perm[96:128]]   # eigenvectors for the 64 last eigenvalues

# transform sample with PCA (note that numpy imposes line-vectors,
# so we right-multiply the vectors)
sample = np.dot(sample, pca_transform)

# train GMM
print "start train GMM ......."
# gmm = ynumpy.gmm_learn(sample, k, nt = 400, niter = 2000, seed = 0, redo = 1, use_weights = True)  # original
gmm = ynumpy.gmm_learn(sample, k, nt = 100, niter = 1500, seed = 0, redo = 1, use_weights = True)  # fixes memory issues

np.save("./opencv_models/weight.gmm", gmm[0])
np.save("./opencv_models/mu.gmm", gmm[1])
np.save("./opencv_models/sigma.gmm", gmm[2])
np.save("./opencv_models/mean.gmm", mean)
np.save("./opencv_models/pca_transform.gmm", pca_transform)
