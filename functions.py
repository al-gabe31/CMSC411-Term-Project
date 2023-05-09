# Contains useful helper functions

# Get the operand type of a string
# Returns the following:
#  0 - Register Type
#  1 - Immediate Type
#  2 - Register Displacement Type
#  3 - Label Type
# -1 - Invalid Type
def get_operand_type(operand):
    # Register Case
    if len(operand) >= 2 and operand[0].upper() == "R" and int(operand[1:len(operand)]) in range(0, 32):
        # print("Register Type")
        return 0
    
    # Positive Immediate Case
    elif len(operand) >= 1 and operand.isdigit():
        # print("Positive Immediate Type")
        return 1
    
    # Negative Immediate Case
    elif len(operand) >= 2 and operand[0] == "-" and operand[1:len(operand)].isdigit():
        # print("Negative Immediate Type")
        return 1
    
    # Hexadecimal Immediate Case
    elif len(operand) >= 2 and operand[-1].lower() == "h" and get_operand_type(operand[0:len(operand) - 1]) == 1:
        # print("Hexadecimal Immediate Case")
        return 1
    
    # Register Diplacement Case
    elif len(operand) >= 5 and (left := operand.find("(")) >= 0 and (right := operand.find(")")) >= 0 and right - left in range(3, 5) and get_operand_type(operand[0:left]) == 1 and get_operand_type(operand[left + 1: right]) == 0 and operand.count("(") == 1 and operand.count(")") == 1:
        # print("Register Displacement Type")
        return 2
    
    # Label Case
    elif operand.isalpha() == True:
        return 3
    
    # Invalid Case
    else:
        # print("Invalid Case")
        return -1

# Converts an integer into its signed 32-bit string version
def int_to_bit(value):
    returner = ""

    if value < 0:
        returner += "1"
        value += pow(2, 31)
    else:
        returner += "0"
    
    for i in range(30, -1, -1):
        if value >= pow(2, i):
            returner += "1"
            value -= pow(2, i)
        else:
            returner += "0"
    
    return returner

# Returns the register number from an operand
def get_reg_num(operand):
    # return int(operand[1:])

    # Register Type Case
    if get_operand_type(operand) == 0:
        return int(operand[1:])

    # Displacement Type Case
    elif get_operand_type(operand) == 2:
        left_index = operand.index("(")
        right_index = operand.index(")")
        return int(operand[left_index + 2: right_index])

    # Error Case
    return -1

# Gets only the substring containing the register and number in a displacement operand
def get_reg_substring(disp_operand):
    if get_operand_type(disp_operand) == 2:
        left_index = disp_operand.index("(")
        right_index = disp_operand.index(")")
        return disp_operand[left_index + 1: right_index]
    
    return ""

def get_disp_value(operand):
    if get_operand_type(operand) == 2:
        # Valid input
        
        left_index = operand.index("(")
        
        return int(operand[:left_index])
    
    else:
        return None