import main

def main__byteLongStringCursor1():
    binobj = main.BinaryObject(b"", "little")
    binobj.appendByte(23)
    binobj.insertLongAt(6000, 1)
    binobj.appendString("This is cool!")
    binobj.appendString("This is not cool!")
    binobj.cursor -= len("This is not cool!")
    print(binobj.cursor, binobj.data, len(binobj.data))
    print(binobj.data[:binobj.cursor])
    print(binobj.getString(binobj.cursor, len("This is cool!")))
    print(binobj.getString(binobj.cursor, len("This is not cool!")))


def main_bankExample():
    binobj = main.BinaryObject(b"", "little")
    for i in [1, 2, 3, 4, 5]:
        binobj.appendByte(i)

    print(binobj.data)
    binobj.saveToBank("ascension 1 to 5")
    binobj.resetData()
    print(binobj.banks)
    dumped = binobj.dumpBanks()
    print(dumped)
    print(main.pickle.loads(dumped))

print(__name__)
if __name__ == "__main__":
    # main__byteLongStringCursor1() # Example program that demonstrates the appending feature, insertion feature, cursor feature, and the reading feature.
    main_bankExample()  # Example program that demonstrates the bank feature, as well as the bank dumping feature.