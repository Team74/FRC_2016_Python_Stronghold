from wpilib.smartdashboard import SmartDashboard
import random

class mySmartDash:
    def __init__(self):
        self.sd = SmartDashboard()

    def sendNumber(self, key, val):
        self.sd.putNumber(key, val)

    def sendRandomData(self, upper, lower):
        sendNumber(self, "Random", random.randrange(upper, lower))
