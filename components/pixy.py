"""
File Author: Ben Veltman
File Creation Date: 02/16/2016
File Purpose: Communicate with Pixy camera
"""

from wpilib import I2C
from . import Component
from ctypes import c_uint8, c_uint16

class Pixy(Component):
    """
    Pixy object tracking camera

    Packet Format (little endian):
    Bytes    16-bit word    Description
    ----------------------------------------------------------------
    0, 1     y              sync: 0xaa55=normal object, 0xaa56=color code object
    2, 3     y              checksum (sum of all 16-bit words 2-6)
    4, 5     y              signature number
    6, 7     y              x center of object
    8, 9     y              y center of object
    10, 11   y              width of object
    12, 13   y              height of object

    Servo Control:
    Bytes    16-bit word   Description
    ----------------------------------------------------------------
    0, 1     y             servo sync (0xff00)
    2, 3     y             servo 0 (pan) position, between 0 and 1000
    4, 5     y             servo 1 (tilt) position, between 0 and 1000

    Camera Brightness:
    Bytes    16-bit word   Description
    ----------------------------------------------------------------
    0, 1     y             camera brightness sync (0xfe00)
    2        n             brightness value

    LED control:
    Bytes    16-bit word   Description
    ----------------------------------------------------------------
    0, 1     y             LED sync (0xfd00)
    2        n             red value
    3        n             green value
    4        n             blue value
    """

    PIXY_I2C_ADDR = 0x54
    PIXY_START_WORD = 0xAA55
    PIXY_START_WORD_CC = 0xAA56

    class Block:
        def __init__(self, sig, xPos, yPos, widthSize, heightSize):
            self.signature = sig
            self.x = xPos
            self.y = yPos
            self.width = widthSize
            self.height = heightSize

        def getX(self):
            return self.x

        def getY(self):
            return self.y

        def getSignature(self):
            return self.signature

        def getWidth(self):
            return self.width

        def getHeight(self):
            return self.height

        def getArea(self):
            return self.height*self.width

    def __init__(self, address = PIXY_I2C_ADDR, port = 0, simPort = None):
        self.addr = address
        self.conn = I2C(I2C.Port.kOnboard, self.addr)   # Create the i2c connection


    def setAddr(self, address):
        '''Set a new i2c address and create a connection to the new address'''
        self.addr = address                             # Set new address
        self.conn = I2C(I2C.Port.kOnboard, self.addr)   # Create the i2c connection


    # Get a 16 bit word from the i2c bus
    def getWord(self):
        '''Get a 16 bit word from the i2c bus'''
        return self.conn.readOnly(2)                    # Read two bytes of data from the i2c bus


    def getByte(self):
        '''Get a byte from the i2c bus'''
        return self.conn.readOnly(1)                    # Read one byte of data from the i2c bus


    def getMessage(self):
        '''Get the full 14 byte message from Pixy'''
        data = []

        for i in range(14):
            data[i] = self.getWord()

        return data


    def setPanTiltPos(self, pan, tilt):
        '''Set the position of the pan/tilt servo mount'''
        # Assemble the byte array
        sync0 = 0x00
        sync1 = 0xFF
        pan0 = pan & 0xFF
        pan1 = (pan>>8) & 0xFF
        tilt0 = tilt & 0xFF
        tilt1 = (tilt>>8) & 0xFF
        data = [sync0, sync1, pan0, pan1, tilt0, tilt1]

        return self.conn.writeBulk(data)


    def setBrightness(self, brightness):
        '''Set the brightness of the camera'''
        # Assemble the byte array
        sync0 = 0x00
        sync1 = 0xFE
        brightness0 = brightness & 0xFF
        brightness1 = (brightness>>8) & 0xFF
        data = [sync0, sync1, brightness0, brightness1]

        return self.conn.writeBulk(data)


    def setLED(self, red, green, blue):
        '''Set the color of the Pixy onboard LED'''
        # Assemble the byte array
        sync0 = 0x00
        sync1 = 0xFD
        red &= 0xFF
        green &= 0xFF
        blue &= 0xFF
        data = [sync0, sync1, red, green, blue]

        return self.conn.writeBulk(data)


    def getNextBlock(self):
        '''Get the next block on the i2c bus'''
        data = []
        sum = 0

        # Get the data
        for i in range(0,7):
            data[i] = self.getWord()

        dataBlock = self.Block(data[2], data[3], data[4], data[5], data[6])  # Build the block object

        # Check the checksum
        for i in range(2,6):
            sum += data[i]

        if sum == data[1]:
            return dataBlock
        else:
            return False


    def getBlocks(self):
        '''Get a list of the blocks detected by the camera in a single frame'''

        blocks = []

        for blockCount in range(0,100):
            checksum = self.getWord()

            if checksum == self.PIXY_START_WORD:       # New frame started
                blockType = NORMAL_BLOCK
                return blocks
            elif checksum == self.PIXY_START_WORD_CC:
                blockType = CC_BLOCK
                return blocks
            elif checksum == 0:
                return blocks

            blocks.append(self.getNextBlock())
