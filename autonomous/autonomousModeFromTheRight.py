"""
File Author: Will Lowry
File Creation Date: 2/11/2016
File Purpose: To create a skeleton autonomous mode starting from the right
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser

class autonomousModeFromTheRight(StatefulAutonomous):

    MODE_NAME = 'autonomousModeFromTheRight'
    DEFAULT = False

    chooser = SendableChooser()
    default_modes = []

    #dt = driveTrain()

    def Initialize(self):
        pass

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_forward_towards_ball')
    def drive_stop(self) :
        self.drive.xboxTankDrive(0, 0)

    @state()
    def drive_forward_towards_ball(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 16 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.swerve_away_from_ball)

    @state()
    def swerve_away_from_ball(self):
        self.drive.turn_angle(180)
        self.next_state(self.drive_forward_away_from_ball)

    @state()
    def drive_forward_away_from_ball(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 19 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.swerve_to_the_left)

    @state()
    def swerve_to_the_left(self):
        self.drive.turn_angle(37)
        self.next_state(self.drive_forward_towards_defense)

    @state()
    def drive_forward_towards_defense(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 34 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.swerve_towards_defense)

    @state()
    def swerve_towards_defense(self):
        self.drive.turn_angle(-37)
        self.next_state(self.drive_forward_towards_crossing_defense)

    @state()
    def drive_forward_towards_crossing_defense(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 17 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.drive_forward_crossing_defense)

    @state()
    def drive_forward_crossing_defense(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 76 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.swerve_towards_goal)

    @state()
    def swerve_towards_goal(self):
        self.drive.turn_angle(-7)
        self.next_state(self.drive_forward_towards_goal)

    @state()
    def drive_forward_towards_goal(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 143 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.swerve_towards_scoring)

    @state()
    def swerve_towards_scoring(self):
        self.drive.turn_angle(-48)
        self.next_state(self.drive_forward_towards_scoring)

    @state()
    def drive_forward_towards_scoring(self) :
        while (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 94 :
            self.drive.xboxTankDrive(0.4, 0.4)
        self.next_state(self.done)

    @state()
    def done(self) :
        pass
