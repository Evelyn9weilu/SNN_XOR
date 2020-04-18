from LIF import LIF_Neuron
import numpy as np
import math


# Neuron 0 and 1 are input neurons. Neurons 2 and 3 are hidden layer neurons. Neuron 4 is the output neuron

# 2 input neurons, 1 for first num and another for second num
inputNeurons = [LIF_Neuron(0)] * 2
# 2 hidden neurons, one representing or and one representing nand
middleNeurons = [LIF_Neuron(0)] * 2
# 1 output neuron, fires high if XOR, fires low if !XOR
outputNeuron = LIF_Neuron(0)

# Creating random initial weights
# Weights represent certain edges in this network:
# 0 (0,2) input0 to OR
# 1 (0,3) input0 to NAND
# 2 (1,2) input1 to OR
# 3 (1,3) input1 to NAND
# 4 (2,4) OR to output
# 5 (3,4) NAND to output
weights = np.random.random(6)
print("Initial random weights: " + weights)

# Creating constants for our high and low inputs to represent 0 or 1
LOW_INPUT = 2
HIGH_INPUT = 11

# Creating tuples for our inputs
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Constants for our weight change
ALPHA = 1


def train():
    # Train network 5,000 times
    for j in range(5000):
        # Train network for each input
        for i in inputs:
            if i == (0, 0):
                inputNeurons[0] = LIF_Neuron(LOW_INPUT)
                inputNeurons[1] = LIF_Neuron(LOW_INPUT)
            elif i == (0, 1):
                inputNeurons[0] = LIF_Neuron(LOW_INPUT)
                inputNeurons[1] = LIF_Neuron(HIGH_INPUT)
            elif i == (1, 0):
                inputNeurons[0] = LIF_Neuron(HIGH_INPUT)
                inputNeurons[1] = LIF_Neuron(LOW_INPUT)
            elif i == (1, 1):
                inputNeurons[0] = LIF_Neuron(HIGH_INPUT)
                inputNeurons[1] = LIF_Neuron(HIGH_INPUT)
    return


def test(x, y):
    if x == 0 and y == 0:
        inputNeurons[0] = LIF_Neuron(LOW_INPUT)
        inputNeurons[1] = LIF_Neuron(LOW_INPUT)
    elif x == 0 and y == 1:
        inputNeurons[0] = LIF_Neuron(LOW_INPUT)
        inputNeurons[1] = LIF_Neuron(HIGH_INPUT)
    elif x == 1 and y == 0:
        inputNeurons[0] = LIF_Neuron(HIGH_INPUT)
        inputNeurons[1] = LIF_Neuron(LOW_INPUT)
    elif x == 1 and y == 1:
        inputNeurons[0] = LIF_Neuron(HIGH_INPUT)
        inputNeurons[1] = LIF_Neuron(HIGH_INPUT)
    return


train()
print(weights)
print(test(0, 0))
print(test(0, 1))
print(test(1, 0))
print(test(1, 1))
