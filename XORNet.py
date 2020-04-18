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
# 1 (1, 3) input1 to OR
# 2 (0, 2) input0 to NAND
# 3 (1, 3) input1 to NAND
# 4 (2, 4) OR to output
# 5 (3, 4) NAND to output
weights = np.random.random(6)
print("Initial random weights: ")
print(weights)

# Creating constants for our high and low inputs to represent 0 or 1
LOW_INPUT = 2
HIGH_INPUT = 11

# Creating tuples for our inputs
inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]

# Constants for our weight change
ALPHA = .0000002
DECAY = .001


def train():

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    neuron0output = 0
    neuron1output = 0

    neuron0activity = 0
    neuron1activity = 0
    neuron2activity = 0
    neuron3activity = 0
    neuron4activity = 0

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
                neuron1output = inputNeuron1.run(LOW_INPUT)
                neuron2training = PROHIBIT
                neuron3training = FORCE_SPIKE
                neuron4training = PROHIBIT
            elif i == (0, 1):
                neuron0output = inputNeuron0.run(LOW_INPUT)
                neuron1output = inputNeuron1.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = FORCE_SPIKE
            elif i == (1, 0):
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron1.run(LOW_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = FORCE_SPIKE
            elif i == (1, 1):
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron1.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = PROHIBIT
                neuron4training = PROHIBIT

            # We find the activity in a 100 time unit interval
            for k in range(100):
                # adds 1 if the neuron spiked, adds 0 otherwise
                neuron0activity += neuron0output[0]
                neuron1activity += neuron1output[0]

                # run the or neuron with current given by input neurons and training value
                neuron2charge = neuron0output[1] * weights[0] + neuron1output[1] * weights[1] + neuron2training
                neuron2output = middleNeuron2.run(neuron2charge)
                neuron2activity += neuron2output[0]

                # run the nand neuron with current given by input neurons and training value
                neuron3charge = neuron0output[1] * weights[2] + neuron1output[1] * weights[3] + neuron3training
                neuron3output = middleNeuron3.run(neuron3charge)
                neuron3activity += neuron3output[0]

                # run the output neuron with current given by hidden neurons and training value
                neuron4charge = neuron2output[1] * weights[4] + neuron3output[1] * weights[5] + neuron4training
                neuron4output = outputNeuron.run(neuron4charge)
                neuron4activity += neuron4output[0]

            # we now calculate weight adjustments based on activity of each neuron and constant decay
            weights[0] += ALPHA * neuron0activity * neuron2activity + DECAY
            weights[1] += ALPHA * neuron1activity * neuron2activity + DECAY
            weights[2] += ALPHA * neuron0activity * neuron3activity + DECAY
            weights[3] += ALPHA * neuron1activity * neuron3activity + DECAY
            weights[4] += ALPHA * neuron2activity * neuron4activity + DECAY
            weights[5] += ALPHA * neuron3activity * neuron4activity + DECAY


# Runs the input 100 times to shown activity in a 100 time unit interval
# If this gate is working, we should see a significant amount of spikes when we expect XOR to return 1
# and far fewer spikes when we expect XOR to return 0
def test(x, y):

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    neuron0spikes = 0
    neuron1spikes = 0

    totalSpikes = 0

    for i in range(100):

        if x == 0 and y == 0:
            neuron0spikes = inputNeuron0.run(LOW_INPUT)[1]
            neuron1spikes = inputNeuron1.run(LOW_INPUT)[1]
        elif x == 0 and y == 1:
            neuron0spikes = inputNeuron0.run(LOW_INPUT)[1]
            neuron1spikes = inputNeuron1.run(HIGH_INPUT)[1]
        elif x == 1 and y == 0:
            neuron0spikes = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1spikes = inputNeuron1.run(LOW_INPUT)[1]
        elif x == 1 and y == 1:
            neuron0spikes = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1spikes = inputNeuron1.run(HIGH_INPUT)[1]

        neuron2spikes = middleNeuron2.run(neuron0spikes * weights[0] + neuron1spikes * weights[1])[1]
        neuron3spikes = middleNeuron3.run(neuron0spikes * weights[2] + neuron1spikes * weights[3])[1]
        neuron4spikes = outputNeuron.run(neuron2spikes * weights[4] + neuron3spikes * weights[5])[1]
        totalSpikes += neuron4spikes

    return totalSpikes


train()
print("Trained weights")
print(weights)

print("Running values for (0, 0), (0, 1), (1, 0), (1, 1)")
print(test(0, 0))
print(test(0, 1))
print(test(1, 0))
print(test(1, 1))
