"""
File Author: Will Lowry
File Creation Date: 1/28/2015
File Purpose: To create our drive functions
"""
from wpilib import CANTalon, Encoder, Timer
from wpilib.interfaces import Gyro
from xbox import XboxController
from . import Component

class driveTrain(Component) :

    # Constants
    WHEEL_DIAMETER = 6
    PI = 3.1415
    ENCODER_TICK_COUNT = 250
    ENCODER_GOAL = 0 # default
    ENCODER_TOLERANCE = 1 # inch

    lencoder = Encoder(0, 1) #Creates an object of type Encoder, called lencoder. It counts
    rencoder = Encoder(2, 3) #the amount that a motor has rotated, and returns it in Direction and Distance variables
    lencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
    rencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)

    controller = XboxController(0)

    lmotor = CANTalon(0)
    rmotor = CANTalon(1)
    autonomousSpeed = 0.2

    dashTimer = Timer()     # Timer for SmartDashboard updating
    dashTimer.start()

# drive forward function
    def drive_forward(self, speed) :
        self.lmotor.set(speed)
        self.rmotor.set(speed)

# stop function
    def drive_stop(self) :
        self.lmotor.set(0)
        self.rmotor.set(0)

# function to tell us whether or not the goal distance has been reached
    def at_distance_goal(self):
        l_error = self.encoder_goal - self.l_encoder.getDistance()
        r_error = self.encoder_goal - self.r_encoder.getDistance()
        return abs(l_error) < self.encoder_tolerance and abs(r_error) < self.encoder_tolerance

# function to continue driving if not at goal distance
    def drive_distance(self) :
        while not at_drive_goal() :
            self.drive_forward(self.autonomousSpeed)

        self.drive_stop()

# fucntion to reset the gyro
    def reset(self):
        print("Reset")
# function to turn a certain number of degrees
    def turn_angle(self):
        print('Turn Angle')
