# simulator grp B15
'''
The Process:
Each of the distinct required components have been made into functions.
The EE function will be used to pass each instruction(which already will have been loaded onto the memory (MEM) beforehand).
The EE within it will contain :
a) A function that checks for general errors ie length etc
b) A function that classifies the instruction into its type ie A to F
c) Diff Functions that execute the instruction depending on the type
d) A function to update the global PC
'''

'''
First Pass:
Will scan for the necessary labels (i.e. line numbers from where the label starts)
Will scan for variables given as arguements //(and also confirm if these values are appropriate.)
Ex: //if code is 64 lines, the first var should be on line 64(0 indexing), if there is no var to 64th line but directly to 65th line then this is an error.
Note:1.Once any other syntactical error is formed we dont have to worry about the values of variables as error message is all that is needed.
     2.Variable values will be stored in a dictionary and then wriiten into memory only just before the printing
'''

'''
PC Reg Values
For each iteration of the PC we should have all the values of the registers at that time. Thus a dictionary with PC value as key
and a list of the register values as the value can be used.
'''


from platform import machine
import sys
MEM = ['0'*16]*256  # actual memory
PC = '0'*8  # initialised at 0
regs = {'000': 'R0', '001': 'R1', '010': 'R2', '011': 'R3',
        '100': 'R4', '101': 'R5', '110': 'R6', '111': 'FLAGS'}
# comR is the set of all registers. Have included lowercase versions too just to adjust for keys
comR = {'R0': '0000000000000000', 'R1': '0000000000000000', 'R2': '0000000000000000', 'R3': '0000000000000000', 'R4': '0000000000000000', 'R5': '0000000000000000', 'R6': '0000000000000000',
        'FLAGS': '0000000000000000'}
InsType = {'10000': 'A', '10001': 'A', '10110': 'A', '11010': 'A', '11011': 'A', '11100': 'A', '10010': 'B', '11001': 'B', '11000': 'B', '10011': 'C',
           '10111': 'C', '11101': 'C', '11110': 'C', '10100': 'D', '10101': 'D', '11111': 'E', '01100': 'E', '01101': 'E', '01111': 'E', '01010': 'F'}


#_____Additional_Functions_________#

def conv2dec(b):  # internally runs the coversion of 8bit bin to decimal for PC
    # if len(b) != 8 or len(b)!= 16:
    #     return 'wrong value'
    # else:
    dec = 0
    b2 = b[::-1]
    for i in range(0, len(b2)):
        dec += int(b2[i])*(2**i)
    return dec


# converting integer x to 16 bit binary val to store in registers
def convert_to_16bit_bin(x):
    binary_num = bin(x)[2:]
    if len(binary_num)>16:
        binary_num=binary_num[-16:]
    return ((16-len(binary_num))*'0')+str(binary_num)


# converting integer x to 8 bit binary val to store in PC
def convert_to_8_bit_bin(x):
    binary_num = bin(x)[2:]
    if len(binary_num)>16:
        binary_num=binary_num[-8:]
    return ((8-len(binary_num))*'0')+str(binary_num)


def ones_complement(bin_string):  # takes 16 bit binary as input and performs bitwise NOT
    ret_string = ''
    for i in range(16):
        if bin_string[i] == '0':
            ret_string += '1'
        else:
            ret_string += '0'
    return ret_string


def conv2Lcase(reg):  # checks in case r1 is passed instead of R1. Assume FLAGS is the only correct option
    if reg[0] == 'r':
        return 'R'+reg[1]

#_____Error_Handling_Functions_____#


# inp is a list of strings. Each string is one (ideally) 16bit instruction
def check_full_len(inp):
    if len(inp) > 256:
        return 'Length Exceeded'
    else:
        return 1


# inpline is a string of (ideally) a 16bit instruction.
def check_indv_len(inpline):
    if len(inpline) != 16:
        return 'Length Exceeded'
    else:
        return 1

#_____Type_Check_&_Break_Functions_#


def check_type(inpline):  # takes in he 16bit instruction and returns type
    if inpline[0:5] not in InsType.keys():
        return 'invalid instruction'
    else:
        return InsType[inpline[0:5]]


