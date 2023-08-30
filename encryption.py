from string import whitespace
import sys
import time

def encryption_algo():

    graph1 = {
        "A": ["B", "C"],
        "B": ["A", "C", "D", "F"],
        "C": ["A", "B", "D", "G"],
        "D": ["B", "C", "E"],
        "E": ["D", "F", "G"],
        "F": ["B", "E", "G", "H", "J"],
        "G": ["C", "E", "F", "H", "K"],
        "H": ["F", "G", "I"],
        "I": ["H", "J", "K"],
        "J": ["F", "I", "K", "L"],
        "K": ["G", "I", "J", "L"],
        "L": ["J", "K"]
    }

    vertices = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
        "E" : 4,
        "F" : 5,
        "G" : 6,
        "H" : 7,
        "I" : 8,
        "J" : 9,
        "K" : 10,
        "L" : 11
    }

    graph2 = {
        "A": ["B", "C"],
        "B": ["A", "C", "D"],
        "C": ["A", "B", "D", "E"],
        "D": ["B", "C", "E", "F", "H"],
        "E": ["C", "D", "F"],
        "F": ["D", "E", "G", "H"],
        "G": ["F", "H", "I"],
        "H": ["D", "F", "G", "I", "J"],
        "I": ["G", "H", "J", "K"],
        "J": ["H", "I", "K"],
        "K": ["I", "J"],
        
    }

    vertices2 = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
        "E" : 4,
        "F" : 5,
        "G" : 6,
        "H" : 7,
        "I" : 8,
        "J" : 9,
        "K" : 10
    }

    # sum of the weights of the edges adjacent to v and denote it as S(v)
    graph1_dec = int(input("Which graph would you want to use? [1] [2]: "))

    if graph1_dec == 1:
        graph1 = graph1
        vertices = vertices
        print("Define dominating set D (A-L)")
    elif graph1_dec == 2:
        graph1 = graph2
        vertices = vertices2
        print("Define dominating set D (A-I)")

    def get_value(args):
        edge = graph1.get(args)
        value = 0
        for e in edge:
            value += vertices.get(e)
        return value

    C_value = input("D1: ").upper()
    v1 = C_value
    if C_value not in vertices:
        print("============================================================================================================")
        sys.exit('Error: Dominating set not in range of A-L!')
        

    F_value = input("D2: ").upper()
    v2 = F_value
    if F_value not in vertices:
        print("============================================================================================================")
        sys.exit('Error: Dominating set not in range of A-L!')

    K_value = input("D3: ").upper()
    v3 = K_value
    if K_value not in vertices:
        print("============================================================================================================")
        sys.exit('Error: Dominating set not in range of A-L!')

    C_value = get_value(C_value)
    F_value = get_value(F_value)
    K_value = get_value(K_value)

    print("============================================================================================================")
    message = input("Encrypt this message: ").translate(dict.fromkeys(map(ord, whitespace)))
    print("============================================================================================================")
    print("Message:", message)

    # convert to a binary string using ASCII encoding
    def to_ascii(args):
        message_list = list(args)

        message_ascii = []
        for x in message_list:
            message_ascii.append("0" + bin(ord(x))[2:])

        return message_ascii

    ascii_values = to_ascii(message)
    concatenate_ascii_values = "".join(ascii_values)
    n = 4
    ascii_split = [concatenate_ascii_values[i:i+n] for i in range(0, len(concatenate_ascii_values), n)]

    #For each chunk C, we compute E = (S(v) + C) mod 2 K, where S(v) is the sum of the labels of v and all vertices adjacent to v, and K = 4.
    def mod_it(args):
        counter = 1
        mod = []

        for x in args:
            if counter == 1:
                y = (C_value + int(x, 2)) % 16
                mod.append(y)
                counter += 1
                continue

            if counter == 2:
                y = (F_value + int(x, 2)) % 16
                mod.append(y)
                counter += 1
                continue

            if counter == 3:
                y = (K_value + int(x, 2)) % 16
                mod.append(y)
                counter = 1
                continue


        return mod

    moded = mod_it(ascii_split)

    #XOR E with the label of v and all edges adjacent to v
    the_C_values = [vertices.get(v1)]
    the_F_values = [vertices.get(v2)]
    the_K_values = [vertices.get(v3)]

    for a in graph1.get(v1):
        the_C_values.append(vertices.get(v1) + vertices.get(a))
        
    for b in graph1.get(v2):
        the_F_values.append(vertices.get(v2) + vertices.get(b))

    for c in graph1.get(v3):
        the_K_values.append(vertices.get(v3) + vertices.get(c))

    for_XOR = {
        "XOR_C" : the_C_values,
        "XOR_F" : the_F_values,
        "XOR_K" : the_K_values
    }

    #Encrypted Chunks = E XOR label(v) XOR labelS(e)
    def XOR_it(args):
        counter = 1
        XOR_chunks = []

        for m in moded:
            if counter == 1:
                for c in for_XOR.get("XOR_C"):
                    m = m ^ c
                XOR_chunks.append(m)
                counter += 1
                continue

            if counter == 2:
                for f in for_XOR.get("XOR_F"):
                    m = m ^ f
                XOR_chunks.append(m)
                counter += 1
                continue

            if counter == 3:
                for k in for_XOR.get("XOR_K"):
                    m = m ^ k
                XOR_chunks.append(m)
                counter = 1
                continue

        return XOR_chunks

    xored = XOR_it(moded)

    xor = []
    for x in xored:
        xor.append(str(x))
    xor = "".join(xor)

    #concatenate the encrypted chunks to obtain the encrypted message
    encrypted = bin(int(xor))[2:]

    end_time = time.process_time()

    print("Encrypted message:", encrypted)
    print("Runtime:", end_time , "seconds")
    print("============================================================================================================")
    print("For decryption:")
    print("Sum of the weights of the edges adjacent to v:", str(C_value) + "," + str(F_value) + "," + str(K_value))
    print("E=(S(v)+C)mod2K:", moded)
    print("============================================================================================================")

