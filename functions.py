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