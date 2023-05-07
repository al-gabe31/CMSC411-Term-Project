from functions import *

# Contains the code for the Instruction class

# List of all supported instructions
INSTRUCTION_TYPES = ['LW', 'SW', 'LI', 'ADD', 'ADDI', 'MULT', 'MULTI', 'SUB', 'SUBI', 'AND', 'ANDI', 'OR', 'ORI', 'BEQ', 'BNE', 'J', 'HLT']

# Maps the instruction to the number of clock cycles it'll take in the EX phase
NUM_CYCLES = {
    'J': 0,
    'BEQ': 0,
    'BNE': 0,
    'AND': 1,
    'ANDI': 1,
    'OR': 1,
    'ORI': 1,
    'LW': 1,
    'SW': 1,
    'LI': 0,
    'ADD': 2,
    'ADDI': 2,
    'SUB': 2,
    'SUBI': 2,
    'MULT': 4,
    'MULTI': 4,
    'HLT': 0,
    'NULL': 4
}

# Operand Type:
#   0 - Register Type               Reg
#   1 - Immediate Type              Imm
#   2 - Register Displacement Type  Disp
#   3 - Label Type                  Labl
INSTRUCTION_FORMAT = {
    'LW': [0, 2],       # Reg   Disp
    'SW': [0, 2],       # Reg   Disp
    'LI': [0, 1],       # Reg   Imm
    'ADD': [0, 0, 0],   # Reg   Reg     Reg
    'ADDI': [0, 0, 1],  # Reg   Reg     Imm
    'SUB': [0, 0, 0],   # Reg   Reg     Reg
    'SUBI': [0, 0, 1],  # Reg   Reg     Imm
    'AND': [0, 0, 0],   # Reg   Reg     Reg
    'ANDI': [0, 0, 1],  # Reg   Reg     Imm
    'OR': [0, 0, 0],    # Reg   Reg     Reg
    'ORI': [0, 0, 1],   # Reg   Reg     Imm
    'J': [3],           # Labl
    'BNE': [0, 0, 3],   # Reg   Reg     Labl
    'BEQ': [0, 0, 3],   # Reg   Reg     Labl
    'MULT': [0, 0, 0],  # Reg   Reg     Reg
    'MULTI': [0, 0, 1],  # Reg   Reg     Imm
    'HLT': []
}

class Instruction:
    # Accepts a string as input
    # Parses the string and assigns the correct values for label, op_code, operands, and remarks
    def __init__(self, line):
        # Attributes
        self.line = ""
        
        self.label = None           # String
        self.op_code = None         # String
        self.operands = None        # Array of String
        self.remarks = None         # String

        # Index     Cycle Stage
        # 0         IF
        # 1         ID
        # 2         EX4
        # 3         MEM
        # 4         WB
        self.cycle_stops = [-1, -1, -1, -1, -1]

        self.instruction_id = -1 # Helps differentiate between multiple clones of the same instruction

        # Parsing command starts here
        if line.find('\n') != -1: # Removes the '\n' at the end if it has one
            line = line[:line.find('\n')]
        adding = line.split(' ')
        adding = [i for i in adding if i != '']

        # Dealing with Label
        if adding[0].find(':') > 0: # Line has label
            self.label = adding[0][0:adding[0].find(':')].upper()
            adding.pop(0)
        else:
            self.label = ''
        
        # Dealing with OP Code
        self.op_code = adding.pop(0).upper()

        # Dealing with Operands
        self.operands = []
        while len(adding) > 0 and adding[0] != '#':
            self.operands.append(adding.pop(0).upper().replace(',', ''))
        
        # Dealing with Remarks
        self.remarks = " ".join(adding)

        self.line = f"{self.label} {self.op_code} {self.operands} {self.remarks}"
    
    # Checks if an Instruction is a valid one
    def is_valid(self):
        # Checks if OP Code is valid
        if self.op_code not in INSTRUCTION_TYPES:
            return False
        
        # Checks if operand(s) are valid
        if len(self.operands) != len(INSTRUCTION_FORMAT[self.op_code]):
            return False
        
        for i in range(len(self.operands)):
            if get_operand_type(self.operands[i]) != INSTRUCTION_FORMAT[self.op_code][i]:
                return False
        
        return True

    def is_null(self):
        return self.op_code == "NULL"
    
    def __str__(self):
        return f"LABEL: {self.label}\nOP CODE: {self.op_code}\nOPERANDS: {self.operands}\nREMARKS: {self.remarks}"
    
    def __eq__(self, otherInstruction):
        if len(self.operands) != len(otherInstruction.operands):
            return False
        
        for i in range(len(self.operands)):
            if self.operands[i] != otherInstruction.operands[i]:
                return False
            
        # if self.label != otherInstruction.label:
        #     # print(f"{self.label} != {otherInstruction.label}")
        #     print("FLAG 1")
        # if self.op_code != otherInstruction.op_code:
        #     print("FLAG 2")
        # if self.remarks != otherInstruction.remarks:
        #     print("FLAG 3")
        
        # print(f"{self.operands}\t{otherInstruction.operands}")
        
        return self.label == otherInstruction.label and self.op_code == otherInstruction.op_code and self.remarks == otherInstruction.remarks