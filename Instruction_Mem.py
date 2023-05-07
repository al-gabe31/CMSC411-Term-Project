# Contains the code for the Instruction_Mem class
from Instruction import *

class Instruction_Mem:
    # Takes all instructions from a text file and stores it into memory
    def __init__(self, file):
        self.instructions = []      # Contains all instructions from memory
        self.cache = [[Instruction("NULL") for j in range(4)] for i in range(4)]
        self.curr_block_destination = 0 # Current block to put instructions in
        self.program_counter = 0 # Index of current instruction
        self.miss_cycles_left = 0
        self.label_indeces = {

        }

        # IMPORTANT DATA FOR output.txt
        self.num_access_requests = 0
        self.num_inst_cache_hits = 0

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
        
        # We then need to record indeces of every label
        for i in range(len(self.instructions)):
            if self.instructions[i].label != '' and self.instructions[i].label not in self.label_indeces:
                self.label_indeces[self.instructions[i].label] = i
        
        if len(self.instructions) > 0:
            print("Successfully Loaded All Instructions")
    
    # Returns True if a specific instruction is located in cache (somewhere)
    # Returns False otherwise
    def instruction_in_cache(self, line_index):
        if line_index < 0 or line_index >= len(self.instructions):
            return False # Line Index Out Of Bounds
        
        target_instruction = self.instructions[line_index]
        values = []

        # Puts all instructions from all blocks in cache into values
        for block in self.cache:
            for instruction in block:
                values.append(instruction)
        
        return target_instruction in values
    
    # Retrieves instruction from memory and puts it into cache
    # Returns -1 for any error cases (fails to put instruction into cache)
    def put_instruction_in_cache(self, line_index):
        # We can't put instruction into cache in any of the following cases
        if line_index < 0 or line_index >= len(self.instructions):
            return -1 # Line index out of bounds
        if self.miss_cycles_left > 0:
            return -1 # Can't put during an instruction-cache miss
        
        if self.instruction_in_cache(line_index) == True:
            print("ERROR - Can't put instruction in cache if it's already there")
            return -1 # Can't put instruction into cache if it's already there

        # Adds 4 instructions into cache
        for i in range(4):
            # Index not out of range
            if line_index + i < len(self.instructions):
                stuff = ", ".join(self.instructions[line_index + i].operands)
                # idk = self.instructions[line_index + i].label + ":"
                idk = ""
                
                if self.instructions[line_index + i].label != "":
                    idk = self.instructions[line_index + i].label + ":"
                
                # self.cache[self.curr_block_destination][i] = Instruction(self.instructions[line_index + i].line)
                self.cache[self.curr_block_destination][i] = Instruction(f"{idk} {self.instructions[line_index + i].op_code} {stuff} {self.instructions[line_index + i].remarks}")

            else:
                self.cache[self.curr_block_destination][i] = Instruction("NULL")
        
        # Updates block index
        self.curr_block_destination += 1
        self.curr_block_destination %= 4
    
    # Returns true if program counter is out of bounds
    # Returns false otherwise
    def pc_out_of_bounds(self):
        return self.program_counter < 0 or self.program_counter >= len(self.instructions)
    
    # This is mostly for debugging
    # Displays all instructions in memory
    def display(self):
        print("Printing Instructions from Memory\n")

        for i in range(len(self.instructions)):
            print(f"LINE {i}\n{self.instructions[i]}")
            print("")