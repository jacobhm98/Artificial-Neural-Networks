from data_generation_lib import *
from multi_layer_perceptron import MultiLayerPerceptron
import numpy as np


def main():
    d1, d2 = generate_data_points([[-3.0, -3], [1, 1]], [[3, 3], [1, 1]], 100)
    data, labels = concatenate_and_shuffle(d1, d2, -1, 1)
    data = add_bias(data)
    model = MultiLayerPerceptron(data.shape[1], hidden_layer_size=8, output_dimensions=1, training_set=data,
                                 learning_rate=0.001, alpha=0.8)
    ratios_per_epoch = number_of_misclassified_samples_per_class(model, data, labels, epochs=20)
    print(ratios_per_epoch)


def number_of_misclassified_samples_per_class(model, training_set, labels, epochs):
    prediction_ratios = np.zeros((epochs, 2))
    total_prediction_ratio = np.zeros(epochs)
    for epoch in range(epochs):
        count1 = 0
        correct1 = 0
        count2 = 0
        correct2 = 0
        prediction = model.forward_pass()
        index = 0
        for data_point, label in zip(training_set, labels):
            if label == 0 or label == -1:
                count1 += 1
                if prediction[index] <= 0:
                    correct1 += 1
            else:
                count2 += 1
                if prediction[index] > 0:
                    correct2 += 1
            index += 1
        prediction_ratios[epoch][0] = correct1 / count1
        prediction_ratios[epoch][1] = correct2 / count2
        total_prediction_ratio[epoch] = (correct1 + correct2) / (count1 + count2)
        model.backward_pass(labels)
    return total_prediction_ratio, prediction_ratios


main()
