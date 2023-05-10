import sys
from functions import *
from Instruction_Mem import *
from Processor import *
from Data import *
from Data_Cache import *

p1 = Processor(str(sys.argv[1]), str(sys.argv[2]))
p1.run()
print("Simulation Finished ~ Check output.txt file")

print("EXITED WITHOUT ERROR")