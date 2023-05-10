import sys
from Processor import *

p1 = Processor(str(sys.argv[1]), str(sys.argv[2]))
p1.run()
print("Simulation Finished ~ Check output.txt file")

print("EXITED WITHOUT ERROR")