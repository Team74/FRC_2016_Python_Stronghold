"""
File Author: Will Lowry
File Creation Date: 1/28/2015
File Purpose: To create our drive functions
"""
import wpilib
from wpilib import CANTalon, Encoder, Timer, RobotDrive
from wpilib.interfaces import Gyro
from xbox import XboxController
from . import Component

class driveTrain(Component) :

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Constants
        WHEEL_DIAMETER = 6
        PI = 3.1415
        ENCODER_TICK_COUNT = 250
        ENCODER_GOAL = 0 # default
        ENCODER_TOLERANCE = 1 # inch
        self.CONTROL_TYPE = 1 # 0 = disable PID components and encoder components

        self.lmotor = CANTalon(0)
        self.rmotor = CANTalon(1)

        self.drive = RobotDrive(self.lmotor, self.rmotor)

        if self.CONTROL_TYPE:
            # Initializing the encoders
            self.lencoder = Encoder(0, 1, False, Encoder.EncodingType.k4X) #Creates an object of type Encoder, called lencoder. It counts
            self.rencoder = Encoder(2, 3, True, Encoder.EncodingType.k4X) #the amount that a motor has rotated, and returns it in Direction and Distance variables

            # Set the distance per encoder tick
            self.lencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
            self.rencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)

            # Initializing PID Controls
            self.pidRight = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.rencoder, self.rmotor, 0.02)
            self.pidLeft = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.lencoder, self.lmotor, 0.02)

            # PID Settings
            self.pidRight.setContinuous(False)
            self.pidLeft.setContinuous(False)
            self.pidRight.setAbsoluteTolerance(0.05)
            self.pidLeft.setAbsoluteTolerance(0.05)
            self.pidRight.setOutputRange(-1, 1)
            self.pidLeft.setOutputRange(-1, 1)

            wpilib.LiveWindow.addSensor("Drive Train", "Left Encoder", self.lencoder)
            wpilib.LiveWindow.addSensor("Drive Train", "Right Encoder", self.rencoder)
            wpilib.LiveWindow.addActuator("Drive Trian", "Right PID", self.pidRight)
            wpilib.LiveWindow.addActuator("Drive Trian", "Left PID", self.pidLeft)

        self.controller = XboxController(0)

        self.autonomousSpeed = 0.2

        self.dashTimer = Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Adding components to the LiveWindow (testing)
        wpilib.LiveWindow.addActuator("Drive Train", "Front Left Motor", self.lmotor)
        #wpilib.LiveWindow.addActuator("Drive Train", "Back Left Motor", self.back_left_motor)
        wpilib.LiveWindow.addActuator("Drive Train", "Front Right Motor", self.rmotor)
        #wpilib.LiveWindow.addActuator("Drive Train", "Back Right Motor", self.back_right_motor)


    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        if self.CONTROL_TYPE:
            wpilib.SmartDashboard.putNumber("Left Distance", self.lencoder.getDistance())
            wpilib.SmartDashboard.putNumber("Right Distance", self.rencoder.getDistance())
            wpilib.SmartDashboard.putNumber("Left Speed", self.lencoder.getRate())
            wpilib.SmartDashboard.putNumber("Right Speed", self.rencoder.getRate())
            #wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

# drive forward function
    def drive_forward(self, speed) :
        self.lmotor.set(speed)
        self.rmotor.set(speed)

# manual drive function for Tank Drive
    def xboxTankDrive(self, leftSpeed, rightSpeed):
        self.lmotor.set(leftSpeed)
        self.rmotor.set(rightSpeed)

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
        if self.CONTROL_TYPE:
            self.lencoder.reset()
            self.rencoder.reset()

# function to turn a certain number of degrees
    def turn_angle(self):
        print('Turn Angle')


    def getDistance(self):
        return (self.lencoder.getDistance() + self.rencoder.getDistance())/2.0
