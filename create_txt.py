"""
Create a text file with names of all .png files in mini dataset
for use in the cnn-cbir-benchmark repository.
"""

import os

from score_retrieval.data import database_paths


default_index_fpath = os.path.join(os.path.dirname(__file__), "data", "minidataset.txt")


def write_index(index_fpath=default_index_fpath):
    """Write index of image paths to given index_fpath."""
    with open(index_fpath, "w") as index_file:
        for path in database_paths:
            index_file.write("{}\n".format(path))


if __name__ == "__main__":
    write_index()
