import numpy as np
import random


class HopfieldNet:
    def __init__(self, max_iter=200):
        self.w = None
        self.n_elements = None
        self.max_iter = max_iter
        self.hundredth_images = None

    def energy(self, pattern):
        pattern = pattern.reshape((1, -1))
        return -1 * pattern @ self.w @ pattern.T

    def fit(self, patterns):
        patterns = np.array(patterns)
        if len(patterns.shape) == 1:
            patterns = np.reshape(patterns, (1, -1))
        self.n_elements = patterns.shape[1]
        self.w = np.zeros((self.n_elements, self.n_elements))
        for pattern in patterns:
            pattern = np.reshape(pattern, (-1, 1))
            self.w += (pattern @ pattern.T) / self.n_elements

    def predict(self, pattern, method='batch', show_energy=False, collect_hundredth_image=False):
        input_pattern = pattern.reshape((-1, self.n_elements))
        current_pattern = input_pattern.copy()
        self.hundredth_images = []
        i = 0.0
        while i <= self.max_iter:
            if method == 'batch':
                current_pattern = self._batch_update(current_pattern)
                i += 1
            if method == 'sequential':
                current_pattern = self._sequential_update(current_pattern)
                i += 0.1
            if show_energy and round(i, ndigits=3) % 10 == 0:
                print(self.energy(current_pattern))
            if collect_hundredth_image and round(i, ndigits=3) % 10 == 0:
                self.hundredth_images.append(current_pattern.copy())
        return current_pattern

    def random_weights(self):
        self.w = np.random.normal(0, 1, (self.n_elements, self.n_elements))

    def make_weights_symmetric(self):
        self.w = 0.5 * np.add(self.w, self.w.T)

    def remove_diagonals(self):
        for i in range(self.n_elements):
            self.w[i][i] = 0

    def _sequential_update(self, pattern):
        index = random.randint(0, pattern.shape[1] - 1)
        pattern[0][index] = np.sign(np.dot(pattern[0], self.w[index]))
        return pattern

    def _batch_update(self, pattern):
        return np.sign(pattern @ self.w)

    def is_stable(self, pattern):
        new_pattern = pattern.copy()
        new_pattern = self._batch_update(new_pattern)
        return np.array_equal(new_pattern, pattern)


class HopfieldNetBinary:
    def __init__(self, max_iter=200, theta=0):
        self.w = None
        self.n_elements = None
        self.max_iter = max_iter
        self.hundredth_images = None
        self.theta = theta

    def energy(self, pattern):
        pattern = pattern.reshape((1, -1))
        return -1 * pattern @ self.w @ pattern.T

    def fit(self, patterns):
        patterns = np.array(patterns)
        p = np.mean(patterns)
        if len(patterns.shape) == 1:
            patterns = np.reshape(patterns, (1, -1))
        self.n_elements = patterns.shape[1]
        self.w = np.zeros((self.n_elements, self.n_elements))
        for pattern in patterns:
            pattern = np.reshape(pattern, (-1, 1))
            self.w += ((pattern - p) @ (pattern.T - p))

    def predict(self, pattern, show_energy=False, collect_hundredth_image=False):
        input_pattern = pattern.reshape((-1, self.n_elements))
        current_pattern = input_pattern.copy()
        self.hundredth_images = []
        i = 0.0
        while i <= self.max_iter:
            current_pattern = self._sequential_update(current_pattern)
            if show_energy and round(i, ndigits=3) % 10 == 0:
                print(self.energy(current_pattern))
            if collect_hundredth_image and round(i, ndigits=3) % 10 == 0:
                self.hundredth_images.append(current_pattern.copy())
            i += 0.1
        return current_pattern

    def random_weights(self):
        self.w = np.random.normal(0, 1, (self.n_elements, self.n_elements))

    def make_weights_symmetric(self):
        self.w = 0.5 * np.add(self.w, self.w.T)

    def remove_diagonals(self):
        for i in range(self.n_elements):
            self.w[i][i] = 0

    def _sequential_update(self, pattern):
        curr_pattern = pattern.copy()
        index = random.randint(0, pattern.shape[1] - 1)
        temp_pattern = 0
        for j in range(self.n_elements):
            temp_pattern += self.w[index][j] * curr_pattern[0][j] - self.theta
        curr_pattern[0][index] = 0.5 + 0.5 * np.sign(temp_pattern)
        return curr_pattern

    def _batch_update(self, pattern):
        return np.sign(pattern @ self.w)

    def is_stable(self, pattern):
        new_pattern = pattern.copy()
        new_pattern = self._batch_update(new_pattern)
        return np.array_equal(new_pattern, pattern)
