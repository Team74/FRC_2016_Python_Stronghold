"""
File Author: Will Lowry
File Creation Date: 2/11/2016
File Purpose: To create a skeleton autonomous
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
from components.drive import driveTrain

class skeletonAutonomous(StatefulAutonomous):

    MODE_NAME = 'skeletonAutonomous'
    DEFAULT = False

    chooser = SendableChooser()
    default_modes = []

    #dt = driveTrain()

    def Initialize(self):
        pass

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='turn_angle')
    def drive_stop(self):
        self.drive.xboxTankDrive(0,0)

    @state()
    def swerve(self):
        self.drive.turn_angle(180)
        self.next_state(self.done)

    @state()
    def done(self) :
        pass
