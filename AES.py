from encrypt import encryptionAES
from decrypt import decryptionAES
from utils import populate_key,key_expansion

#Number of rounds
key_rounds = {
    128:10,
    192:12,
    256:14
}

#Length of the hexadecimal format key. 
key_hex_length = {
    128:32,
    192:48,
    256:64
    }



if __name__=="__main__":
    #given a msg
    
    plaintext = input("Enter the text to be encrypted: ")
    # key_size = input("Enter key size (128/192/224) (default:128):")
    
    if not plaintext:
        print("Plain text not received.")
        exit(-1)
    # if not key_size:
    key_size = 128
    key_size = int(key_size)
    key = b'0x0f1571c947d9e8590cb7add6af7f6798'
    if not int(key_size) in [128,192,224]:
        print("Enter correct key size")
        exit(-2)

    key_matrix = populate_key(key[2:])
    subkeys = key_expansion(key_matrix,num_rounds=key_rounds[key_size])
    cipher_text = encryptionAES(plaintext,subkeys)
    print("Encrypted text: ",cipher_text)
    retrieved_text = decryptionAES(cipher_text,subkeys)
    print("Decrypted Text: ",retrieved_text)

    