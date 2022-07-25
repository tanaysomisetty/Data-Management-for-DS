import sys

def encode(st):
    currChar = ""
    count = 1
    encoding = ""
    first = True
    
    for c in st:
        if c == currChar:
            count += 1
        else:
            if first == False:
                encoding = encoding + currChar + str(count)
            else:
                first = False
            currChar = c
            count = 1
    encoding = encoding + currChar + str(count)
    return encoding

    
def decode(st):
    currChar = ""
    currCount = 0
    decoding = ""
    
    for c in st:
        if c.isalpha():
            currChar = c
        else:
            currCount = int(c)
            for i in range(currCount):
                decoding = decoding + currChar
            
    return decoding

print(encode(sys.argv[1]))
print(decode(sys.argv[2]))