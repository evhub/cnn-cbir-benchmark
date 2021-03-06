#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import numpy as np
from yael import ynumpy
import time


from score_retrieval.constants import DEFAULT_DATASET
txt_path = './data/{}.txt'.format(DEFAULT_DATASET)
# sift_dir = './hesaff_sifts/'  # '/home/yuanyong/py/fv_retrieval/oxford_hesaff_sift'
sift_dir = "./opencv_sifts"

with open(txt_path, 'r') as f:
    content = f.readlines()
    content = [x.strip() for x in content]


all_desc = []
for i, line in enumerate(content):

    # exclude query images
    from score_retrieval.data import query_paths
    if line in query_paths:
        continue

    print "%d(%d): %s" %(i+1, len(content), line)
    # hesaff_path = os.path.join(sift_dir, os.path.splitext(os.path.basename(line))[0] + '.hesaff.sift')
    hesaff_path = os.path.join(sift_dir, os.path.splitext(os.path.basename(line))[0] + '.opencv.sift')
    hesaff_info = np.loadtxt(hesaff_path, skiprows=2)  # np.loadtxt(hesaff_path)
    if hesaff_info.shape[0] == 0:
       continue
    elif hesaff_info.shape[0] > 0 and len(hesaff_info.shape) == 1:
        desc = hesaff_info[5:]
        all_desc.append(desc)
    elif hesaff_info.shape[0] > 0 and len(hesaff_info.shape) > 1:
        desc = hesaff_info[:, 5:]
        all_desc.append(desc)

# make a big matrix with all image descriptors, rootsift
all_desc = np.sqrt(np.vstack(all_desc))

n_sample = 256 * 1000

# choose n_sample descriptors at random
np.random.seed(1024)
sample_indices = np.random.choice(all_desc.shape[0], n_sample)
sample = all_desc[sample_indices]

# until now sample was in uint8. Convert to float32
sample = sample.astype('float32') # yael likes floats better than doubles

# compute mean and covariance matrix for the PCA
mean = sample.mean(axis = 0)
sample = sample - mean
cov = np.dot(sample.T, sample)

# compute PCA matrix and keep only 64 dimensions
eigvals, eigvecs = np.linalg.eig(cov)
perm = eigvals.argsort()                   # sort by increasing eigenvalue
pca_transform = eigvecs[:, perm[64:128]]   # eigenvectors for the 64 last eigenvalues

# transform sample with PCA (note that numpy imposes line-vectors,
# so we right-multiply the vectors)
sample = np.dot(sample, pca_transform)

# train Kmeans
print "start train kmeans ......."

print sample.shape[0]

# number of cluster to create
k = 128
# k = 32  # for ease of testing
# dimensionality of the vectors
d = sample.shape[1]
# number of vectors
n = sample.shape[0]
# number of threads to use
nt = 20
# number of iterations (0 for convergence)
niter = 0
# number of redo
redo = 1

t0 = time.time()
(centroids, qerr, dis, assign, nassign) = ynumpy.kmeans(sample, k, nt = nt, niter = niter, redo = redo, output = 'full')
t1 = time.time()
print "kmeans performed in %.3f s" % (t1 - t0)

np.save("./models/centroids_data.npy", centroids)
np.save("./models/pca_data.npy", pca_transform)
np.save("./models/mean_data.npy", mean)
