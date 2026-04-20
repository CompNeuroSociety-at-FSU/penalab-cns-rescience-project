# This is where the class based ong the giant fiber system will be tested and worked on, so in the separate file
# So yeah

from brian2 import *
import matplotlib
import numpy
import gfs

if __name__ == "__main__":
    example_1 = gfs.gfs_object()
    print(example_1.gf_neurons)