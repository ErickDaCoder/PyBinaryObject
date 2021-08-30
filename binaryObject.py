#------------------------- Binary Editor -------------------------#
# This file allows you to interact with binary files. This was    #
# originally a blind port of the Binary Object made by Third Eye  #
# Entertainment for Clickteam Fusion.                             #
#-----------------------------------------------------------------#


import struct # For the float converter
import pickle # For the dictionary dumper
import zlib # For the compressor (this is the original compression module used by the Clickteam Fusion variant)

class BinaryObject:
    def __init__(self, indata, endianness):
        self.data = indata
        self.endianness = endianness
        self.banks = {}
        self.cursor = 0
    
    # --------------- Decoder ---------------
    
    def getString(self, position, length):
        return self.data[:position + length][-length:]
    
    def getByte(self, position):
        return int.from_bytes(self.data[:position + 1][-1:], byteorder = self.endianness)
    
    def getShort(self, position):
        return int.from_bytes(self.data[:position + 2][-2:], byteorder = self.endianness)
    
    def getLong(self, position):
        return int.from_bytes(self.data[:position + 4][-4:], byteorder = self.endianness)
    
    def getFloat(self, position):
        return struct.unpack(( (">" if self.endianness == "big" else "<") + "f"), self.data[:position + 4][-4:])[0]
    
    def loadFromBank(self, bankname):
        self.data = self.banks[bankname]
    
    # --------------- Encoder ---------------
    # * - Converters
    def convertByte(self, byteValue):
        return byteValue.to_bytes(1, byteorder = self.endianness)
    
    def convertShort(self, shortValue):
        return shortValue.to_bytes(2, byteorder = self.endianness)
    
    def convertLong(self, longValue):
        return longValue.to_bytes(4, byteorder = self.endianness)
    
    def convertFloat(self, floatValue):
        return struct.pack(( (">" if self.endianness == "big" else "<") + "f"), floatValue )
    
    # * - Appenders, inserters, and saver
    
    def insertStringAt(self, position, string):
        self.data = self.data[:position] + string.encode("ascii") + self.data[position:]
        self.cursor += len(string)
    
    def insertByteAt(self, position, byteValue):
        self.data = self.data[:position] + self.convertByte(byteValue) + self.data[position:]
        self.cursor += 1
    
    def insertShortAt(self, position, shortValue):
        self.data = self.data[:position] + self.convertShort(shortValue) + self.data[position:]
        self.cursor += 2
    
    def insertLongAt(self, position, longValue):
        self.data = self.data[:position] + self.convertLong(longValue) + self.data[position:]
        self.cursor += 4
    
    def insertFloatAt(self, position, floatValue):
        self.data = self.data[:position] + self.convertFloat(floatValue) + self.data[position:]
        self.cursor += 4
    
    def appendString(self, string):
        self.data += (str.encode(string, "ascii"))
        self.cursor += len(string)
    
    def appendByte(self, byteValue):
        self.data += self.convertByte(byteValue)
        self.cursor += 1
    
    def appendShort(self, shortValue):
        self.data += self.convertShort(shortValue)
        self.cursor += 2
    
    def appendLong(self, longValue):
        self.data += self.convertLong(longValue)
        self.cursor += 4
    
    def appendFloat(self, floatValue):
        self.data += self.convertFloat(floatValue)
        self.cursor += 4
    
    def saveToBank(self, bankname):
        self.banks[bankname] = self.data
    
    # --------------- Miscellaneous ---------------
    
    def removeBank(self, bankName):
        del self.banks[bankName]
    
    def dumpBanks(self):
        return pickle.dumps(self.banks)
    
    def loadDumpedBanks(self, pickledBanks):
        self.banks = pickle.loads(pickledBanks)
    
    def resetData(self):
        self.data = b""
        self.cursor = 0
    
    def resetBanks(self):
        self.banks = {}
    
    def compressData(self, compressLevel):
        self.data = zlib.compress(self.data, level=compressLevel)
    
    def decompressData(self):
        self.data = zlib.decompress(self.data)
    
    def removeBytes(self, position, nBytes):
        self.data = self.data[:position] + self.data[position+nBytes:]
