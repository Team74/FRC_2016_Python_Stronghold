#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.drive import driveTrain
from robotpy_ext.autonomous.selector import AutonomousModeSelector
#from pyfrc.sim.pygame_joysticks import UsbJoysticks
#import pygame

# to stay in sync with our driver station
CONTROL_LOOP_WAIT_TIME = 0.005#0.025

class MyRobot(wpilib.SampleRobot):

    # Constants
    WHEEL_DIAMETER = 6
    PI = 3.1415
    ENCODER_TICK_COUNT = 250

    def robotInit(self):
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)
        self.controller = XboxController(0)

        #self.lmotor = wpilib.CANTalon(1)
        #self.rmotor = wpilib.CANTalon(0)

        self.drive = driveTrain(self)

        # Initialize Components functions
        self.components = {
                            'drive' : self.drive
                            }
        '''
        # Setup PID
        self.pidRight = wpilib.PIDController(1, 0, 0,
                                        lambda: self.drive.getRightRate(),
                                        lambda d: self.drive.driveRightSide(d)) # Initialize PID controller object
        self.pidLeft = wpilib.PIDController(1, 0, 0,
                                        lambda: self.drive.getLeftRate(),
                                        lambda d: self.drive.driveLeftSide(d)) # Initialize PID controller object

        #self.pidRight = wpilib.PIDController(1, 0, 0,self.drive.getRightEnc(),self.drive.getRightMotor()) # Initialize PID controller object
        #self.pidLeft = wpilib.PIDController(1, 0, 0, self.drive.getLeftEnc(),self.drive.getLeftMotor()) # Initialize PID controller object

        self.pidRight.setAbsoluteTolerance(0.01)
        self.pidLeft.setAbsoluteTolerance(0.01)
        self.pidRight.setOutputRange(-1,1)
        self.pidLeft.setOutputRange(-1,1)
        '''

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.dash.putNumber('Left Encoder Rate', 0)
        self.dash.putNumber('Right Encoder Rate', 0)
        self.dash.putNumber('Left Encoder Distance', 0)
        self.dash.putNumber('Right Encoder Distance', 0)
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)
        '''
        wpilib.LiveWindow.addActuator("PID", "Right PID Controller", self.pidRight)
        wpilib.LiveWindow.addActuator("PID", "Left PID Controller", self.pidLeft)

        # Reset all the things
        self.drive.reset()
        self.pidRight.reset()
        self.pidLeft.reset()
        self.pidRight.enable()
        self.pidLeft.enable()
        '''
        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)              # Wait for 0.01 seconds

    def autonomous(self):
        #self.autonomous_modes.run()
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)
        #self.lencoder.reset() #sets the encoder values to 0 at the start of each call
        #self.rencoder.reset()
        ###############################################################################
        currentSpeed = 0.1 #Set this to the desired speed
        ###############################################################################
        while self.isAutonomous() and self.isEnabled(): #Here just in case I have put the While loop in the wrong place(Hescott)             # remove the need to multiply by -1
            self.autonomous_modes.run()

    def operatorControl(self):
        while self.isOperatorControl() and self.isEnabled():
            #wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)
            #self.drive.driveManual(self.controller.getLeftY(), self.controller.getRightY())
            self.drive.driveRightSide(self.controller.getRightY())
            self.drive.driveLeftSide(self.controller.getLeftY())
            self.drive.log()
            wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

    def test(self):
        wpilib.LiveWindow.run()

        while self.isTest() and self.isEnabled():
            self.drive.driveRightSide(self.controller.getRightY())
            self.drive.driveLeftSide(self.controller.getLeftY())
            self.drive.log()


if __name__ == "__main__":
    wpilib.run(MyRobot)
