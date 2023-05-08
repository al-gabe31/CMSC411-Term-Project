# Contains the code for the Register class
from Instruction import *
from Instruction_Mem import *

NUM_BITS_IN_REG = 32

class Register:
    def __init__(self):
        self.data = 0
        self.bits = [0 for i in range(NUM_BITS_IN_REG)]
    
    # Updates the data stored into the register
    # Returns 0 on success
    # Returns -1 on failure
    def insert_data(self, data):
        # First checks that the data is valid
        if isinstance(data, int) == False or data < -1 * pow(2, NUM_BITS_IN_REG) or data > pow(2, NUM_BITS_IN_REG) - 1:
            return -1 # Does nothing
        
        self.data = data
        
        if data >= 0:
            new_data = [int(digit) for digit in bin(data)[2:]]
    
            while len(new_data) < NUM_BITS_IN_REG:
                new_data.insert(0, 0)
            
            self.bits = new_data
        else:
            self.bits[0] = 1
            data += pow(2, 31)
            
            for i in range(1, 32):
                if data >= pow(2, 31 - i):
                    self.bits[i] = 1
                    data -= pow(2, 31 - i)
        return 0 # Success

    def __eq__(self, otherRegister):
        return self.data == otherRegister.data

# Returns value from a bitwise AND
def bitwise_AND(reg1, reg2):
    bits = [0 for i in range(NUM_BITS_IN_REG)]
    
    for i in range(NUM_BITS_IN_REG):
        if reg1.bits[i] == 1 and reg2.bits[i] == 1:
            bits[i] = 1
    
    value = 0
    
    if bits[0] == 1:
        value -= pow(2, NUM_BITS_IN_REG - 1)
    
    for i in range(1, NUM_BITS_IN_REG):
        if bits[i] == 1:
            value += pow(2, NUM_BITS_IN_REG - i - 1)
    
    return value

# Returns value from a bitwise ANDI
def bitwise_ANDI(reg1, immediate):
    reg2 = Register()
    reg2.insert_data(immediate)
    
    return bitwise_AND(reg1, reg2)

# Returns value from a bitwise OR
def bitwise_OR(reg1, reg2):
    bits = [0 for i in range(NUM_BITS_IN_REG)]
    
    for i in range(NUM_BITS_IN_REG):
        if reg1.bits[i] == 1 or reg2.bits[i] == 1:
            bits[i] = 1
    
    value = 0
    
    if bits[0] == 1:
        value -= pow(2, NUM_BITS_IN_REG - 1)
    
    for i in range(1, NUM_BITS_IN_REG):
        if bits[i] == 1:
            value += pow(2, NUM_BITS_IN_REG - i - 1)
    
    return value

# Returns value from a bitwise ORI
def bitwise_ORI(reg1, immediate):
    reg2 = Register()
    reg2.insert_data(immediate)
    
    return bitwise_OR(reg1, reg2)