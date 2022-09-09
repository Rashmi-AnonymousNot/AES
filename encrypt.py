import codecs
import numpy as np
import math
from utils import populate_key,key_expansion,rotate_word,mixcols_ord
from Sbox import sbox

def populate_data(hexa_text,num_blocks):
    i = 0
    init_matrix = np.array([[[hex(0) for _ in range(4)] for _ in range(4)] for _ in range(num_blocks)])  #np.zeros((num_blocks,4,4))

    for n in range(num_blocks):
        for c in range(4):
            for r in range(4):
                print(hexa_text[i:i+2])
                init_matrix[n][r][c] = int(hexa_text[i:i+2],16)    #"{}{}".format(hexa_text[i],hexa_text[i+1])
                i=i+2
                if(i>=len(hexa_text)):
                    return init_matrix
    return init_matrix


def initial(text):

    # hexa_text = codecs.encode(text.encode(),"hex")
    hexa_text = hex(int(codecs.encode(text.encode(),"hex"),16))[2:]
    print("hexa: ",hexa_text)
    num_blocks = math.ceil(len(hexa_text)/32)
    # hexa_text = hexa_text.decode("ascii")
    init_matrix = populate_data(hexa_text,num_blocks)
    print(init_matrix)
    return init_matrix

def AddRoundKey(state_mat,key):
    result = state_mat.copy()
    for i in range(4):
        for j in range(4):
            result[i,j]="{:02x}".format(int(state_mat[i][j],16)^int(key[i][j],16))
    return result

def SubBytes(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            new_state[i][j] = "{:02x}".format(sbox[int(state[i][j],16)])
    return new_state

def ShiftRows(state):
    state[1] = rotate_word(state[1],1)
    state[2] = rotate_word(state[2],2)
    state[3] = rotate_word(state[3],3)
    return state

def mixCols_Byte(state1,val1):
    if val1 == 0x01:
        return state1
    elif val1 ==0x02:
        temp_state1 = (state1<<1) #Left shift by 1 = multiplication by 2
        if state1>=0x80:
            #means that MSB is 1. Perform bitwise xor with 0x1B
            state1 = "{:02x}".format((int(temp_state1,16)^int(0x1B,16)) & 0xFF)
            return state1
        return temp_state1
    elif val1 ==0x03:
        temp_state1 = (state1<<1) #Left shift by 1 = multiplication by 2
        if state1>=0x80:
            #means that MSB is 1. Perform bitwise xor with 0x1B. Bitwise AND with 0xFF to keep the result positive
            temp_state1 = "{:02x}".format((int(temp_state1,16)^int(0x1B,16)) & 0xFF)
        state1 = "{:02x}".format((int(state1,16) ^ int(temp_state1,16)) & 0xFF) # XOR one more time with state byte to get the final result for multiplication with 0x03
        return state1
    return state1

def MixColumns(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
                new_state[i][j]= "{:02x}".format(
                    mixCols_Byte( state[i][0],mixcols_ord[0][j]) ^
                    mixCols_Byte( state[i][1],mixcols_ord[1][j]) ^
                    mixCols_Byte( state[i][2],mixcols_ord[2][j]) ^
                    mixCols_Byte( state[i][3],mixcols_ord[3][j])  
                )
    return new_state

def encryptionAES(plaintext,subkeys):
    state_matrix = initial(plaintext)

    #Iterating through all the 128bit msg blocks
    for num_block in range(state_matrix.shape[0]):
        #XOR the round 0 key and state matrix(contains the msg)
        state = state_matrix[num_block]
        round1_state = AddRoundKey(state,subkeys[0])
        for r in range(1,len(subkeys)):
            temp = SubBytes(round1_state)
            temp = ShiftRows(temp)
            temp = MixColumns(temp)

    


