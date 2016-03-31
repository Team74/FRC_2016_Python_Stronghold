"""
File Author: Will Hescott
File Creation Date: 2/23/2016
File Purpose: Work, damn you!
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser, Timer
#from components.armControl import arm


class autonomousModeTestingLowBar(StatefulAutonomous):

    MODE_NAME = 'CDFnoarm'
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
        '''while(self.arm.getPOT() >= 0.5):
            self.arm.armAuto(0,1,0,rate=0.5)

        self.arm.armAuto(0,0,0.5)
        '''
        Timer.delay(3)
        self.next_state('drive_forward_step_2')

    @state()
    def move_arm_to_30(self):
        '''while(self.arm.getPOT() <= 30):
            self.arm.armAuto(1,0,30,rate=0.7)

            self.arm.armAuto(0,0,30)
        '''
        Timer.delay(3)
        self.next_state('drive_forward_step_3')

    @state()
    def drive_forward_step_3(self):
        if self.drive.getAutonDistance() <= 77 :
            self.drive.autonTankDrive(0.3, 0.3)
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.next_state('done')


    @state()
    def drive_forward_step_1(self):
        if self.drive.getAutonDistance() <= 50 :
            self.drive.autonTankDrive(0.3, 0.3)
            #Timer.delay(3)
            #print("Test Sucessful")
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.next_state('move_arm_to_0')

    @state()
    def drive_forward_step_2(self):
        if self.drive.getAutonDistance() <= 19 :
            self.drive.autonTankDrive(0.3, 0.3)
        else :
            self.drive.reset()
            self.drive.autonTankDrive(0,0)
            self.next_state('move_arm_to_30')

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
