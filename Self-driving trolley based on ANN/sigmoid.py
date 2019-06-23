#!/usr/bin/env python
"""Sigmoid Function"""
from numpy import power, e

def sigmoid(x_value):
    """Return the sigmoid value"""
    return 1.0/(1.0 + power(e, -x_value))

'''
from matplotlib import pyplot as plt
import numpy as np

for x in range(-100,100,2):
    y = 1.0/(1 + np.power(np.e, -x))

plt.plot(x,y,'sigmoid')
'''


