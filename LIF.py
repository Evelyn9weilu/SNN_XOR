
class LIF_Neuron():
    currCharge = 0
    def __init__(self):
        self.currCharge = 1
    def runNeuron(self, inputCharge):
        
        
        resistance = 100
        threshold = 10
        spike = 5
        C = 1

        self.currCharge += (inputCharge - (self.currCharge / resistance)) / C
        if self.currCharge  < 0:
            self.currCharge = 0
        if (self.currCharge >= threshold):
            # currCharge + spike
            # currCharge = float(0)
            self.currCharge = C
            
            return True
        return False
