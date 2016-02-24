"""
File Author: Will Lowry
File Creation Date: 2/11/2016
File Purpose: To create a skeleton autonomous mode starting from position one
"""

from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
#from components.armControl import arm


class autonomousModeFromFirstPosition(StatefulAutonomous):

    MODE_NAME = 'First Position Auto'
    DEFAULT = True

    chooser = SendableChooser()
    default_modes = []
    iCount = 0
    #dt = driveTrain()

    def Initialize(self):
        pass

# A positive motor value for the ARM makes it go down
# A positive motor value for the WHEEL makes them take in the ball

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='arm_up')
    def drive_stop(self) :
        self.drive.reset()
        self.drive.autonTankDrive(0, 0)

    @state()
    def arm_up(self) :
        if self.arm.getPOT() <= 4 :
            self.arm.armAuto(1, 0)
        else :
            self.arm.armAuto(0,0)
            self.next_state('drive_forward_towards_ball')

    @state()
    def drive_forward_towards_ball(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 14 :
            self.drive.autonTankDrive(0.4, 0.4)
            self.arm.wheelSpin()
        else :
            self.drive.reset()
            self.next_state('rotate_away_from_ball')
    '''
    @state()
    def arm_down_to_take_in_ball(self) :
        if self.arm.getPOT() >= 7:
            self.arm.armAuto(0, 1)
        else :
            self.arm.armAuto(0,0)
            self.next_state('take_in_ball')

    @state()
    def take_in_ball(self) :
        if self.iCount <= 100:
            self.arm.wheelSpin()
            self.iCount += 1
        else:
            self.arm.wheelSpin(speed=0)
            self.next_state('rotate_away_from_ball')
    '''
    @state()
    def rotate_away_from_ball(self):
        self.drive.turn_angle(180)
        self.next_state('drive_forward_away_from_ball')


    @state()
    def drive_forward_away_from_ball(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 19 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('rotate_to_the_left')

    @state()
    def rotate_to_the_left(self):
        self.drive.turn_angle(-37)
        self.next_state('drive_forward_towards_defense')

    @state()
    def drive_forward_towards_defense(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 34 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('rotate_towards_defense')

    @state()
    def rotate_towards_defense(self):
        self.drive.turn_angle(37)
        self.next_state('drive_forward_towards_crossing_defense')

    @state()
    def drive_forward_towards_crossing_defense(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 17 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('drive_forward_crossing_defense')

    @state()
    def drive_forward_crossing_defense(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 76 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('rotate_towards_goal')

    @state()
    def rotate_towards_goal(self):
        self.drive.turn_angle(7)
        self.next_state('drive_forward_towards_goal')

    @state()
    def drive_forward_towards_goal(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 143 :
            self.drive.autonTankDrive(-0.4, -0.4)
        else :
            self.drive.reset()
            self.next_state('rotate_towards_scoring')

    @state()
    def spin_around(self) :
        self.turn_angle(180)
        self.next_state('rotate_towards_scoring')

    @state()
    def rotate_towards_scoring(self):
        self.drive.turn_angle(-48)
        self.next_state('drive_forward_towards_scoring')

    @state()
    def drive_forward_towards_scoring(self) :
        if (abs(self.drive.lfencoder.getDistance()) + abs(self.drive.rfencoder.getDistance()))/2 <= 94 :
            self.drive.autonTankDrive(0.4, 0.4)
        else :
            self.drive.reset()
            self.next_state('done')

    @state()
    def done(self) :
        pass