# checks type and returns list that breaks ins into its components like opcode,regs,variable etc
def Breakin2list(inpline):
    if check_type(inpline) == 'A':
        return Break_A(inpline)
    elif check_type(inpline) == 'B':
        return Break_B(inpline)
    elif check_type(inpline) == 'C':
        return Break_C(inpline)
    elif check_type(inpline) == 'D':
        return Break_D(inpline)
    elif check_type(inpline) == 'E':
        return Break_E(inpline)
    elif check_type(inpline) == 'F':
        return Break_F(inpline)
    else:
        return 'invalid instruction'


def Break_A(inpline):
    l = []
    l+= [inpline[0:5]]
    l+= [inpline[7:10]]
    l+= [inpline[10:13]]
    l+= [inpline[13:16]]
    return l


def Break_B(inpline):
    l = []
    l+= [inpline[0:5]]
    l+= [inpline[5:8]]
    l+= [inpline[8:]]
    return l


def Break_C(inpline):
    l = []
    l+= [inpline[0:5]]
    l+= [inpline[10:13]]
    l+= [inpline[13:16]]
    return l


def Break_D(inpline):
    l = []
    l+= [inpline[0:5]]
    l+= [inpline[5:8]]
    l+= [inpline[8:]]
    return l


def Break_E(inpline):
    l = []
    l+= [inpline[0:5]]
    l+= [inpline[8:]]
    return l


def Break_F(inpline):
    l = []
    l+= [inpline[0:]]
    return l

#_____Required_Functions___________#


def PCounter(b):  # returns the instruction at the line number given(in binary)
    return MEM[conv2dec(b)]


def RF(reg):
    if reg not in comR.keys() and reg[0]!='r':
        return 'wrong value'
    else:
        return comR[conv2Lcase(reg)]


# main code starts from here
binary_input = sys.stdin.read()
machine_code = binary_input.split('\n')
for i in range(len(machine_code)):
    MEM[i] = machine_code[i]
