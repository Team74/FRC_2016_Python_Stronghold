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

    MODE_NAME = 'Low Bar Test'
    DEFAULT = False

    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_forwards_through_low_bar')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forwards_through_low_bar(self) :
        if self.drive.getDistance() <= 192 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('turn_towards_scoring')

    @state()
    def turn_towards_scoring(self) :
        self.drive.turn_angle(115)
        self.drive.reset()
        self.next_state('drive_forward_towards_scoring_01')

    @state()
    def drive_forward_towards_scoring_01(self) :
        if self.drive.getDistance() <= 108 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.drive.reset()
            self.next_state('done')

    @state()
    def done(self) :
        pass
