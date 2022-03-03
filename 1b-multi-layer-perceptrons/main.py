import time

from data_generation_lib import *
from multi_layer_perceptron import MultiLayerPerceptron
import numpy as np


def main():
    function_approx(False)


def generate_data_vary_number_of_hidden_nodes():
    # for i in [1, 2, 4, 8, 16]:
    get_results(100, 0.001, 100, 20, 16)


def generate_data_with_bias(N):
    d1, d2 = generate_data_points([[0, 0], [2, 2]], [[3, 3], [1, 1]], N)
    subset_N = int(N / 4)
    subset_d1 = d1[:subset_N]
    subset_d2 = d2[:subset_N]
    d1 = d1[subset_N:]
    d2 = d2[subset_N:]
    # visualize_data(d1, d2)


def function_approx(visualize=False):
    patterns, targets = generate_functional_data(True)
    hidden_layer_size=25
    Iterations = 20
    Epochs = 300
    mse_per_epoch = np.zeros((Iterations, Epochs))
    for iteration in range(Iterations):
        model = MultiLayerPerceptron(patterns.shape[1], hidden_layer_size=hidden_layer_size, output_dimensions=1, training_set=patterns,
                                     learning_rate=0.001, alpha=0.9)
        for epoch in range(Epochs):
            model.forward_pass()
            model.backward_pass(targets)
            if visualize:
                model.visualize_function_approx()
            mse_per_epoch[iteration][epoch] = model.mse(targets)
    mse_per_epoch = np.mean(mse_per_epoch, axis=0)
    f = open('hidden_layer_size=' + str(hidden_layer_size) + str('_function_approx.txt'), 'w')
    for epoch in mse_per_epoch:
        f.write(str(epoch)+'\n')


def training(data_subset, labels_subset, num_of_hidden_nodes, validation_set, validation_labels, epochs):
    model = MultiLayerPerceptron(data_subset.shape[1], hidden_layer_size=num_of_hidden_nodes, output_dimensions=1,
                                 training_set=data_subset,
                                 learning_rate=0.001, alpha=0.8)
    predictions = np.zeros(epochs)

    for i in range(epochs):
        model.forward_pass()
        model.backward_pass(labels_subset)
        prediction = number_of_misclassified_samples_per_class(model, validation_set, validation_labels)
        predictions[i] = prediction

    return predictions

    #sampling data
    d1_train, d2_train, d1_val, d2_val = remove_samples(d1, d2, 100, 0.5, 0)
    print(len(d1_train), len(d2_train), len(d1_val), len(d2_val))
    data_train, labels_train = concatenate_and_shuffle(d1_train, d2_train, -1, 1)
    data_val, labels_val = concatenate_and_shuffle(d1_val, d2_val, -1, 1)
    data_train = add_bias(data_train)
    data_val = add_bias(data_val)
    sampled_model = MultiLayerPerceptron(data_train.shape[1], hidden_layer_size=3, output_dimensions=1, training_set=data_train,
                                learning_rate=0.00001, alpha=0.8, val_set= data_val )

    total_prediction_ratio, prediction_ratios=train_and_test_data(sampled_model, data_train, labels_train, data_val, labels_val, epochs=20)
    print("total prediction ratio\n", total_prediction_ratio)
    print("prediction_ratios\n",prediction_ratios )








    



def train_and_test_data(model, training_set, training_labels, val_set, val_labels, epochs):
    
    prediction_ratios = np.zeros((epochs, 2))
    total_prediction_ratio = np.zeros(epochs)

    for epoch in range(epochs):
        count1 = 0
        correct1 = 0
        count2 = 0
        correct2 = 0
        index = 0
        prediction = model.forward_pass_val()
        model.forward_pass()
        model.backward_pass(training_labels)


        for data_point, label in zip(val_set, val_labels):
            if label == 0 or label == -1:
                count1 += 1
                if prediction[index] <= 0:
                    correct1 += 1
            else:
                count2 += 1
                if prediction[index] > 0:
                    correct2 += 1
            index += 1
        if count1==0:
            prediction_ratios[epoch][0] = 0
        else:
            prediction_ratios[epoch][0] = correct1 / count1
        if count2==0:
            prediction_ratios[epoch][1] = 0
        else:
            prediction_ratios[epoch][1] = correct2 / count2
        total_prediction_ratio[epoch] = (correct1 + correct2) / (count1 + count2)
    return total_prediction_ratio, prediction_ratios







def get_results(N, learning_rate, iterations, epochs, num_of_hidden_nodes):
    ratios = np.zeros((iterations, epochs, 2))

    for i in range(iterations):
        random.seed(time.time())
        data, label, data_subset, labels_subset = generate_data_with_bias(N)
        prediction_ratios = training(data_subset, labels_subset, num_of_hidden_nodes, data, label, epochs)
        # prediction_ratios = number_of_misclassified_samples_per_class(model, data, label)
        ratios[i] = prediction_ratios
    ratios = np.mean(ratios, axis=0)
    write_results_to_file(str(num_of_hidden_nodes) + '_num_of_hidden_nodes' + str(time.time()) + '.txt', learning_rate,
                          num_of_hidden_nodes, ratios)


def write_results_to_file(filename, learning_rate, num_of_hidden_nodes, ratios):
    f = open(filename, 'w')
    f.write(str(learning_rate) + " " + str(num_of_hidden_nodes) + '\n')
    for ratio in ratios:
        f.write(str(ratio))
        f.write('\n')
    f.flush()


def number_of_misclassified_samples_per_class(model, validation_set, validation_labels):
    count1 = 0
    correct1 = 0
    count2 = 0
    correct2 = 0
    predictions = model.forward_pass(validation_set)
    for prediction, label in zip(predictions, validation_labels):
        if label == 0 or label == -1:
            count1 += 1
            if prediction <= 0:
                correct1 += 1
        else:
            count2 += 1
            if prediction > 0:
                correct2 += 1
    prediction_ratio_1 = correct1 / count1
    prediction_ratio_2 = correct2 / count2
    return prediction_ratio_1, prediction_ratio_2

def remove_samples(d1, d2, n, class1_removal, class2_removal):
    class1_adjusted_len = n - round(n * class1_removal)
    d1_train = d1[:class1_adjusted_len]
    d1_val = d1[class1_adjusted_len:]

    class2_adjusted_len = n - round(n * class2_removal)
    d2_train = d2[:class2_adjusted_len]
    d2_val = d2[class2_adjusted_len:]

    return d1_train, d2_train, d1_val, d2_val





main()
