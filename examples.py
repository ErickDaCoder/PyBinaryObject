import binaryobject
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
    print(pickle.loads(dumped))

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

if __name__ == "__main__":
    # main__byteLongStringCursor1() # Example program that demonstrates the appending feature, insertion feature, cursor feature, and the reading feature.
    #main_bankExample() # Example program that demonstrates the bank feature, as well as the bank dumping feature.
    main__saveExample()
    main__loadExample()
