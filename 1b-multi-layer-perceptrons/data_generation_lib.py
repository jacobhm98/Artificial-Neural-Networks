import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import multivariate_normal


def generate_functional_data(create_plot=False):
    N = 21
    x = np.linspace(-5.0, 5.0, num=N).reshape((N, 1))
    y = np.linspace(-5.0, 5.0, num=N).reshape((N, 1))
    z = np.matmul(np.exp(-x * x * 0.1), np.exp(-y * y * 0.1).T) - 0.5
    targets = np.reshape(z, (N**2, 1))
    xx, yy = np.meshgrid(x, y)
    if create_plot:
        plt.contour(xx, yy, z)
        plt.show()
    x_dat = np.reshape(xx, (N**2, 1))
    y_dat = np.reshape(yy, (N**2, 1))
    patterns = np.concatenate((x_dat, y_dat), axis=1)
    patterns = add_bias(patterns)
    return patterns, targets

def generate_data_points(param1, param2, n, class1_removal=None, class2_removal=None):
    distr1 = multivariate_normal(param1[0], param1[1])
    distr2 = multivariate_normal(param2[0], param2[1])
    data1 = np.zeros((n, 2))
    data2 = np.zeros((n, 2))
    for i in range(n):
        data1[i] = distr1.rvs()
        data2[i] = distr2.rvs()
    if class1_removal is not None:
        class1_adjusted_len = n - round(n * class1_removal)
        data1 = data1[:class1_adjusted_len]
    if class2_removal is not None:
        class2_adjusted_len = n - round(n * class2_removal)
        data2 = data2[:class2_adjusted_len]
    return data1, data2


def remove_from_subset(d1):
    count1 = 0
    count2 = 0
    for d in d1:
        if d[0] < 0:
            count1 += 1
        elif d[0] > 0:
            count2 += 1
    to_remove1 = round(count1 * 0.2)
    to_remove2 = round(count2 * 0.8)
    deleted1 = 0
    deleted2 = 0
    i = 0
    while deleted1 < to_remove1 or deleted2 < to_remove2:
        if d1[i][0] < 0 and deleted1 < to_remove1:
            d1 = np.delete(d1, i, axis=0)
            deleted1 += 1
            continue

        elif d1[i][0] > 0 and deleted2 < to_remove2:
            d1 = np.delete(d1, i, axis=0)
            deleted2 += 1
            continue
        i += 1
    return d1


def visualize_data(data1, data2):
    plt.scatter(data1[:, 0], data1[:, 1], c='red')
    plt.scatter(data2[:, 0], data2[:, 1], c='blue')
    plt.show()


def concatenate_and_shuffle(d1, d2, class1, class2):
    concatenated = np.concatenate((d1, d2), axis=0)
    concatenated = concatenated.tolist()
    labels = [class1] * d1.shape[0] + [class2] * d2.shape[0]
    data = list(zip(concatenated, labels))
    random.shuffle(data)
    data, labels = list(zip(*data))
    return np.array(data), np.array(labels)


def add_bias(data_set):
    N = data_set.shape[0]
    biases = np.ones((N, 1))
    data_set = np.concatenate((data_set, biases), axis=1)
    return data_set


def generate_gaussian_data_points(domain, variance):
    x = np.arange(-domain, domain, variance)
    y = np.arange(-domain, domain, variance)
    x, y = np.meshgrid(x, y)
    r = np.sqrt(x ** 2 + y ** 2)
    z = (1. / np.sqrt(1 * np.pi)) * np.exp(-.5 * r ** 2)
    return x, y, z


def plot_3d_plot(x, y, z):
    fig = plt.figure(figsize=(12, 6))
    ax = fig.gca(projection='3d')
    ax.plot_surface(x, y, z,
                    cmap=cm.coolwarm,
                    linewidth=0,
                    antialiased=True)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    plt.show()
