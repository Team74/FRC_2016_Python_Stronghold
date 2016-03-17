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

    MODE_NAME = 'Low Bar'
    DEFAULT = True
    DRIVE_DISTANCE = 300

    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_forward')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forward(self) :
        if self.drive.getAutonDistance() <= self.DRIVE_DISTANCE :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('done')

    @state()
    def done(self) :
        self.drive.autonTankDrive(0, 0)
