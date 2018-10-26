# Create a text file with names of all .png files in mini dataset
# for use in the cnn-cbir-benchmark repo

import os
DATAPATH = '/home/mirlab/score-retrieval/data/mini_dataset/'

files = []
for (dirpath, dirnames, filenames) in os.walk(DATAPATH):
    files.extend(filenames)
    break
files = [filename for filename in files if '.png' in filename] # only keep png files

with open('minidataset.txt', 'w') as f:
    for item in files:
        f.write("%s\n" % item)