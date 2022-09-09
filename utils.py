import numpy as np
from Sbox import sbox
Rcon = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1B,0x36]

mixcols_ord = np.array(
    [[0x02,0x03,0x01,0x01],
    [0x01,0x02,0x03,0x01],
    [0x01,0x01,0x02,0x03],
    [0x03,0x01,0x01,0x02]
    ])


def populate_key(key_hexa):
    i=0
    key_matrix = np.array([[hex(0) for _ in range(4)] for _ in range(4)]) 
    for c in range(4):
            for r in range(4):
                print(key_hexa[i:i+2])
                key_matrix[r][c] = key_hexa[i:i+2]    #"{}{}".format(hexa_text[i],hexa_text[i+1])
                i=i+2
                if(i>=len(key_hexa)):
                    return key_matrix
    return key_matrix

def rotate_word(word,num_rotations):
    return(np.roll(word,4-num_rotations)) #4-num_rot  is done because we have to roll it in the anticlockwise direction. np.roll rolls in clockwise.


def SubWord(word):
    new_word = word.copy()
    for i in range(len(word)):
        new_word[i] = "{:02x}".format(sbox[int(word[i],16)])
    return new_word

def xor_rcon(rconstant,test_y1):
    test_z1 = test_y1.copy()
    test_z1[0] = "{:02x}".format(int(test_y1[0],16) ^ rconstant)
    return test_z1

def xor_words(word1,word2):
    w = word1.copy()
    for i in range(4):
        w[i]="{:02x}".format(int(word1[i],16)^int(word2[i],16))
    return w

def key_expansion(key_matrix,num_rounds):
    subkeys = {}
    w = {}
    #Round 0
    w[0] = key_matrix[:,0]
    w[1] = key_matrix[:,1]
    w[2] = key_matrix[:,2]
    w[3] = key_matrix[:,3]
    x ={}
    y={}
    z={}
    subkeys[0] = np.column_stack((w[0],w[1],w[2],w[3]))
    for i in range(1,num_rounds+1):
        x[i] = rotate_word(w[4*i-1],1)
        y[i] = SubWord(x[i])
        z[i] = xor_rcon(Rcon[i-1],y[i])
        w[4*i] = xor_words(w[4*(i-1)], z[i])
        w[4*i+1] = xor_words(w[4*i], w[4*(i-1)+1])
        w[4*i+2] = xor_words(w[4*i + 1], w[4*(i-1)+2])
        w[4*i+3] = xor_words(w[4*i + 2], w[4*(i-1)+3])
        subkeys[i] = np.column_stack((w[4*i],w[4*i+1],w[4*i+2],w[4*i+3]))
    
    print(subkeys.items())
    return subkeys
    
