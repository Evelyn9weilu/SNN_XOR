from LIF import LIF_Neuron
import numpy as np
import math


inputNeuron = [LIF_Neuron()] * 2
middleNeuron = [LIF_Neuron()] * 4

outputNeuron = LIF_Neuron()
alpha = .001
decay = .00001
weights = np.random.random(12)



# High input = 1 ???
# Low input <= .5 ???
lowInput = 2
highInput = 7
inputs = [.35] *2
def train():
    

    for k in range (4):
        if (k == 0):
            inputs[0] = lowInput
            inputs[1] = highInput
            trainingInput= 1000
        if (k == 1):
            inputs[0] = highInput
            inputs[1] = lowInput
            trainingInput= 1000
        if (k == 2):
            inputs[0] = lowInput
            inputs[1] = lowInput
            trainingInput = -50
        if (k == 3):
            inputs[0] = highInput
            inputs[1] = highInput
            trainingInput = -50
   
        
        for i in range(3000):
            
            # outputNeuron.runNeuron(trainingInput)
            for j in range (len(inputNeuron)):
                
                if ((inputNeuron[j].runNeuron(inputs[j]))):
                    
                    nextInput = 1
                else:
                    nextInput = 0
                for i in range (len(middleNeuron)):
                    if (middleNeuron[i].runNeuron(nextInput * weights[j*4 + i])):
                        
                        #strengthen weights here
                        weights[j*4 + i] += (alpha * weights[j*4 + i]) - decay 
                        toOutput = 1
                    else:
                        weights[j*4 + i] -= decay 
                        toOutput = 0
                    if (outputNeuron.runNeuron(trainingInput * weights[i+8] + (toOutput * weights[i + 8]))):
                        
                        weights[i+8] += (alpha * weights[i+8]) - decay 
                    else:
                        weights[i+8] -= decay 


def test(x,y):
    neuron1Fires = 0
    neuron2Fires = 0
    totalFires = 0
    if x == 0:
        input0 = lowInput
    else:
        input0 = highInput
    if y == 0:
        input1 = lowInput
    else:
        input1 = highInput
    for i in range(500):
        
        if (inputNeuron[0].runNeuron(input0)):
            nextInput = 1
        else:
            nextInput = 0
        for i in range (len(middleNeuron)):
            if (middleNeuron[i].runNeuron(nextInput * weights[i])):
                toOutput = 1
            else:
                toOutput = 0
            if (outputNeuron.runNeuron(toOutput * weights[i + 8])):
                totalFires+=1
        if (inputNeuron[1].runNeuron(input0)):
            nextInput = 1
        else:
            nextInput = 0
        for i in range (len(middleNeuron)):
            if (middleNeuron[i].runNeuron(nextInput * weights[i+4])):
                toOutput = 1
            else:
                toOutput = 0
            if (outputNeuron.runNeuron(toOutput * weights[i + 8])):
                totalFires+=1
    
    return totalFires
train()
print(weights)
print(test(0,0))
print(test(0,1))
print(test(1,0))
print(test(1,1))


# from LIF import LIF_Neuron
# import numpy as np
# import math

# # 2 input neurons, 1 for first num and another for second num
# inputNeuron = [LIF_Neuron()] * 2

# # 2 hidden neurons, one representing or and one representing nand
# middleNeuron = [LIF_Neuron()] * 2

# # 1 output neuron, fires high if XOR, fires low if !XOR
# trainingNeuron = LIF_Neuron()
# outputNeuron = LIF_Neuron()

# weights = np.random.random(6)
# print(weights)


# # High input = 1 ???
# # Low input <= .5 ???
# lowInput = .35
# highInput = 1

# def train(input):
#     for i in range(1000):
#         if (input == (0,0)):
#             inputNeuron[0].runNeuron(lowInput)
#             inputNeuron[1].runNeuron(lowInput)
#         if (input == (0,1)):
#             inputNeuron[0].runNeuron(lowInput)
#             inputNeuron[1].runNeuron(highInput)
#         if (input == (1,0)):
#             inputNeuron[0].runNeuron(highInput)
#             inputNeuron[1].runNeuron(lowInput)
#         if (input == (1,1)):
#             inputNeuron[0].runNeuron(highInput)
#             inputNeuron[1].runNeuron(highInput) 
            
# # Things to figure out
# # How to tell if two neurons are firing at the same time

# # Brain Damage's result for (0,0), (0,1), (1,0), (1,1)
# (0, 296, 184)
# (28, 294, 190)
# (27, 294, 190)
# (66, 265, 185)