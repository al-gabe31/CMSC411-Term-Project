# Contains the code for the Data_Cache class
from Data import *

class Data_Cache:
    # Takes all data from a text file and stores it into memory
    def __init__(self, file):
        self.data = [] # Contains all data from memory
        self.cache = {
            "set0": [[Data() for i in range(4)], [Data() for i in range(4)]],
            "set1": [[Data() for i in range(4)], [Data() for i in range(4)]]
        } # 2-way set four 4-word block cache
        self.miss_cycles_left = 0
        self.lru_indeces = [0, 0] # First index is for set0 and the second for set1
        
        self.used = {
            "set0": [False, False],
            "set1": [False, False]
        }
        
        self.cache_to_data = {
            "set0": [-1, -1],
            "set1": [-1, -1]
        } # Records the line_index of each block to the data's memory

        # IMPORTANT DATA FOR output.txt
        self.num_access_requests = 0
        self.num_data_cache_hits = 0

        with open(file, "r") as file:
            # Reads the text file line by line
            while line := file.readline():
                self.data.append(Data(line[0:32]))
    
    # Returns True if a specific data is located in cache (somewhere)
    # Returns False otherwise
    def data_in_cache(self, value):
        values = []

        # Puts all data from both sets in both blocks each into values
        # Starting with set 0
        for data in self.cache["set0"][0]:
            values.append(data.data_decimal)
        for data in self.cache["set0"][1]:
            values.append(data.data_decimal)
        # Moving on to set 1
        for data in self.cache["set1"][0]:
            values.append(data.data_decimal)
        for data in self.cache["set1"][1]:
            values.append(data.data_decimal)
        
        return value in values

    # Returns which set a specific data is located in cache
    # Returns "set0" if it's in set0
    # Returns "set1" if it's in set1
    # Returns -1 if it's in neither set
    def get_set_address(self, value):
        set0_values = []
        set1_values = []

        for data in self.cache["set0"][0]:
            set0_values.append(data.data_decimal)
        for data in self.cache["set0"][1]:
            set0_values.append(data.data_decimal)

        for data in self.cache["set1"][0]:
            set1_values.append(data.data_decimal)
        for data in self.cache["set1"][1]:
            set1_values.append(data.data_decimal)
        
        if value in set0_values:
            return "set0"
        elif value in set1_values:
            return "set1"
        return -1

    # Returns the address of the block a specific data is located in a set
    # Returns 0 if it's located in block 0
    # Returns 1 if it's located in block 1
    # Returns -1 if it isn't located in either blocks
    def get_block_address(self, set, value):
        if set == -1:
            return -1
        
        block0_values = []
        block1_values = []

        for data in self.cache[set][0]:
            block0_values.append(data.data_decimal)
        for data in self.cache[set][1]:
            block1_values.append(data.data_decimal)
        
        if value in block0_values:
            return 0
        elif value in block1_values:
            return 1
        return -1
    
    # Returns the address of a specific data located in a block
    # Returns 0-3 if value located in a specific set and block
    # Returns -1 if value isn't located in a specific set and block
    def get_data_address(self, set, block, value):
        if set == -1 or block == -1:
            return -1
        
        if self.cache[set][block][0].data_decimal == value:
            return 0
        if self.cache[set][block][1].data_decimal == value:
            return 1
        if self.cache[set][block][2].data_decimal == value:
            return 2
        if self.cache[set][block][3].data_decimal == value:
            return 3
        return -1
    
    # Retrieves data from memory and puts it into cache
    # Returns -1 for any error cases (fails to put data into cache)
    def put_data_in_cache(self, address):
        # We can't put data into cache in any of the following cases
        if address < 256 or address >= 384:
            return -1 # Address out of bounds
        if self.miss_cycles_left > 0:
            return -1 # Can't put during a data-cache miss
        
        line_index = address - 256 # Since data starts at address 0x100
        line_index /= 4 # Has to be word aligned
        line_index = int(line_index)

        base_data = self.data[line_index]

        if self.data_in_cache(base_data.data_decimal) == True:
            return -1 # Can't put data into cache if it's already there
        
        set_number = int(line_index / 4) % 2
        set_string = ""
        if set_number == 0:
            set_string = "set0"
        else:
            set_string = "set1"

        if self.used[set_string][self.lru_indeces[set_number]] == False:
            self.cache_to_data[set_string][self.lru_indeces[set_number]] = line_index
            
            # Adds 4 data into cache
            for i in range(4):
                # Index not out of range
                if line_index + i < len(self.data):
                    self.cache[set_string][self.lru_indeces[set_number]][i].update(self.data[line_index + i].data_decimal)
                else:
                    self.cache[set_string][self.lru_indeces[set_number]][i].update(0)
            
            self.used[set_string][self.lru_indeces[set_number]] = True
            
            # Update LRU block index
            self.lru_indeces[set_number] += 1
            self.lru_indeces[set_number] %= 2
        else:
            # We first have to clear that block in the cache
            for i in range(4):
                self.data[self.cache_to_data[set_string][self.lru_indeces[set_number]] + i] = self.cache[set_string][self.lru_indeces[set_number]][i]
            
            self.miss_cycles_left = 12
            self.used[set_string][self.lru_indeces[set_number]] = False
            return -2 # Indicating a D-Cache stall where you had to clear data in the cache
    
    # Updates data from cache and in memory
    def update_data_in_cache(self, address, new_value):
        # We can't update data from cache in any of the following cases
        if address < 256 or address >= 384:
            return -1 # Address out of bounds
        if self.miss_cycles_left > 0:
            return -1 # Can't update during a data-cache miss
        
        line_index = address - 256 # Since data starts at address 0x100
        line_index /= 4 # Has to be word aligned
        line_index = int(line_index)

        base_data = self.data[line_index]
        base_value = base_data.data_decimal

        if self.data_in_cache(base_data.data_decimal) == False:
            return -1 # Can't update data from cache if it's not there
        
        set_address = self.get_set_address(base_value)
        block_address = self.get_block_address(set_address, base_value)
        data_address = self.get_data_address(set_address, block_address, base_value)

        # Officially updates the data in cache
        self.cache[set_address][block_address][data_address].update(new_value)
        self.data[line_index].update(new_value)
    
    # On second thought, we might now have to do this...
    def write_back_to_mem(self):
        # DON'T FORGET TO CHANGE THIS TO "data.txt"
        with open("dummy_data.txt", "w") as file:
            for i in range(len(self.data)):
                line = self.data[i].data_string + "\n"
                file.write(line)
    
    # This is mostly for debugging
    def print_all_data(self):
        for data in self.data:
            print(data.data_decimal)