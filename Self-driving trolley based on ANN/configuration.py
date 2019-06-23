"""Configurations for the RC car"""
CLASSIFICATION_LABELS = ['forward', 'reverse', 'left', 'right', 'idle']
CLASSIFICATION_LABELS_AND_VALUES = {
    'forward': [1, 0, 0, 0, 0],
    'reverse': [0, 1, 0, 0, 0],
    'left': [0, 0, 1, 0, 0],
    'right': [0, 0, 0, 1, 0],
    'idle': [0, 0, 0, 0, 1]
}


IMAGE_DIMENSIONS = (80, 60)
LAMBDA = 0.05
HIDDEN_LAYER_SIZE = 100
