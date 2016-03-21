"""
File Author: Will Lowry
File Creation Date: 2/23/2016
File Purpose: To create a skeleton autonomous mode testing the low bar
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
#from components.armControl import arm


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'Rock Wall'
    DEFAULT = False
    DRIVE_DISTANCE = 175

    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='move_arm')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def move_arm(self):
        while(self.arm.getPOT() >= 25):
            self.arm.armAuto(0,1,25,rate=0.5)

        self.arm.armAuto(0,0,25)

        self.next_state('drive_forward')

    @state()
    def drive_forward(self) :
        if self.drive.getAutonDistance() <= self.DRIVE_DISTANCE :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.drive.reset()
            self.next_state('done')

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
