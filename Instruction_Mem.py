# Contains the code for the Instruction_Mem class
from Instruction import *

class Instruction_Mem:
    # Takes all instructions from a text file and stores it into memory
    def __init__(self, file):
        self.instructions = []      # Array of Instruction objects

        with open(file, "r") as file:
            # Reads the text file line by line
            while line := file.readline():
                self.instructions.append(Instruction(line))
        
        # We then need to validate each instruction
        # Deletes all instructions if any of them are invalid
        for i in range(len(self.instructions)):
            if self.instructions[i].is_valid() == False:
                print(f"Invalid Arguments @ Line {i + 1}")
                self.instructions.clear()
                break
        
        if len(self.instructions) > 0:
            print("Successfully Loaded All Instructions")
    
    # Displays all instructions in memory
    def display(self):
        print("Printing Instructions from Memory\n")

        for i in range(len(self.instructions)):
            print(f"LINE {i + 1}\n{self.instructions[i]}")
            print("")