# Contains the code for the Processor class
from Instruction import *
from Instruction_Mem import *
from Register import *
from Data import *
from Data_Cache import *
from copy import *

class Processor:
    def __init__(self, inst_file, data_file):
        self.cycle_num = 1
        self.instructions = [] # Array of Instructions that the processor had to process
        
        # I know the naming scheme is inconsistent... but just stick with it for now TT_TT
        self.inst_mem = Instruction_Mem(inst_file)
        self.data_cache = Data_Cache(data_file)

        self.in_cache_miss = False

        self.program_counter = 0 # Keeps track of which instruction we're on

        self.HLT_ID = False # Records if a HLT instruction has passed the ID stage

        self.forwarding = {

        } # Maps Registers to values
        self.buffer = [] # Array of tuples that will add to self.forwarding at the start of the next cycle

        self.IF = Instruction("NULL")                          # Instruction in Instruction Fetch stage
        self.ID = Instruction("NULL")                          # Instruction in Instruction Decode stage
        self.EX = [Instruction("NULL") for i in range(4)]      # Instruction in Execute stage (an array of Instruction objects of size 4)
        self.MEM = Instruction("NULL")                         # Instruction in Memory stage
        self.WB = Instruction("NULL")                          # Instruction in Write Back stage

        self.registers = [Register() for i in range(32)]
    
    def is_all_null(self):
        return self.IF.is_null() and self.ID.is_null() and self.EX[0].is_null() and self.EX[1].is_null() and self.EX[2].is_null() and self.EX[3].is_null() and self.MEM.is_null() and self.WB.is_null()
    
    def act_IF(self, instruction):
        # Do something here
        if instruction.is_null() == False:
            print("Accessing from I-Cache")
            self.inst_mem.num_access_requests += 1

        # Move instruction to the next stage (if possible)
        if self.ID.is_null() and self.inst_mem.miss_cycles_left == 0:
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 0)
            
            self.ID = self.IF
            self.IF = Instruction("NULL")
    
    def act_ID(self, instruction):
        # Do something here
        is_ready = True # Determines if an instruction is ready for the next stage

        # Special Cases for ID Stage:
        #   - J
        #   - BEQ
        #   - BNE
        #   - LI
        #   - HLT
        # Everything else just puts things into the forwarding buffer
        if instruction.op_code == "J":
            self.program_counter = self.inst_mem.label_indeces[instruction.label]

            # Don't forget to clear the IF stage and remove this instruction from the pipeline
            self.IF = Instruction("NULL")
            self.update_stop_cycle(instruction.instruction_id, 1)
            self.ID = Instruction("NULL")
        
        elif instruction.op_code == "BEQ":
            flags = [False, False]
            
            # First checks if either registers are currently in self.forwarding
            if (flag_1 := instruction.operands[0] in self.forwarding) or (flag_2 := instruction.operands[1] in self.forwarding):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                else:
                    flags[0] = True # Take data from forwarding unit instead
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
                else:
                    flags[1] = True # Take data from forwarding unit instead
            
            # If both registers are ready, then check for "equal"
            if is_ready:
                reg1 = self.registers[get_reg_num(instruction.operands[0])]
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                if flags[0] == True:
                    reg1 = Register()
                    reg1.insert_data(self.forwarding[instruction.operands[0]])
                
                if flags[1] == True:
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                if reg1 == reg2:
                    # Take branch
                    self.program_counter = self.inst_mem.label_indeces[instruction.label]
                
                # Don't forget to clear the IF stage and remove this instruction from the pipeline
                self.IF = Instruction("NULL")
                self.update_stop_cycle(instruction.instruction_id, 1)
                self.ID = Instruction("NULL")
        
        elif instruction.op_code == "BNE":
            flags = [False, False]
            
            # First checks if either registers are currently in self.forwarding
            if (flag_1 := instruction.operands[0] in self.forwarding) or (flag_2 := instruction.operands[1] in self.forwarding):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                else:
                    flags[0] = True # Take data from forwarding unit instead
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
                else:
                    flags[1] = True # Take data from forwarding unit instead
            
            # If both registers are ready, then check for "not equal"
            if is_ready:
                reg1 = self.registers[get_reg_num(instruction.operands[0])]
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                if flags[0] == True:
                    reg1 = Register()
                    reg1.insert_data(self.forwarding[instruction.operands[0]])
                
                if flags[1] == True:
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                if reg1 != reg2:
                    # Take branch
                    self.program_counter = self.inst_mem.label_indeces[instruction.label]
                
                # Don't forget to clear the IF stage and remove this instruction from the pipeline
                self.IF = Instruction("NULL")
                self.update_stop_cycle(instruction.instruction_id, 1)
                self.ID = Instruction("NULL")
        
        elif instruction.op_code == "LI":
            # First checks if register is currently in self.forwarding
            if flag_1 := instruction.operands[0] in self.forwarding:
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
            
            # If register is ready, then simply load immediate into register
            if self.EX[0].is_null() and is_ready:
                # Initialize register in forwarding unit
                self.forwarding[instruction.operands[0]] = "None"

                # Puts resulting data into buffer
                self.buffer.append((instruction.operands[0], int(instruction.operands[1])))
        
        elif instruction.op_code == "HLT":
            self.HLT_ID = True

            self.update_stop_cycle(instruction.instruction_id, 1)

            # HLT instruction doesn't get to continue to the next stage
            self.ID = Instruction("NULL")
        
        
        # Every other other instruction just has to check if all registers involved in the instruction are currently in the forwarding unit

        # REG   DISP
        elif instruction.op_code in ("LW", "SW"):
            # First check if either registers are currently in self.forwarding
            if (flag_1 := instruction.operands[0] in self.forwarding) or (flag_2 :=  get_reg_substring(instruction.operands[1]) in self.forwarding):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[get_reg_substring(instruction.operands[1])] == "None":
                    is_ready = False
            
            # If both registers are ready, then initialize all registers in self.forwarding
            if self.EX[0].is_null() and is_ready:
                # Initializes registers in forwarding unit
                self.forwarding[instruction.operands[0]] = "None"
                self.forwarding[get_reg_substring(instruction.operands[1])] = "None"
        
        # REG   REG   REG
        elif instruction.op_code in ("AND", "OR", "ADD", "SUB", "MULT"):
            # First check if either registers are currently in self.forwarding
            if (flag_1 := instruction.operands[0] in self.forwarding) or (flag_2 := instruction.operands[1] in self.forwarding) or (flag_3 := instruction.operands[2] in self.forwarding):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for third operand
                if flag_3 and self.forwarding[instruction.operands[2]] == "None":
                    is_ready = False
            
            # If all registers are ready, then initialize all registers in self.forwarding
            if self.EX[0].is_null() and is_ready:
                # Initializes registers in forwarding unit
                self.forwarding[instruction.operands[0]] = "None"
                self.forwarding[instruction.operands[1]] = "None"
                self.forwarding[instruction.operands[2]] = "None"
        
        # REG   REG   IMM
        elif instruction.op_code in ("ANDI", "ORI", "ADDI", "SUBI", "MULTI"):
            # First check if either registers are currently in self.forwarding
            if (flag_1 := instruction.operands[0] in self.forwarding) or (flag_2 := instruction.operands[1] in self.forwarding):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
            
            # If all registers are ready, then initialize all registers in self.forwarding
            if self.EX[0].is_null() and is_ready:
                # Initializes registers in forwarding unit
                self.forwarding[instruction.operands[0]] = "None"
                self.forwarding[instruction.operands[1]] = "None"

        # Move instruction to the next stage (if possible)
        if self.EX[0].is_null() and is_ready:
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 1)
            
            self.EX[0] = self.ID
            self.ID = Instruction("NULL")
    
    def act_EX1(self, instruction):
        # Do something here

        # Move instruction to the next stage (if possible)
        if self.EX[1].is_null():
            self.EX[1] = self.EX[0]
            self.EX[0] = Instruction("NULL")
    
    def act_EX2(self, instruction):
        # Do something here

        # Move instruction to the next stage (if possible)
        if self.EX[2].is_null():
            self.EX[2] = self.EX[1]
            self.EX[1] = Instruction("NULL")
    
    def act_EX3(self, instruction):
        # Do something here

        # Move instruction to the next stage (if possible)
        if self.EX[3].is_null():
            self.EX[3] = self.EX[2]
            self.EX[2] = Instruction("NULL")
    
    def act_EX4(self, instruction):
        # Do something here

        # Move instruction to the next stage (if possible)
        if self.MEM.is_null():
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 2)
            
            self.MEM = self.EX[3]
            self.EX[3] = Instruction("NULL")
    
    def act_MEM(self, instruction):
        # Do something here

        # Move instruction to the next stage (if possible)
        if self.WB.is_null():
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 3)
            
            self.WB = self.MEM
            self.MEM = Instruction("NULL")
    
    def act_WB(self, instruction):
        # Do something here

        # Remove instruction from the pipeline
        # Record exit cycle for this instruction
        self.update_stop_cycle(instruction.instruction_id, 4)
        
        self.WB = Instruction("NULL")
    
    # Shifts all Instructions to their next stage
    def shift(self):
        # self.WB = self.MEM

        # # Execute stages of the processor (can get kinda tricky)
        # self.MEM = self.EX[3]
        # self.EX[3] = self.EX[2]
        # self.EX[2] = self.EX[1]
        # self.EX[1] = self.EX[0]
        # self.EX[0] = self.ID
        
        # self.ID = self.IF

        self.act_WB(self.WB)
        self.act_MEM(self.MEM)
        self.act_EX4(self.EX[3])
        self.act_EX3(self.EX[2])
        self.act_EX2(self.EX[1])
        self.act_EX1(self.EX[0])
        self.act_ID(self.ID)
        self.act_IF(self.IF)

        # if len(self.inst_mem.instructions) > 0:
        #     self.IF = self.inst_mem.instructions.pop(0)
        # else:
        #     self.IF = Instruction("NULL")

        if self.inst_mem.miss_cycles_left > 0:
            print("I-Cache Miss STALL")
            self.inst_mem.miss_cycles_left -= 1
            if self.inst_mem.miss_cycles_left == 0:
                self.in_cache_miss = False
        elif self.inst_mem.pc_out_of_bounds(self.program_counter) == False and self.inst_mem.instruction_in_cache(self.program_counter) == True:
            print("I-Cache Hit!")
            self.inst_mem.num_inst_cache_hits += 1
            self.IF = deepcopy(self.inst_mem.instructions[self.program_counter])
            self.IF.instruction_id = self.cycle_num
            self.instructions.append(self.IF)
            self.program_counter += 1
        elif self.inst_mem.pc_out_of_bounds(self.program_counter) == False and self.inst_mem.instruction_in_cache(self.program_counter) == False:
            print("I-Cache Miss")
            self.inst_mem.put_instruction_in_cache(self.program_counter)
            self.inst_mem.miss_cycles_left = 9
            self.in_cache_miss = True
            self.inst_mem.num_inst_cache_hits -= 1 # Quick fix :)
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
        SAFETY = 200 # Prevents infinite while loop
        
        # Loading all instructions into the processor stage
        while self.inst_mem.pc_out_of_bounds(self.program_counter) == False or self.is_all_null() == False and self.cycle_num < SAFETY:
            print(f"CYCLE {self.cycle_num}")

            # Gets all tuples currently in self.buffer and puts it into self.forwarding
            while(len(self.buffer) > 0):
                self.forwarding[self.buffer[0][0]] = self.buffer[0][1]
                self.buffer.pop(0)
            self.shift()
            self.display_curr_state()
            self.cycle_num += 1
            print("")
        
        # Finishing all instructions in the processor stage
    
    # Returns the index of a specific instruction by instruction_id in self.instructions
    # Returns -1 if instruction_id not in self.instructions
    def locate_instruction_id(self, instruction_id):
        # Goes through the entire self.instructions array looking for the matching instruction_id
        for i in range(len(self.instructions)):
            if self.instructions[i].instruction_id == instruction_id:
                return i
            
        # If it hasn't found it at this point, return -1
        return -1 # instruction_id not in self.instructions for whatever reason

    # Updates the stop cycle of an instrution by instruction_id
    def update_stop_cycle(self, instruction_id, cycle_num):
        index = self.locate_instruction_id(instruction_id)
        if index in range(len(self.instructions)):
            self.instructions[index].cycle_stops[cycle_num] = self.cycle_num