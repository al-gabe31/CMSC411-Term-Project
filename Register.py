# Contains the code for the Register class
from Instruction import *
from Instruction_Mem import *

NUM_BITS_IN_REG = 32

class Register:
    def __init__(self):
        self.data = 0
        self.bits = [0 for i in range(NUM_BITS_IN_REG)]
    
    def insert_data(self, data):
        # First checks that the data is valid
        if isinstance(data, int) == False or data < 0 or data > pow(2, NUM_BITS_IN_REG) - 1:
            return -1 # Does nothing
        
        self.data = data
        new_data = [int(digit) for digit in bin(data)[2:]]

        while len(new_data) < NUM_BITS_IN_REG:
            new_data.insert(0, 0)
        
        self.bits = new_data
        return 0 # Success