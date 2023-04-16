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
    
    # Displays all instructions in memory
    def display(self):
        print("Printing Instructions from Memory\n")

        for i in range(len(self.instructions)):
            print(f"LINE {i + 1}\n{self.instructions[i]}")
            print("")