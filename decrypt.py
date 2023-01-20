import codecs
from operator import mul
import numpy as np
import math
from utils import key_expansion,rotate_word,inv_mixcols_ord
from Sbox import inv_s_box



def AddRoundKey(state_mat,key):
    result = state_mat.copy()
    for i in range(4):
        for j in range(4):
            result[i,j]="{:02x}".format(int(state_mat[i][j],16)^int(key[i][j],16))
    return result

def InvSubBytes(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
            new_state[i][j] = "{:02x}".format(inv_s_box[int(state[i][j],16)])
    return new_state

def InvShiftRows(state):
    state[1] = rotate_word(state[1],3)
    state[2] = rotate_word(state[2],2)
    state[3] = rotate_word(state[3],1)
    return state

def mul_by_2(state1):
    """
    Multiply given hexadecimal format byte by 0x02
    """
    temp_state1 = "{:02x}".format((int(state1,16)<<1) & 0xff) #Left shift by 1 = multiplication by 2
    if int(state1,16)>=0x80:
            #means that MSB is 1. Perform bitwise xor with 0x1B
            state1 = "{:02x}".format((int(temp_state1,16)^int(b'0x1B',16)) & 0xff)
            return state1
    return temp_state1

def Inv_mixCols_Byte(val1,state1):
    if val1 == 0x09:
        temp_state1 = mul_by_2(mul_by_2(mul_by_2(state1))) #Multiplying by 2, 3 times to get 8. Will xor with state1 to get 9
        state1 = "{:02x}".format((int(state1,16) ^ int(temp_state1,16)) & 0xff)
        return state1
    elif val1 ==0x0B:
        # to multiply by 11-> mul by 4, add 1 to get 5. mul by 2 and add 1
        temp_state1 = mul_by_2(mul_by_2(state1))
        temp_state2 = "{:02x}".format((int(state1,16) ^ int(temp_state1,16)) & 0xff) 
        temp_state3 = mul_by_2(temp_state2)
        state1 = "{:02x}".format((int(state1,16) ^ int(temp_state3,16)) & 0xff)
        return state1

    elif val1 ==0x0D:
        #to multiply by 13-> multiply by 2, add 1 to get 3. multiply by 2 to get 6. multiply by 2 to get 12. add 1
        temp_state1 = mul_by_2(state1)
        temp_state2 = "{:02x}".format((int(state1,16) ^ int(temp_state1,16)) & 0xff) 
        temp_state3 = mul_by_2(mul_by_2(temp_state2))
        state1 = "{:02x}".format((int(state1,16) ^ int(temp_state3,16)) & 0xff) # XOR one more time with state byte to get the final result for multiplication with 0x03
        return state1
    elif val1 ==0x0E:
        #mul by 2, add 1 to get 3. mul by 2 to get 6. add 1 to get 7, mul by 2 to get 14 aka 0E
        temp_state1 = mul_by_2(state1)
        temp_state2 = "{:02x}".format((int(state1,16) ^ int(temp_state1,16)) & 0xff) 
        temp_state3 = mul_by_2(temp_state2)
        temp_state4 = "{:02x}".format((int(state1,16) ^ int(temp_state3,16)) & 0xff) 
        state1 = mul_by_2(temp_state4)

    return state1
    
def InvMixColumns(state):
    new_state = state.copy()
    for i in range(4):
        for j in range(4):
                new_state[i][j]= "{:02x}".format(
                    int(Inv_mixCols_Byte( inv_mixcols_ord[i][0],state[0][j]),16) ^
                    int(Inv_mixCols_Byte( inv_mixcols_ord[i][1],state[1][j]),16) ^
                    int(Inv_mixCols_Byte( inv_mixcols_ord[i][2],state[2][j]),16) ^
                    int(Inv_mixCols_Byte( inv_mixcols_ord[i][3],state[3][j]),16)  
                )
    return new_state

def decryptionAES(cipher_matrix,subkeys,num_rounds_key):
    final_matrix = cipher_matrix.copy()
    key_to_be_added = num_rounds_key # In decryption, the keys are added in reverse
    for num_block in range(cipher_matrix.shape[0]):
        key_to_be_added = num_rounds_key

        state = cipher_matrix[num_block]
        round_state = AddRoundKey(state,subkeys[key_to_be_added])
        # print("Round ",key_to_be_added,"addroundkey: ",round_state)
        key_to_be_added=key_to_be_added-1
        for _ in range(1,num_rounds_key):
            # print("In round ",key_to_be_added)
            temp = InvShiftRows(round_state)
            # print("Inv shift rows",temp)
            temp1 = InvSubBytes(temp)
            # print("inv sub bytes: ",temp1)
            temp2 = AddRoundKey(temp1,subkeys[key_to_be_added])
            # print("add round key: ",temp2)
            round_state = InvMixColumns(temp2)
            # print("inv mix cols: ",round_state)
            key_to_be_added = key_to_be_added-1
            if(key_to_be_added <= 0):
                break
        #Last round does not have MixColumns layer
        temp = InvShiftRows(round_state)
        # print("round 1 inv shift rows",temp)
        temp1 = InvSubBytes(temp)
        # print("inv sub bytes",temp1)
        round_state = AddRoundKey(temp1,subkeys[0])
        # print("add round key",round_state)
        final_matrix[num_block] = round_state
    return final_matrix
