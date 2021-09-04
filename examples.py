from binaryobject import BinaryObject
def main__byteLongStringCursor1():
    binobj = BinaryObject(b"", "little")
    binobj.appendByte(23)
    binobj.insertLongAt(6000, 1)
    binobj.appendString("This is cool!")
    binobj.appendString("This is not cool!")
    binobj.cursor -= len("This is not cool!")
    print( binobj.cursor, binobj.data, len(binobj.data) )
    print( binobj.data[:binobj.cursor] )
    print( binobj.getString( binobj.cursor, len("This is cool!")) )
    print( binobj.getString(binobj.cursor, len("This is not cool!")) )

def main__bankExample():
    binobj = BinaryObject(b"", "little")
    for i in range(1, 6):
        binobj.appendByte(i)
    
    print(binobj.data)
    binobj.saveToBank("ascension 1 to 5")
    binobj.resetData()
    print(binobj.banks)
    dumped = binobj.dumpBanks()
    print(dumped)
    print(binobj.loadDumpedBanks(dumped))

def main__saveExample():
    b = BinaryObject(b"", "little")
    b.appendByte( len("Cool String!") )
    b.appendString("Cool String!")
    b.appendString("NNNNNNNNNNNN")
    with open("binaryobjecttest.txt", "wb") as f:
        f.write(b.data)

def main__loadExample():
    with open("binaryobjecttest.txt", "rb") as f:
        b = BinaryObject(f.read(), "little")
    
    print(b.data)
    print(b.getString(1, b.getByte(0) ))

def main__conditional():
    b = BinaryObject(b"", "little")
    b.appendByte(120)
    b.appendByte(38)
    b.saveToBank("MyBank")
    if b.bankExists("MyBank"):
        print("Bank exists.")
    
def main__dataAddress():
    b = BinaryObject(b"", "little")
    print(b.getPointerToData())

def main__md5hash():
    b = BinaryObject(b"", "little")
    b.appendLong(128183)
    b.appendLong(239818)
    b.appendLong(287631)
    print(b.getMD5Signature())

def main__sha512hash():
    b = BinaryObject(b"", "little")
    b.appendLong(128183)
    b.appendLong(239818)
    b.appendLong(287631)
    print(b.getSHA256Hash())

if __name__ == "__main__":
    main__byteLongStringCursor1() # Example program that demonstrates the appending feature, insertion feature, cursor feature, and the reading feature.
    main__bankExample() # Example program that demonstrates the bank feature, as well as the bank dumping feature.
    main__saveExample()
    main__loadExample()
    main__conditional()
    main__dataAddress()
    main__md5hash()
    main__sha512hash()
