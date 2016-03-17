"""
File Author: Will Lowry
File Creation Date: 2/20/2016
File Purpose: To create a skeleton autonomous mode starting from position five
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
from components.armControl import arm

class autonomousModeFromFifthPosition(StatefulAutonomous):

    MODE_NAME = 'Fifth Position Auto'
    DEFAULT = False

    chooser = SendableChooser()
    default_modes = []

    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_forward_towards_ball')
    def drive_stop(self) :
        self.drive.autonTankDrive(0, 0)

    @state()
    def drive_forward_towards_ball(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 16 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('arm_down_to_take_in_ball')

    @state()
    def arm_down_to_take_in_ball(self) :
        if self.backSwitch.get() == True :
            self.armMotor(0.5)
        else :
            self.next_state('take_in_ball')

    @timed_state(first=False, duration=1.0, next_state='rotate_away_from_ball')
    def take_in_ball(self) :
        self.arm.wheelSpin()

    @state()
    def rotate_away_from_ball(self):
        self.drive.turn_angle(180)
        self.next_state('drive_forward_away_from_ball')

    @state()
    def drive_forward_away_from_ball(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 19 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('rotate_to_the_left')

    @state()
    def rotate_to_the_left(self):
        self.drive.turn_angle(83)
        self.next_state('drive_forward_towards_defense')

    @state()
    def drive_forward_towards_defense(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 194 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('rotate_towards_defense')

    @state()
    def rotate_towards_defense(self):
        self.drive.turn_angle(-83)
        self.next_state('drive_forward_towards_crossing_defense')

    @state()
    def drive_forward_towards_crossing_defense(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 17 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('drive_forward_crossing_defense')

    @state()
    def drive_forward_crossing_defense(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 76 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('rotate_towards_goal')

    @state()
    def rotate_towards_goal(self):
        self.drive.turn_angle(-7)
        self.next_state('drive_forward_towards_goal')

    @state()
    def drive_forward_towards_goal(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 143 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('rotate_towards_scoring')

    @state()
    def rotate_towards_scoring(self):
        self.drive.turn_angle(-48)
        self.next_state('drive_forward_towards_scoring')

    @state()
    def drive_forward_towards_scoring(self) :
        if (self.drive.lfencoder.getDistance() + self.drive.rfencoder.getDistance()) <= 94 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.next_state('done')

    @state()
    def done(self) :
        pass