def decryption_algo():
    weights = input("Weights of edges separated by ',': ")
    formula = input("E=(S(v)+C)mod2K values separated by ',': ")
    weights = weights.strip().split(",")
    formula = formula.strip().split(",")

    counter = 1
    decrypted = [bin((int(formula[0]) - int(weights[0])) % 16)[2:].zfill(4)]

    for f in formula[1:]:
        f = bin((int(f) - int(weights[counter]) + 16) % 16)[2:].zfill(4)
        decrypted.append(f)
        if counter < 2:
            counter += 1
        else:
            counter = 0

    decrypted = "".join(decrypted)
    n = 8
    decrypted = [decrypted[i:i+n] for i in range(0, len(decrypted), n)]

    chr_decrypted = []
    for d in decrypted:
        chr_decrypted.append(chr(int(d, 2)))

    # def binary_to_string(bits):
    #     return ''.join([chr(int(i, 2)) for i in bits])

    print("============================================================================================================")
    print(decrypted)
    print(chr_decrypted)
    print("============================================================================================================")

while True:
    print("============================================================================================================")
    print("What are we doing today?")
    dec1 = int(input("[1] Encryption   [2] Decryption   [3] Exit: "))

    if dec1 == 1:
        print("============================================================================================================")
        encryption_algo()
        dec2 = input("Encrypt another message? (Y/N): ")
        if dec2.lower() == "y":
            encryption_algo()
        elif dec2.lower() == "n":
            continue
        else:
            print("============================================================================================================")
            sys.exit("Invalid input!")
            print("============================================================================================================")
    elif dec1 == 2:
        print("============================================================================================================")
        decryption_algo()
        dec2 = input("Decrypt another message? (Y/N): ")
        if dec2.lower() == "y":
            decryption_algo()
        elif dec2.lower() == "n":
            continue
        else:
            print("============================================================================================================")
            sys.exit("Invalid input!")
            print("============================================================================================================")
    elif dec1 == 3:
        print("============================================================================================================")
        print("Thank you for encrypting!")
        print("============================================================================================================")
        exit()
    else:
        print("============================================================================================================")
        sys.exit("Invalid input!")
        print("============================================================================================================")