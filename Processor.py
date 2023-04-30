# Contains the code for the Processor class
from Instruction import *
from Instruction_Mem import *

class Processor:
    def __init__(self, file):
        self.inst_mem = Instruction_Mem(file)

        self.IF = Instruction("NULL")                          # Instruction in Instruction Fetch stage
        self.ID = Instruction("NULL")                          # Instruction in Instruction Decode stage
        self.EX = [Instruction("NULL") for i in range(4)]      # Instruction in Execute stage (an array of Instruction objects of size 4)
        self.MEM = Instruction("NULL")                         # Instruction in Memory stage
        self.WB = Instruction("NULL")                          # Instruction in Write Back stage

        self.registers = [None for i in range(32)]
    
    def is_all_null(self):
        return self.IF.is_null() and self.ID.is_null() and self.EX[0].is_null() and self.EX[1].is_null() and self.EX[2].is_null() and self.EX[3].is_null() and self.MEM.is_null() and self.WB.is_null()
    
    # Shifts all Instructions to their next stage
    def shift(self):
        self.WB = self.MEM

        # Execute stages of the processor (can get kinda tricky)
        self.MEM = self.EX[3]
        self.EX[3] = self.EX[2]
        self.EX[2] = self.EX[1]
        self.EX[1] = self.EX[0]
        self.EX[0] = self.ID
        
        self.ID = self.IF

        if len(self.inst_mem.instructions) > 0:
            self.IF = self.inst_mem.instructions.pop(0)
        else:
            self.IF = Instruction("NULL")
    
    def display_curr_state(self):
        print(f"IF --> {self.IF.line}")
        print(f"ID --> {self.ID.line}")
        print(f"EX1 --> {self.EX[0].line}")
        print(f"EX2 --> {self.EX[1].line}")
        print(f"EX3 --> {self.EX[2].line}")
        print(f"EX4 --> {self.EX[3].line}")
        print(f"MEM --> {self.MEM.line}")
        print(f"WB --> {self.WB.line}")
    
    def run(self):
        cycle_num = 1
        
        # Loading all instructions into the processor stage
        while len(self.inst_mem.instructions) > 0 or self.is_all_null() == False:
            print(f"CYCLE {cycle_num}")
            self.shift()
            self.display_curr_state()
            cycle_num += 1
            print("")
        
        # Finishing all instructions in the processor stage