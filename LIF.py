
class LIF_Neuron():

    # constant LIF properties
    # baseline charge when neuron is fully neutral
    baseCharge = 1
    # membrane capacitance
    C = 1
    # time interval for our neuron, based on neuron firing 200 times per sec
    dt = 1
    # neuron resistance
    resistance = 12
    # spiking threshold
    threshold = 10
    # additional charge that results from passing threshold
    spike = 5

    # dynamic LIF variables
    inputCharge = 0
    currentCharge = baseCharge

    # Constructor takes in initial input charge
    def __init__(self, current):
        self.inputCharge = current

    # Every call using .start() or next() will update the neuron charge
    # Neuron will check if it should spike
    # If it has spiked, we yield a 1 and the current charge plus spike
    # otherwise we yield a 0 and the baseline charge
    def start(self):

        # add dV to current charge, dv based on input charge and leak
        self.currentCharge += self.dt * (self.inputCharge - (self.currentCharge / self.resistance)) / self.C

        # Check if we have reached the threshold
        if self.currentCharge >= self.threshold:
            # resetting charge and spiking
            self.currentCharge = self.baseCharge
            yield (1, self.currentCharge + self.spike)
        else:


            # IF THIS DOESN'T WORK, TRY OUTPUTTING 90% OF THE PREVIOUS OUTPUT

            yield (0, self.baseCharge)
