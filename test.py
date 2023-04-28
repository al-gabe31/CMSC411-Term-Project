from functions import *
from Instruction_Mem import *



# Testing Register Case
# print(get_operand_type("R1") == 0)
# print(get_operand_type("R6") == 0)
# print(get_operand_type("r20") == 0)
# print(get_operand_type("R-1") == -1) # Error Case
# print(get_operand_type("R0") == 0)
# print(get_operand_type("R32") == -1) # Error Case
# print(get_operand_type("100h") == 1)
# print(get_operand_type("-2h") == 1)
# print(get_operand_type("20H") == 1)
# print(get_operand_type("12h0") == -1) # Error Case
# print(get_operand_type("h12") == -1) # Error Case

# print(get_operand_type("5") == 1)
# print(get_operand_type("30") == 1)
# print(get_operand_type("101") == 1)
# print(get_operand_type("-3") == 1)
# print(get_operand_type("-1") == 1)
# print(get_operand_type("0") == 1)

# print(get_operand_type("5(R0)") == 2)
# print(get_operand_type("-3(r20)") == 2)
# print(get_operand_type("5)R0(") == -1) # Invalid Case
# print(get_operand_type("5((R0))") == -1) # Invalid Case
# print(get_operand_type("5(R0)()") == -1) # Invalid Case
# print(get_operand_type("5(R0") == -1) # Invalid Case
# print(get_operand_type("5RO)") == -1) # Invalid Case
# print(get_operand_type("5h(R0)") == 2)
# print(get_operand_type("(R0)5") == -1) # Invalid Case

# print(get_operand_type("LOOP") == 3)
# print(get_operand_type("LOOP0:") == -1) # Invalid Case
# print(get_operand_type("LO$OP") == -1) # Invalid Case

print("EXITED WITHOUT ERROR")