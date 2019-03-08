"""
Create a text file with names of all .png files in mini dataset
for use in the cnn-cbir-benchmark repository.
"""

import os

from score_retrieval.data import DEFAULT_DATASET
from score_retrieval.data import index_images


def write_index(dataset=DEFAULT_DATASET):
    """Write index of image paths to given index_fpath."""
    index_fpath = os.path.join(os.path.dirname(__file__), "data", "{}.txt".format(dataset))
    with open(index_fpath, "w") as index_file:
        for _, path in index_images(dataset=dataset):
            index_file.write("{}\n".format(path))


if __name__ == "__main__":
    write_index()
