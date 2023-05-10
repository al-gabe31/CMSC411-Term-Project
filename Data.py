from functions import *

# Contains the code for the Data class

class Data:
    # Accepts a 32 long string as input as 1's and 0's
    def __init__(self, line = "0" * 32):
        # Attributes
        self.data_string = "0" * 32
        self.data_binary = [0 for i in range(32)]
        self.data_decimal = 0

        # First, validate input
        if len(line) == 32 and line.count("0") + line.count("1") == 32:
            self.data_string = line

            # Gets binary version of string
            for i in range(32):
                self.data_binary[i] = int(line[i])
            
            # Gets decimal version of string
            self.data_decimal -= pow(2, 31) * self.data_binary[0]
            for i in range(30, -1, -1):
                self.data_decimal += pow(2, i) * self.data_binary[31 - i]
                
        elif len(line) != 32:
            pass
        elif actual_count := line.count("0") + line.count("1") != 32:
            pass
    
    # Updates the values stored inside a Data object
    def update(self, new_value):
        self.data_string = int_to_bit(new_value)
        self.data_binary = [int(bit) for bit in self.data_string]
        self.data_decimal = new_value
    
    # Checks for equality between 2 Data objects
    def __eq__(self, otherData):
        return self.data_decimal == otherData.data_decimal