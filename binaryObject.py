#------------------------- Binary Editor -------------------------#
# This file allows you to interact with binary files. This was    #
# originally a blind port of the Binary Object made by Third Eye  #
# Entertainment for Clickteam Fusion.                             #
#-----------------------------------------------------------------#
from struct import pack, unpack # For the float converter
from pickle import dumps, loads # For the dictionary dumper
from zlib import compress, decompress# For the compressor (this is the original compression module used by the Clickteam Fusion variant)
from hashlib import md5, sha256 # For the MD5 hash function. SHA512 is a new feature that was not present in the original.
from base64 import b64decode, b64encode

class BinaryObject:
    def __init__(self, indata, endianness):
        self.data = indata
        self.endianness = endianness
        self.banks = {}
        self.cursor = 0
    
    # --- Conditions:
    
    def bankExists(self, bankName):
        return bankName in self.banks
    
    # --- Actions:
    
    def convertByte(self, byteValue):
        return byteValue.to_bytes(1, byteorder = self.endianness)
    
    def convertShort(self, shortValue):
        return shortValue.to_bytes(2, byteorder = self.endianness)
    
    def convertLong(self, longValue):
        return longValue.to_bytes(4, byteorder = self.endianness)
    
    def convertFloat(self, floatValue): # Uses struct.pack
        return pack(( (">" if self.endianness == "big" else "<") + "f"), floatValue )
    
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
    
    def loadFromBank(self, bankname):
        self.data = self.banks[bankname]
    
    def saveToBank(self, bankname):
        self.banks[bankname] = self.data
    
    def removeBank(self, bankName):
        del self.banks[bankName]
    
    def dumpBanks(self): # Uses pickle.dumps
        return dumps(self.banks)
    
    def loadDumpedBanks(self, dumpedBanks): # Uses pickle.loads
        self.banks = loads(dumpedBanks)
    
    def resetData(self):
        self.data = b""
        self.cursor = 0
    
    def resetBanks(self):
        self.banks = {}
    
    def compressData(self, compressLevel=5): # Uses zlib.compress
        self.data = compress(self.data, level=compressLevel)
    
    def decompressData(self): # Uses zlib.decompress
        self.data = decompress(self.data)
    
    def removeBytes(self, position, nBytes):
        self.data = self.data[:position] + self.data[position+nBytes:]
        self.cursor -= nBytes
    
    def base64EncodeData(self):
        self.data = b64encode(self.data)
    
    def base64DecodeData(self):
        self.data = b64decode(self.data)
    
    # --- Expressions:
    
    def getByteSize(self):
        return 1
    
    def getShortSize(self):
        return 2
    
    def getLongSize(self):
        return 4
    
    def getFloatSize(self):
        return 4
    
    def getString(self, position, length):
        return self.data[:position + length][-length:]
    
    def getByte(self, position):
        return int.from_bytes(self.data[:position + 1][-1:], byteorder = self.endianness)
    
    def getShort(self, position):
        return int.from_bytes(self.data[:position + 2][-2:], byteorder = self.endianness)
    
    def getLong(self, position):
        return int.from_bytes(self.data[:position + 4][-4:], byteorder = self.endianness)
    
    def getFloat(self, position): # Uses struct.unpack
        return unpack(( (">" if self.endianness == "big" else "<") + "f"), self.data[:position + 4][-4:])[0]
    
    def getPointerToData(self):
        return hex(id(self.data))
    
    def getMD5Signature(self):
        return md5(self.data).hexdigest()
    
    def getSHA256Hash(self):
        return sha256(self.data).hexdigest()