PC = '0'*8
comR['FLAGS']= '0000000000000000'
len_check = check_full_len(machine_code)
if len_check == 1:
    while (int(PC, 2) < len(machine_code)):
        i = int(PC,2)
        print('i:',i)
        instruction = machine_code[i]
        instr_len_check = check_indv_len(instruction)
        

        if instr_len_check:
            type = check_type(machine_code[i])
            instruction_list = Breakin2list(machine_code[i])

            if type == 'A':
                if instruction_list[0] == '10000':  # add reg1 reg2 reg3
                    sum=int(comR[regs[instruction_list[1]]], 2)+int(comR[regs[instruction_list[2]]], 2)
                    comR[regs[instruction_list[3]]] = convert_to_16bit_bin(sum)
                    comR['FLAGS']= '00000000000000000'
                    if int(comR[regs[instruction_list[1]]], 2)+int(comR[regs[instruction_list[2]]], 2)>65535:
                        comR['FLAGS']= '00000000000001000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

                elif instruction_list[0] == '10001':  # sub reg1 reg2 reg3
                    diff = int(comR[regs[instruction_list[1]]], 2) - \
                        int(comR[regs[instruction_list[2]]], 2)

                    if diff >= 0:
                        comR[regs[instruction_list[3]]
                             ] = convert_to_16bit_bin(diff)
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)

                    else:
                        comR[regs[instruction_list[3]]
                             ] = convert_to_16bit_bin(0)
                        comR['FLAGS']= '00000000000001000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                elif instruction_list[0] == '10110': #mul reg1 reg2 reg3
                    pro=int(comR[regs[instruction_list[1]]], 2)*int(comR[regs[instruction_list[2]]], 2)
                    comR['FLAGS']= '00000000000000000'
                    if pro>65535:
                        comR['FLAGS']= '00000000000001000'
                    comR[regs[instruction_list[3]]] = convert_to_16bit_bin(pro)
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                
                elif instruction_list[0]=='11010': # xor reg1 reg2 reg3
                    comR[regs[instruction_list[3]]]=convert_to_16bit_bin(int(comR[regs[instruction_list[1]]], 2)^int(comR[regs[instruction_list[2]]], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                
                elif instruction_list[0]=='11011': #or reg1 reg2 reg3
                    comR[regs[instruction_list[3]]]=convert_to_16bit_bin(int(comR[regs[instruction_list[1]]], 2)|int(comR[regs[instruction_list[2]]], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                
                else: #and reg1 reg2 reg3
                    comR[regs[instruction_list[3]]]=convert_to_16bit_bin(int(comR[regs[instruction_list[1]]], 2)&int(comR[regs[instruction_list[2]]], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                    
            elif type == 'B':
                if instruction_list[0] == '10010':  # mov reg1 $Imm
                    comR[regs[instruction_list[1]]] = convert_to_16bit_bin(
                        int(instruction_list[2], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

                elif instruction_list[0] == '11000':  # rs reg1 $Imm
                    comR[regs[instruction_list[1]]] = convert_to_16bit_bin(int(
                        comR[regs[instruction_list[1]]], 2) >> int(comR[regs[instruction_list[2]]], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

                else:  # lsreg1 $Imm
                    comR[regs[instruction_list[1]]] = convert_to_16bit_bin(int(
                        comR[regs[instruction_list[1]]], 2) << int(comR[regs[instruction_list[2]]], 2))
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

            elif type == 'C':
                if instruction_list[0] == '10011':  # mov reg1 reg2
                    comR[regs[instruction_list[2]]] = comR[regs[instruction_list[1]]]
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                    
                elif instruction_list[0] == '10111':  # div reg3 reg4
                    quo=int(comR[regs[instruction_list[1]]], 2)//int(comR[regs[instruction_list[2]]], 2)
                    rem=int(comR[regs[instruction_list[1]]], 2)%int(comR[regs[instruction_list[2]]], 2)
                    comR['R0']=convert_to_16bit_bin(quo)
                    comR['R1']=convert_to_16bit_bin(rem)
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

                elif instruction_list[0] == '11101':  # not reg1 reg2
                    comR[regs[instruction_list[2]]] = ones_complement(
                        comR[regs[instruction_list[1]]])
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)

                else:  # cmp reg1 reg2

                    if int(comR[regs[instruction_list[1]]], 2)>int(comR[regs[instruction_list[2]]], 2):
                        comR['FLAGS'] = '0000000000000010'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                    elif int(comR[regs[instruction_list[1]]], 2)<int(comR[regs[instruction_list[2]]], 2):
                        comR['FLAGS']= '0000000000000100'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                    else:
                        comR['FLAGS']= '0000000000000001'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
            elif type == 'D':
                if instruction_list[0] == '10100':  # load reg1 mem
                    new_val = MEM[conv2dec(instruction_list[2])]
                    comR[regs[instruction_list[1]]] = new_val
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                else:
                    MEM[conv2dec(instruction_list[2])] = comR[regs[instruction_list[1]]]
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    PC = convert_to_8_bit_bin(i+1)
                pass

            elif type == 'E':
                if instruction_list[0] == '11111':  # jmp mem
                    PC = str(instruction_list[1])
                    comR['FLAGS']= '00000000000000000'
                    print(PC,end=' ')
                    print(*list(comR.values()))
                    continue
                elif instruction_list[0] == '01100':  # jlt mem
                    if comR['FLAGS'][-3] == '1':
                        PC = str(instruction_list[1])
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        continue
                    else:
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                        pass
                elif instruction_list[0] == '01101':  # jgt mem
                    if comR['FLAGS'][-2] == '1':
                        PC = str(instruction_list[1])
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        continue
                    else:
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                        pass
                else:  # je mem
                    if comR['FLAGS'][-1] == '1':
                        PC = str(instruction_list[1])
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        continue
                    else:
                        comR['FLAGS']= '00000000000000000'
                        print(PC,end=' ')
                        print(*list(comR.values()))
                        PC = convert_to_8_bit_bin(i+1)
                        pass
            else:
                comR['FLAGS']= '00000000000000000'
                print(PC,end=' ')
                print(*list(comR.values()))
                break
        else:
            print(instr_len_check)  # give error in case of length exceeding?
        
        
        
else:
    print(len_check)  # give error in case of length exceeding?
    
for i in MEM:
    print(i)