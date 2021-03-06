from LIF import LIF_Neuron
import numpy as np

# Neuron 0 and 1 are input neurons. Neurons 2 and 3 are hidden layer neurons. Neuron 4 is the output neuron
# 2 input neurons, 1 for first num and another for second num
# 2 hidden neurons
# 1 output neuron, fires high if XOR, fires low if !XOR

# Creating random initial weights
# Weights represent directed edges in this network:
# 0 (0, 2) input0 to first hidden neuron
# 1 (1, 2) input1 to first hidden neuron
# 2 (0, 3) input0 to second hidden neuron
# 3 (1, 3) input1 to second hidden neuron
# 4 (2, 4) first hidden neuron to output
# 5 (3, 4) second hidden neuron to output
weights = np.random.random(6)
print("Initial random weights: ")
print(weights)

# hardbound for weights
WEIGHT_MAX = 1

# Creating constants for our high and low inputs to represent 0 or 1
LOW_INPUT = 1
HIGH_INPUT = 9

# Constants for our weight change
ALPHA = .175
DECAY = .002


def train():

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    # These values simulate a training current that either force or spike or prohibit a spike
    neuron2training = 0
    neuron3training = 0
    neuron4training = 0
    FORCE_SPIKE = 1000
    PROHIBIT = -2000

    # Train network with this many iterations
    for j in range(1000):

        # print("starting training iteration ", j)
        # print(weights)

        # Each iteration trains every possible input once
        for i in range(4):

            # We find the activity in a 100 time unit interval
            neuron0output = 0
            neuron1output = 0

            neuron0activity = 0
            neuron1activity = 0
            neuron2activity = 0
            neuron3activity = 0
            neuron4activity = 0

            # (0, 0)
            if i == 0:
                neuron0output = inputNeuron0.run(LOW_INPUT)
                neuron1output = inputNeuron1.run(LOW_INPUT)
                neuron2training = PROHIBIT
                neuron3training = FORCE_SPIKE
                neuron4training = PROHIBIT * 2
            # (1, 1)
            elif i == 1:
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron1.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = FORCE_SPIKE
            # (0, 1)
            elif i == 2:
                neuron0output = inputNeuron0.run(LOW_INPUT)
                neuron1output = inputNeuron1.run(HIGH_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = PROHIBIT
            # (1, 0)
            elif i == 3:
                neuron0output = inputNeuron0.run(HIGH_INPUT)
                neuron1output = inputNeuron1.run(LOW_INPUT)
                neuron2training = FORCE_SPIKE
                neuron3training = FORCE_SPIKE
                neuron4training = PROHIBIT

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

            # the activity must be reduced to represent what occurs in one time unit and as a decimal
            neuron0activity = neuron0activity / 1000
            neuron1activity = neuron1activity / 1000
            neuron2activity = neuron2activity / 1000
            neuron3activity = neuron3activity / 1000
            neuron4activity = neuron4activity / 1000

            # weight adjustments
            # we now calculate weight adjustments based on activity of each neuron and exponential decay

            # print("weight adjustments")

            weight0dw = ALPHA * neuron0activity * neuron2activity - DECAY * weights[0]
            # print(weight0dw)
            weights[0] += weight0dw

            weight1dw = ALPHA * neuron1activity * neuron2activity - DECAY * weights[1]
            # print(weight1dw)
            weights[1] += weight1dw

            weight2dw = ALPHA * neuron0activity * neuron3activity - DECAY * weights[2]
            # print(weight2dw)
            weights[2] += weight2dw

            weight3dw = ALPHA * neuron1activity * neuron3activity - DECAY * weights[3]
            # print(weight3dw)
            weights[3] += weight3dw

            weight4dw = ALPHA * neuron2activity * neuron4activity - DECAY * weights[4]
            # print(weight4dw)
            weights[4] += weight4dw

            weight5dw = ALPHA * neuron3activity * neuron4activity - DECAY * weights[5]
            # print(weight5dw)
            weights[5] += weight5dw

            # Bounding our weights
            for l in range(len(weights)):
                if weights[l] >= WEIGHT_MAX:
                    weights[l] = WEIGHT_MAX


# Runs the input 100 times to shown activity in a 100 time unit interval
# If this gate is working, we should see a significant amount of spikes when we expect XOR to return 1
# and far fewer spikes when we expect XOR to return 0
def test(x, y):

    inputNeuron0 = LIF_Neuron()
    inputNeuron1 = LIF_Neuron()
    middleNeuron2 = LIF_Neuron()
    middleNeuron3 = LIF_Neuron()
    outputNeuron = LIF_Neuron()

    totalSpikes = 0

    for i in range(100):

        neuron0current = 0
        neuron1current = 0

        if x == 0 and y == 0:
            neuron0current = inputNeuron0.run(LOW_INPUT)[1]
            neuron1current = inputNeuron1.run(LOW_INPUT)[1]
        elif x == 0 and y == 1:
            neuron0current = inputNeuron0.run(LOW_INPUT)[1]
            neuron1current = inputNeuron1.run(HIGH_INPUT)[1]
        elif x == 1 and y == 0:
            neuron0current = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1current = inputNeuron1.run(LOW_INPUT)[1]
        elif x == 1 and y == 1:
            neuron0current = inputNeuron0.run(HIGH_INPUT)[1]
            neuron1current = inputNeuron1.run(HIGH_INPUT)[1]

        neuron2output = middleNeuron2.run(neuron0current * weights[0] + neuron1current * weights[1])
        neuron2current = neuron2output[1]

        neuron3output = middleNeuron3.run(14 - (neuron0current * weights[2] + neuron1current * weights[3]))
        neuron3current = neuron3output[1]

        neuron4spikes = outputNeuron.run(neuron2current * weights[4] + neuron3current * weights[5])[0]
        totalSpikes += neuron4spikes

    # TESTING ONLY REMOVE LATER
    return totalSpikes
    # return totalSpikes


train()
print("Trained weights")
print(weights)

print("\nFinding spikes rates in a 100 time unit interval")
print("Expected results for a working xor network is significant spike rate difference between 0 and 1 outputs.")
print("(0, 0): " + str(test(0, 0)))
print("(0, 1): " + str(test(0, 1)))
print("(1, 0): " + str(test(1, 0)))
print("(1, 1): " + str(test(1, 1)))