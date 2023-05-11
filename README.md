# CMSC411-Term-Project
Name:   Gabe Aquino
ID:     LQ90575
Email:  lq90575@umbc.edu
About:  Python program that mimics a pipeline processor

# Important Notes
My project isn't 100% "aligned" with what it should be in all the test cases provided. For instance with the instruction provided in the project file, the "ADD R7, R7, R6" instruction finishes the ID stage stage 3 cycles earlier. Because of all, all instructions past that (as well as any instructions that are currently in the pipeline when this occurs) will finish their remaining stages 3 cycles later. As for the 2 other test cases, the problem is very similar. You have a slight misalignment in one of the stages (so far, it seems like it only happens in the ID stage), and all remaining stages for every instruction left are misaligned by the same amount. Also one last thing. Each program of course has 2 "HLT" instructions at the very end. The program will fetch both "HLT" instructions no matter what, even if the first one has already finished the ID stage. I don't know if it's really too big of a deal, but my program still includes includes information about the 2nd "HLT" instruction. Because of that, the data for number of access requests for instruction cache and number of instruction cache hits might be 1 more.

However, the project does work for the most part! There is both an I-Cache and D-Cache. Both behave the way as intended during an I-Cache miss and D-Cache miss (based on the provided test cases). Forwarding for the most part also works. The program checks which registers are currently being used and stores that result in the forwarding unit. Once that instruction reaches the WB stage, it updates the proper registers and removes the temp data in the forwarding unit.

If you have any questions regarding my project, feel free to email and and I can try to clear things up.

# How to Run the Program
Before doing anything, make sure that you have the right instructions in inst.txt as well as all the necessary data in data.txt. Once you have that, just type "make" in the command line and simulation.py should create the output.txt file containing all information about the simulation run.

You can change what instructions the simulation takes by pasting in a different instruction in the inst.txt file. Just type "make" again to let the simulation run.

Once you are done with the simulation, you can delete output.txt by typing "make clean". This assumes that you're running this in a Bash terminal (since it uses the "rm output.txt command).

# Changing the Safety (Prevents Infinite While Loop)
In the Processor.py file at line 754, there is a SAFETY variable meant to prevent an infinite while loop. It sets the maximum cycle number that the processor will take. It's currently set at a really high number (1000) since I doubt any 32 instruction should take more than 1000 cycles (unless it's an infinite branching loop). Feel free to change the SAFETY variable to a higher number if needed.