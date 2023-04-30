from functions import *
from Instruction_Mem import *
from Processor import *

# p1 = Processor("inst.txt")
# print(p1.is_all_null())
# p1.run()

registers = [Register() for i in range(32)]
registers[0].insert_data(65537)
print(registers[0].data)
print(registers[0].bits)