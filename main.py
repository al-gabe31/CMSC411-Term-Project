from functions import *
from Instruction_Mem import *
from Processor import *
from Data import *
from Data_Cache import *

# TESTING Data_Cache

# data = []
# with open("data.txt", "r") as file:
#     while line := file.readline():
#         data.append(Data(line[0:32]))

# for stuff in data:
#     print(stuff.data_decimal)

# d1 = Data("00000000000000000000000000000010")
# print(d1.data_string)
# print(d1.data_binary)
# print(d1.data_decimal)

# dc1 = Data_Cache("data.txt")
# dc1.print_all_data()
# print("\n\n")
# if dc1.put_data_in_cache(256) != -1:
#     values = [i.data_decimal for i in dc1.cache["set0"][0]]
#     print(values)
#     print(dc1.lru_indeces[0])
# if dc1.update_data_in_cache(260, 5) != 1:
#     values = [i.data_decimal for i in dc1.cache["set0"][0]]
#     print(values)
#     print(dc1.lru_indeces[0])
# dc1.write_back_to_mem()
# if dc1.put_data_in_cache(256 + (0 * 4)) != -1:
#     values = [i.data_decimal for i in dc1.cache["set0"][1]]
#     print(values)
#     print(dc1.lru_indeces[0])
# if dc1.put_data_in_cache(256 + (16 * 4)) != -1:
#     values = [i.data_decimal for i in dc1.cache["set0"][0]]
#     print(values)
#     print(dc1.lru_indeces[0])



# TESTING Processor

p1 = Processor("inst.txt", "data.txt")
p1.run()
# p1.inst_mem.display()
# p1.data_cache.print_all_data()
print(f"Total requests for I-Cache --> {p1.inst_mem.num_access_requests}")
print(f"Number of I-Cache hits --> {p1.inst_mem.num_inst_cache_hits}")
print("\n\n")
for instruction in p1.instructions:
    print(f"Instruction ID {instruction.instruction_id} finished IF at cycle {instruction.cycle_stops[0]}")



# TESTING Registers

# registers = [Register() for i in range(32)]
# registers[0].insert_data(-4)
# print(registers[0].data)
# print(registers[0].bits)



# TESTING Instruction_Mem

# im1 = Instruction_Mem("inst.txt")
# im1.display()
# im1.put_instruction_in_cache(0)
# im1.put_instruction_in_cache(4)
# im1.put_instruction_in_cache(2)
# im1.put_instruction_in_cache(3)
# for block in im1.cache:
#     for instruction in block:
#         print(f"{instruction.line}")
#     print("\n\n")

# print(im1.instruction_in_cache(1))
# for instruction in im1.instructions:
#     print(instruction.operands)

# for line in range(len(im1.instructions)):
#     print(f"{line + 1} --> {im1.instruction_in_cache(line)}")
# print(im1.instruction_in_cache(5))

# safety = 30
# index = 0
# num_miss = 0
# num_access = 0
# num_hits = 0
# while im1.pc_out_of_bounds() == False and index < safety:
#     if im1.instruction_in_cache(index) == False:
#         print("I-Cache Miss")
#         num_miss += 1
#         im1.put_instruction_in_cache(index)
#     else:
#         print("Instruction Hit!")
#         num_hits += 1
#     print("Accessing from I-Cache")
#     num_access += 1
#     im1.program_counter += 1
    
#     index += 1
# print("\n\n")
# print(f"Num Miss --> {num_miss}")
# print(f"Num Access --> {num_access}")
# print(f"Num Hits --> {num_hits}")



print("EXITED WITHOUT ERROR")