import sys
from functions import *
from Instruction_Mem import *
from Processor import *
from Data import *
from Data_Cache import *

print(f"Number of arguments passed {len(sys.argv)}")
print(f"Stuff {str(sys.argv[1])}")

p1 = Processor(str(sys.argv[1]), str(sys.argv[2]))
p1.run()

print("EXITED WITHOUT ERROR")