"""
File Author: Will Lowry
File Creation Date: 1/28/2015
File Purpose: To create our drive functions
"""
import wpilib
import math
from wpilib import CANTalon, Encoder, Timer, RobotDrive
from wpilib.interfaces import Gyro
from xbox import XboxController
from . import Component

class driveTrain(Component) :

    def __init__(self, robot):

        self.robot = robot

        # Constants
        WHEEL_DIAMETER = 6
        PI = 3.1415
        ENCODER_TICK_COUNT = 250
        ENCODER_GOAL = 0 # default
        ENCODER_TOLERANCE = 1 # inch

        self.lmotor = CANTalon(0)
        self.rmotor = CANTalon(1)

        # Set to correct control mode
        #self.lmotor.changeControlMode(self.lmotor.ControlMode.Speed)
        #self.rmotor.changeControlMode(self.rmotor.ControlMode.Speed)

        self.drive = RobotDrive(self.lmotor, self.rmotor)
        self.drive.setSafetyEnabled(True)
        self.drive.setExpiration(0.1)
        self.drive.setSensitivity(0.5)
        self.drive.setMaxOutput(1.0)
        #self.drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontLeft, True)
        #self.drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kFrontRight, True)
        #self.drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearLeft, True)
        #self.drive.setInvertedMotor(wpilib.RobotDrive.MotorType.kRearRight, True)

        self.lencoder = Encoder(0, 1) #Creates an object of type Encoder, called lencoder. It counts
        self.rencoder = Encoder(2, 3) #the amount that a motor has rotated, and returns it in Direction and Distance variables

        self.lencoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kRate)
        self.rencoder.setPIDSourceType(wpilib.Encoder.PIDSourceType.kRate)


        # Set the distance per encoder tick
        self.lencoder.setDistancePerPulse(WHEEL_DIAMETER*math.pi/ENCODER_TICK_COUNT)
        self.rencoder.setDistancePerPulse(WHEEL_DIAMETER*math.pi/ENCODER_TICK_COUNT)


        # Setup motor feedback sensors
        #self.lmotor.setFeedbackDevice(self.lencoder.getRaw())
        #self.rmotor.setFeedbackDevice(self.rencoder.getRaw())


        self.controller = XboxController(0)

        self.autonomousSpeed = 0.2

        self.dashTimer = Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        wpilib.LiveWindow.addActuator("Drive Train", "Front Left Motor", self.lmotor)
        #wpilib.LiveWindow.addActuator("Drive Train", "Back Left Motor", self.back_left_motor)
        wpilib.LiveWindow.addActuator("Drive Train", "Front Right Motor", self.rmotor)
        #wpilib.LiveWindow.addActuator("Drive Train", "Back Right Motor", self.back_right_motor)
        wpilib.LiveWindow.addSensor("Drive Train", "Left Encoder", self.lencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Right Encoder", self.rencoder)
        super().__init__()


    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        wpilib.SmartDashboard.putNumber("Left Distance", self.lencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Right Distance", self.rencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Left Speed", self.lencoder.getRate())
        wpilib.SmartDashboard.putNumber("Right Speed", self.rencoder.getRate())
        #wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

    # Allow manual driving of the robot in tank drive mode
    def driveManual(self, left, right):
        self.drive.tankDrive(left, right)

    def driveLeftSide(self, speed):
        self.lmotor.set(speed)

    def driveRightSide(self, speed):
        self.rmotor.set(speed)

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
        l_error = self.encoder_goal - self.lencoder.getDistance()
        r_error = self.encoder_goal - self.rencoder.getDistance()
        return abs(l_error) < self.encoder_tolerance and abs(r_error) < self.encoder_tolerance

# function to continue driving if not at goal distance
    def drive_distance(self) :
        while not at_drive_goal() :
            self.drive_forward(self.autonomousSpeed)

        self.drive_stop()

# fucntion to reset the gyro
    def reset(self):
        self.lencoder.reset()
        self.rencoder.reset()

# function to turn a certain number of degrees
    def turn_angle(self):
        print('Turn Angle')


    def getDistance(self):
        return (self.lencoder.getDistance() + self.rencoder.getDistance())/2.0

    def getLeftRate(self):
        return self.lencoder.getRate()

    def getRightRate(self):
        return self.rencoder.getRate()

    def getRightEnc(self):
        return self.rencoder

    def getLeftEnc(self):
        return self.lencoder

    def getRightMotor(self):
        return self.rmotor

    def getLeftMotor(self):
        return self.lmotor
