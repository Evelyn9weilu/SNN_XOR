from LIF import LIF_Neuron
import numpy as np
import math


# Neuron 0 and 1 are input neurons. Neurons 2 and 3 are hidden layer neurons. Neuron 4 is the output neuron

# 2 input neurons, 1 for first num and another for second num
inputNeuron0 = None
inputNeuron1 = None
# 2 hidden neurons, one representing or and one representing nand
middleNeuron2 = None
middleNeuron3 = None
# 1 output neuron, fires high if XOR, fires low if !XOR
outputNeuron = None

# Creating random initial weights
# Weights represent directed edges in this network:
# 0 (0, 2) input0 to OR
# 1 (0, 3) input0 to NAND
# 2 (1, 2) input1 to OR
# 3 (1, 3) input1 to NAND
# 4 (2, 4) OR to output
# 5 (3, 4) NAND to output
weights = np.random.random(6)
# print("Initial random weights: ")
# print(weights)

# Creating constants for our high and low inputs to represent 0 or 1
LOW_INPUT = 1
HIGH_INPUT = 11

# Creating tuples for our inputs
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Constants for our weight change
ALPHA = .01
DECAY = .01


def train():

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    neuron0output = 0
    neuron1output = 0
    neuron2output = 0
    neuron3output = 0
    neuron4output = 0

    neuron0activity = 0
    neuron1activity = 0
    neuron2activity = 0
    neuron3activity = 0
    neuron4activity = 0
    neuron5activity = 0

    # These values simulate a training current that either force or spike or prohibit a spike
    neuron2training = 0
    neuron3training = 0
    neuron4training = 0
    FORCE_SPIKE = 20
    PROHIBIT = -20

    # Train network 5,000 times
    for j in range(5000):
        # Each iteration trains every possible input once
        for i in inputs:
            if i == (0, 0):
                neuron0output = inputNeuron0.run(LOW_INPUT)
                neuron1output = inputNeuron0.run(LOW_INPUT)
                neuron2training = PROHIBIT
                neuron3training = FORCE_SPIKE
                neuron4training = PROHIBIT
            elif i == (0, 1):
                neuron0output = inputNeuron0.run(LOW_INPUT)
                neuron1output = inputNeuron0.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = FORCE_SPIKE
            elif i == (1, 0):
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron0.run(LOW_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = FORCE_SPIKE
            elif i == (1, 1):
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron0.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = PROHIBIT
                neuron4training = PROHIBIT

            # We find the activity in a 500 unit interval
            for k in range(500):
                if neuron0output[0] == 1:
                    neuron0activity += 1

    return


# Runs the input 100 times to shown activity in a 100 unit interval
# If this gate is working, we should see a significant amount of spikes when we expect XOR to return 1
# and far fewer spikes when we expect XOR to return 0
def test(x, y):

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    neuron0output = 0
    neuron1output = 0
    neuron2output = 0
    neuron3output = 0
    neuron4output = 0

    totalSpikes = 0

    for i in range(100):

        if x == 0 and y == 0:
            neuron0output = inputNeuron0.run(LOW_INPUT)[1]
            neuron1output = inputNeuron0.run(LOW_INPUT)[1]
        elif x == 0 and y == 1:
            neuron0output = inputNeuron0.run(LOW_INPUT)[1]
            neuron1output = inputNeuron0.run(HIGH_INPUT)[1]
        elif x == 1 and y == 0:
            neuron0output = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1output = inputNeuron0.run(LOW_INPUT)[1]
        elif x == 1 and y == 1:
            neuron0output = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1output = inputNeuron0.run(HIGH_INPUT)[1]

        neuron2output = middleNeuron2.run(neuron0output * weights[0] + neuron1output * weights[1])[1]
        neuron3output = middleNeuron3.run(neuron0output * weights[2] + neuron1output * weights[3])[1]
        neuron4output = outputNeuron.run(neuron2output * weights[4] + neuron3output * weights[5])
        totalSpikes += neuron4output[0]

    return totalSpikes


train()
print(weights)
print(test(0, 0))
print(test(0, 1))
print(test(1, 0))
print(test(1, 1))
