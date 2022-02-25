import numpy as np
from rbf_net import RBFNetwork

def sin2(x):
    return np.sin(2 * x)

def square(x):
    if np.sin(2 * x) >= 0:
        return 1
    else:
        return -1

network = RBFNetwork(n_inputs=1, n_rbf=50, n_outputs=1)
x_train = np.arange(0, 2*np.pi, 0.1)
y = np.zeros(x_train.shape)
y_train_target = list(map(square, x_train))

x_test = np.arange(0.05, 2*np.pi, 0.1)
y_test_target = list(map(square, x_train))


