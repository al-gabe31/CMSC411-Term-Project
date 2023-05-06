from functions import *
from Instruction_Mem import *
from Processor import *
from Data import *
from Data_Cache import *

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

dc1 = Data_Cache("data.txt")
dc1.print_all_data()
print("\n\n")
if dc1.put_data_in_cache(256) != -1:
    values = [i.data_decimal for i in dc1.cache["set0"][0]]
    print(values)
    print(dc1.lru_indeces[0])
if dc1.update_data_in_cache(260, 5) != 1:
    values = [i.data_decimal for i in dc1.cache["set0"][0]]
    print(values)
    print(dc1.lru_indeces[0])
dc1.write_back_to_mem()
# if dc1.put_data_in_cache(256 + (0 * 4)) != -1:
#     values = [i.data_decimal for i in dc1.cache["set0"][1]]
#     print(values)
#     print(dc1.lru_indeces[0])
# if dc1.put_data_in_cache(256 + (16 * 4)) != -1:
#     values = [i.data_decimal for i in dc1.cache["set0"][0]]
#     print(values)
#     print(dc1.lru_indeces[0])

# p1 = Processor("inst.txt")
# print(p1.is_all_null())
# p1.run()



# registers = [Register() for i in range(32)]
# registers[0].insert_data(65537)
# print(registers[0].data)
# print(registers[0].bits)


print("EXITED WITHOUT ERROR")