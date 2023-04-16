# Contains the code for the Instruction class

# List of all supported instructions
INSTRUCTION_TYPES = ['LW', 'SW', 'LI', 'ADD', 'ADDI', 'MULT', 'MULTI', 'SUB', 'SUBI', 'AND', 'ANDI', 'OR', 'ORI', 'BEQ', 'BNE', 'J', 'HLT']

# Maps the instruction to the number of clock cycles it'll take in the EX phase
NUM_CYCLES = {
    'J': 0,
    'BEQ': 0,
    'BNE': 0,
    'LI': 0,
    'AND': 1,
    'ANDI': 1,
    'OR': 1,
    'ORI': 1,
    'LW': 1,
    'SW': 1,
    'LI': 1,
    'ADD': 2,
    'ADDI': 2,
    'SUB': 2,
    'SUBI': 2,
    'MULT': 4,
    'MULTI': 4
}

class Instruction:
    # Accepts a string as input
    # Parses the string and assigns the correct values for label, op_code, operands, and remarks
    def __init__(self, line):
        # Attributes
        self.label = None           # String
        self.op_code = None         # String
        self.operands = None        # Array of String
        self.remarks = None         # String

        # Index     Cycle Stage
        # 0         IF
        # 1         ID
        # 2         EX1
        # 3         EX2
        # 4         EX3
        # 5         EX4
        # 6         MEM
        # 7         WB
        self.cycle_stops = [-1, -1, -1, -1, -1, -1, -1, -1]

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
            self.operands.append(adding.pop(0).upper())
        
        # Dealing with Remarks
        self.remarks = " ".join(adding)
    
    def __str__(self):
        return f"LABEL: {self.label}\nOP CODE: {self.op_code}\nOPERANDS: {self.operands}\nREMARKS: {self.remarks}"