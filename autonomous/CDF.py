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

    MODE_NAME = 'CDF'
    DEFAULT = False
    DRIVE_DISTANCE = 190

    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_forward_step_1')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def move_arm_to_0(self):
        while(self.arm.getPOT() >= 0.5):
            self.arm.armAuto(0,1,0,rate=0.5)

        self.arm.armAuto(0,0,0.5)

        self.next_state('drive_forward_step_2')

    @state()
    def move_arm_to_30(self):
        while(self.arm.getPOT() <= 30):
            self.arm.armAuto(1,0,30,rate=0.7)

            self.arm.armAuto(0,0,30)

            self.next_state('drive_forward_step_3')

    @state()
    def drive_forward_step_3(self):
        if self.drive.getAutonDistance() <= 77 :
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.drive.next_state('done')


    @state()
    def drive_forward_step_1(self):
        if self.drive.getAutonDistance() <= 55 :
            self.drive.autonTankDrive(0.5, 0.5)
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.next_state('move_arm_to_0')

    @state()
    def drive_forward_step_2(self):
        if self.drive.getAutonDistance() <= 17 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.next_state('move_arm_to_30')

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
