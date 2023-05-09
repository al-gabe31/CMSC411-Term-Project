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
            flag_1 = instruction.operands[0] in self.forwarding
            flag_2 = instruction.operands[1] in self.forwarding
            if (flag_1) or (flag_2):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                elif instruction.operands[0] in self.forwarding:
                    flags[0] = True # Take data from forwarding unit instead
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
                elif instruction.operands[1] in self.forwarding:
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
            flag_1 = instruction.operands[0] in self.forwarding
            flag_2 = instruction.operands[1] in self.forwarding
            if (flag_1) or (flag_2):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                elif instruction.operands[0] in self.forwarding:
                    flags[0] = True # Take data from forwarding unit instead
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
                elif instruction.operands[1] in self.forwarding:
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
            flag_1 = instruction.operands[0] in self.forwarding
            
            if flag_1:
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
            
            # If register is ready, then simply load immediate into register
            if self.EX[0].is_null() and is_ready:
                # Initialize register in forwarding unit
                if instruction.operands[0] not in self.forwarding:
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
            flag_1 = instruction.operands[0] in self.forwarding
            flag_2 = get_reg_substring(instruction.operands[1]) in self.forwarding
            
            if (flag_1) or (flag_2):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[get_reg_substring(instruction.operands[1])] == "None":
                    is_ready = False
            
            # If both registers are ready, then initialize all registers in self.forwarding
            if self.EX[0].is_null() and is_ready:
                # Initializes registers in forwarding unit
                if instruction.operands[0] not in self.forwarding:
                    self.forwarding[instruction.operands[0]] = "None"
                if get_reg_substring(instruction.operands[1]) not in self.forwarding:
                    self.forwarding[get_reg_substring(instruction.operands[1])] = "None"
        
        # REG   REG   REG
        elif instruction.op_code in ("AND", "OR", "ADD", "SUB", "MULT"):
            # First check if either registers are currently in self.forwarding
            flag_1 = instruction.operands[0] in self.forwarding
            flag_2 = instruction.operands[1] in self.forwarding
            flag_3 = instruction.operands[2] in self.forwarding
            
            if (flag_1) or (flag_2) or (flag_3):
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
                if instruction.operands[0] not in self.forwarding:
                    self.forwarding[instruction.operands[0]] = "None"
                if instruction.operands[1] not in self.forwarding:
                    self.forwarding[instruction.operands[1]] = "None"
                if instruction.operands[2] not in self.forwarding:
                    self.forwarding[instruction.operands[2]] = "None"
        
        # REG   REG   IMM
        elif instruction.op_code in ("ANDI", "ORI", "ADDI", "SUBI", "MULTI"):
            # First check if either registers are currently in self.forwarding
            flag_1 = instruction.operands[0] in self.forwarding
            flag_2 = instruction.operands[1] in self.forwarding
            
            if (flag_1) or (flag_2):
                # Forwarding not yet ready for first operand
                if flag_1 and self.forwarding[instruction.operands[0]] == "None":
                    is_ready = False
                
                # Forwarding not yet ready for second operand
                if flag_2 and self.forwarding[instruction.operands[1]] == "None":
                    is_ready = False
            
            # If all registers are ready, then initialize all registers in self.forwarding
            if self.EX[0].is_null() and is_ready:
                # Initializes registers in forwarding unit
                if instruction.operands[0] not in self.forwarding:
                    self.forwarding[instruction.operands[0]] = "None"
                if instruction.operands[1] not in self.forwarding:
                    self.forwarding[instruction.operands[1]] = "None"

        # Move instruction to the next stage (if possible)
        if self.EX[0].is_null() and is_ready:
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 1)
            
            self.EX[0] = self.ID
            self.ID = Instruction("NULL")
    
    def act_EX1(self, instruction):
        # Do something here


        # Instructions that finish here:
        #   - AND
        #   - ANDI
        #   - OR
        #   - ORI

        # Move instruction to the next stage (if possible)
        if self.EX[1].is_null():
            if instruction.op_code == "AND":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                reg3 = self.registers[get_reg_num(instruction.operands[2])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])
                
                if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                    reg3 = Register()
                    reg3.insert_data(self.forwarding[instruction.operands[2]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], bitwise_AND(reg2, reg3)))
            
            elif instruction.op_code == "ANDI":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], bitwise_ANDI(reg2, int(instruction.operands[2]))))
            
            elif instruction.op_code == "OR":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                reg3 = self.registers[get_reg_num(instruction.operands[2])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])
                
                if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                    reg3 = Register()
                    reg3.insert_data(self.forwarding[instruction.operands[2]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], bitwise_OR(reg2, reg3)))
            
            elif instruction.op_code == "ORI":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], bitwise_ORI(reg2, int(instruction.operands[2]))))
            
            self.EX[1] = self.EX[0]
            self.EX[0] = Instruction("NULL")
    
    def act_EX2(self, instruction):
        # Do something here


        # Instructions that finish here:
        #   - ADD
        #   - ADDI
        #   - SUB
        #   - SUBI

        # Move instruction to the next stage (if possible)
        if self.EX[2].is_null():
            if instruction.op_code == "ADD":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                reg3 = self.registers[get_reg_num(instruction.operands[2])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])
                
                if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                    reg3 = Register()
                    reg3.insert_data(self.forwarding[instruction.operands[2]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data + reg3.data))
            
            elif instruction.op_code == "ADDI":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data + int(instruction.operands[2])))
            
            elif instruction.op_code == "SUB":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                reg3 = self.registers[get_reg_num(instruction.operands[2])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])
                
                if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                    reg3 = Register()
                    reg3.insert_data(self.forwarding[instruction.operands[2]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data - reg3.data))
            
            elif instruction.op_code == "SUBI":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data - int(instruction.operands[2])))
            
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


        # Instructions that finish here:
        #   - MULT
        #   - MULTI

        # Move instruction to the next stage (if possible)
        if self.MEM.is_null():
            if instruction.op_code == "MULT":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                reg3 = self.registers[get_reg_num(instruction.operands[2])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])
                
                if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                    reg3 = Register()
                    reg3.insert_data(self.forwarding[instruction.operands[2]])
                
                print(f"{reg2.data * reg3.data} = {reg2.data} * {reg3.data}")

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data * reg3.data))

            elif instruction.op_code == "MULTI":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]

                # Check if forwarding is needed
                if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                    reg2 = Register()
                    reg2.insert_data(self.forwarding[instruction.operands[1]])

                # Put result into buffer
                self.buffer.append((instruction.operands[0], reg2.data * int(instruction.operands[2])))
            
            # Record exit cycle for this instruction
            self.update_stop_cycle(instruction.instruction_id, 2)
            
            self.MEM = self.EX[3]
            self.EX[3] = Instruction("NULL")
    
    def act_MEM(self, instruction):
        # Do something here


        # The only instructions that are relevant here are:
        #   - LW
        #   - SW

        # Move instruction to the next stage (if possible)
        if self.WB.is_null():
            is_ready = True
            
            if instruction.op_code == "LW":
                reg2 = self.registers[get_reg_num(instruction.operands[1])]
                mem_address = get_disp_value(instruction.operands[1]) + reg2.data
                
                # We then validate the mem_address
                if mem_address < 256 or mem_address >= 384:
                    print("ERROR IN LW - mem_address out of bounds")
                    return -1
                
                line_index = mem_address - 256 # Since data starts at address 0x100
                line_index /= 4 # Has to be word aligned
                line_index = int(line_index)

                base_data = self.data_cache.data[line_index].data_decimal
                
                # First checks if data is currentl in D-Cache
                if self.data_cache.data_in_cache(base_data) and self.data_cache.miss_cycles_left == 0:
                    # D-Cache Hit
                    # Put resulting data into buffer
                    self.buffer.append((instruction.operands[0], base_data))
                else:
                    # D-Cache Miss
                    is_ready = False
                    
                    # We then check if the processor is currently dealing with I-Cache Miss
                    if self.in_cache_miss == False and self.data_cache.miss_cycles_left == 0:
                        # If it's not, then continue with D-Cache miss protocol
                        
                        result = self.data_cache.put_data_in_cache(mem_address)

                        if result != -2:
                            self.data_cache.miss_cycles_left = 11
                            self.in_cache_miss = True

                    # If it's currently dealing with a cache miss but it's from d-cache, then simply just decrement the miss cycles left for d-cache
                    elif self.in_cache_miss == True and self.data_cache.miss_cycles_left > 0:
                        self.data_cache.miss_cycles_left -= 1
                        if self.data_cache.miss_cycles_left == 0:
                            self.in_cache_miss = False
                    
                    # If it's actually because it's waiting for I-Cache miss to resolve, then just wait
                    elif self.in_cache_miss == True and self.data_cache.miss_cycles_left == 0:
                        pass # Do nothing
                    
                    # This is just here just in case something unexpected happens
                    else:
                        print("ERROR IN LW - Uknown case happened")
            
            elif instruction.op_code == "SW":
                reg3 = self.registers[instruction.operands[0]]
                reg4 = self.registers[get_reg_num(instruction.operands[1])]
                mem_address = get_disp_value(instruction.operands[1]) + reg4

                # We then validate the mem_address
                if mem_address < 256 or mem_address >= 384:
                    print("ERROR IN SW - mem_address out of bounds")
                    return -1
                
                line_index = mem_address - 256 # Since data starts at address 0x100
                line_index /= 4 # Has to be word aligned
                line_index = int(line_index)

                base_data = self.data_cache.data[line_index].data_decimal

                if self.data_cache.data_in_cache(base_data):
                    # Data is currently located in cache and we just update it from there
                    self.data_cache.update_data_in_cache(mem_address, reg3.data)
                else:
                    # We have to get data from cache and update it from there
                    is_ready = False

                    # We then check if the processor is currently dealing with I-Cache Miss
                    if self.in_cache_miss == False and self.data_cache.miss_cycles_left == 0:
                        # If it's not, then continue with D-Cache miss protocol
                        
                        result = self.data_cache.put_data_in_cache(mem_address)

                        if result != -2:
                            self.data_cache.miss_cycles_left = 11
                            self.in_cache_miss = True
                    
                    # If it's currently dealing with a cache miss but it's from d-cache, then simply just decrement the miss cycles left for d-cache
                    elif self.in_cache_miss == True and self.data_cache.miss_cycles_left > 0:
                        self.data_cache.miss_cycles_left -= 1
                        if self.data_cache.miss_cycles_left == 0:
                            self.in_cache_miss = False
                    
                    # If it's actually because it's waiting for I-Cache miss to resolve, then just wait
                    elif self.in_cache_miss == True and self.data_cache.miss_cycles_left == 0:
                        pass # Do nothing
                    
                    # This is just here just in case something unexpected happens
                    else:
                        print("ERROR IN LW - Uknown case happened")
            
            if is_ready:
                # Record exit cycle for this instruction
                self.update_stop_cycle(instruction.instruction_id, 3)
                
                self.WB = self.MEM
                self.MEM = Instruction("NULL")
    
    def act_WB(self, instruction):
        # Do something here

        if instruction.op_code == "SW":
            # All it does is remove the registers from the forwarding unit (so long as the value in the dictionary isn't currently "None")
            if instruction.operands[0] in self.forwarding and self.forwarding[instruction.operands[0]] != "None":
                self.forwarding.pop(instruction.operands[0], None)

            if get_reg_substring(instruction.operands[1]) in self.forwarding and self.forwarding[get_reg_substring(instruction.operands[1])] != "None":
                self.forwarding.pop(get_reg_substring(instruction.operands[1]))
        
        elif instruction.op_code == "LW":
            # Basically does the same thing as SW except it also updates the register
            if instruction.operands[0] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[0])].insert_data(self.forwarding[instruction.operands[0]])

            # Remove registers from forwarding (if they aren't currently in the process of being updated again)
            if instruction.operands[0] in self.forwarding and self.forwarding[instruction.operands[0]] != "None":
                self.forwarding.pop(instruction.operands[0], None)

            if get_reg_substring(instruction.operands[1]) in self.forwarding and self.forwarding[get_reg_substring(instruction.operands[1])] != "None":
                self.forwarding.pop(get_reg_substring(instruction.operands[1]))
        
        elif instruction.op_code == "LI":
            # Updates registers
            if instruction.operands[0] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[0])].insert_data(self.forwarding[instruction.operands[0]])

            # Remove registers
            if instruction.operands[0] in self.forwarding and self.forwarding[instruction.operands[0]] != "None":
                self.forwarding.pop(instruction.operands[0], None)
        
        elif instruction.op_code in ("ADD", "SUB", "AND", "OR", "MULT"):
            # Updates registers
            if instruction.operands[0] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[0])].insert_data(self.forwarding[instruction.operands[0]])
            if instruction.operands[1] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[1])].insert_data(self.forwarding[instruction.operands[1]])
            if instruction.operands[2] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[2])].insert_data(self.forwarding[instruction.operands[2]])

            # Remove registers
            if instruction.operands[0] in self.forwarding and self.forwarding[instruction.operands[0]] != "None":
                self.forwarding.pop(instruction.operands[0], None)
            if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                self.forwarding.pop(instruction.operands[1], None)
            if instruction.operands[2] in self.forwarding and self.forwarding[instruction.operands[2]] != "None":
                self.forwarding.pop(instruction.operands[2], None)
        
        elif instruction.op_code in ("ADDI", "SUBI", "ANDI", "ORI", "BNE", "BEQ", "MULTI"):
            # Updates registers
            if instruction.operands[0] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[0])].insert_data(self.forwarding[instruction.operands[0]])
            if instruction.operands[1] in self.forwarding:
                self.registers[get_reg_num(instruction.operands[1])].insert_data(self.forwarding[instruction.operands[1]])

            # Remove registers
            if instruction.operands[0] in self.forwarding and self.forwarding[instruction.operands[0]] != "None":
                self.forwarding.pop(instruction.operands[0], None)
            if instruction.operands[1] in self.forwarding and self.forwarding[instruction.operands[1]] != "None":
                self.forwarding.pop(instruction.operands[1], None)

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
            if self.in_cache_miss == False:
                print("I-Cache Miss")
                self.inst_mem.put_instruction_in_cache(self.program_counter)
                self.inst_mem.miss_cycles_left = 9
                self.in_cache_miss = True
                self.inst_mem.num_inst_cache_hits -= 1 # Quick fix :)
            else:
                print("Waiting for D-Cache Miss to Resolve")
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
        print(f"Program Counter: {self.program_counter}")
        print(f"In Cache Miss: {self.in_cache_miss}")
        print(f"I-Cache Miss Cycles Left: {self.inst_mem.miss_cycles_left}")
        print(f"D-Cache Miss Cycles Left: {self.data_cache.miss_cycles_left}")
        print(f"Forwarding: {self.forwarding}")
        print(f"Register Values:")
        for i in range(0, 8):
            print(f"R{i} --> {self.registers[i].data}")
    
    def run(self):
        SAFETY = 75 # Prevents infinite while loop
        
        # Loading all instructions into the processor stage
        while (self.inst_mem.pc_out_of_bounds(self.program_counter) == False or self.is_all_null() == False) and self.cycle_num < SAFETY:
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