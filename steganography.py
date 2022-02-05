import hashlib
from skimage import io as skio
import sys

def encodeImage(file, bstring):
    imagearray = skio.imread(file)
    blist = list(bstring)
    for M in imagearray:
        for N in M:
            for value in range(0, 3):
                if len(blist) != 0:
                    a = list(int2Binary(N[value]))                
                    a.pop()
                    a.pop()
                    a.append(blist.pop(0))
                    a.append(blist.pop(0))
                    N[value] = binary2Integer(''.join(a))
    name, extension = file.split('.')
    outfile = name + '_steg.' + extension
    #print(imagearray[0][0:40])
    skio.imsave(outfile, imagearray)
    return 1

def decodeImage(file):
    imagearray = skio.imread(file)
    bitstring = ''
    for M in imagearray:
        for N in M:
            for value in range(0, 3):
                a = list(int2Binary(N[value]))
                bitstring = bitstring + a.pop(-2)
                bitstring = bitstring + a.pop(-1)
    return bitstring

def decodeBinaryString(bitstring):
    asciistring = ''
    for i in range(0, int(len(bitstring)/8)):
        charbits = bitstring[i*8:i*8+8]
        asciistring = asciistring + binary2Character(charbits)
    return asciistring

def unpackage(astring):
    okaystuff, garbage = astring.split('</h>')
    moregarbage, betterstuff = okaystuff.split('<m>')
    message, hash = betterstuff.split('</m><h>')
    return message, hash

def binary2Integer(binary):
    return int(binary, 2)

def int2Binary(integer):
    return format(integer, '08b')

def text2Binary(string):
    return str(''.join(format(i, '08b') for i in bytearray(string, encoding ='utf-8')))

def binary2Character(bitstring):
    return chr(binary2Integer(bitstring))

def hashString(ts):
    m = hashlib.sha256()
    m.update(bytearray(ts, encoding ='utf-8'))
    return m.hexdigest()

def getContents(pathtofile):
    with open(pathtofile) as f:
        return f.read()
        
def writeContents(message):
    with open('secretmessage.txt', 'w') as f:
        f.write(message)

def startEncode(ifp, tfp):
    textstring = getContents(tfp)
    texthash = hashString(textstring)
    encodingstring = '<m>' + textstring + '</m><h>' + texthash + '</h>'
    binarystring = text2Binary(encodingstring)
    status = encodeImage(ifp, binarystring)
    print(f'{status=}')
    
def startDecode(ifp):
    encodedmessagebits = decodeImage(ifp)
    asciistring = decodeBinaryString(encodedmessagebits)
    message, hash = unpackage(asciistring)
    vhash = hashString(message)
    if vhash == hash:
        status = 1
    else:
        status = 0
    writeContents(message)
    print(f'{status=}')

process = sys.argv[1]

if process == 'e':
    imagefilepath = sys.argv[2]
    textfilepath = sys.argv[3]
    startEncode(imagefilepath, textfilepath)
elif process == 'd':
    imagefilepath = sys.argv[2]
    startDecode(imagefilepath)