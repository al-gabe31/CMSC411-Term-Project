from functions import *
from Instruction_Mem import *
from Processor import *

p1 = Processor("inst.txt")
# print(p1.is_all_null())
p1.run()