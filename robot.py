#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from robotpy_ext.autonomous import AutonomousModeSelector
from wpilib.smartdashboard import SmartDashboard
#from pyfrc.sim.pygame_joysticks import UsbJoysticks
#import pygame

# to stay in sync with our driver station
CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    # Constants
    WHEEL_DIAMETER = 6
    PI = 3.1415
    ENCODER_TICK_COUNT = 250

    def robotInit(self):
        self.controller = XboxController(0)

        self.lmotor = wpilib.CANTalon(1)
        self.rmotor = wpilib.CANTalon(0)

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        self.lencoder = wpilib.Encoder(0, 1) #Creates an object of type Encoder, called lencoder. It counts
        #self.lencoder.setReverseDirection(True)
        self.rencoder = wpilib.Encoder(2, 3) #the amount that a motor has rotated, and returns it in Direction and Distance variables
        self.lencoder.setDistancePerPulse(self.WHEEL_DIAMETER*self.PI/self.ENCODER_TICK_COUNT*(-1))
        self.rencoder.setDistancePerPulse(self.WHEEL_DIAMETER*self.PI/self.ENCODER_TICK_COUNT)

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.dash.putNumber('Left Encoder Rate', 0)
        self.dash.putNumber('Right Encoder Rate', 0)
        self.dash.putNumber('Left Encoder Distance', 0)
        self.dash.putNumber('Right Encoder Distance', 0)
        #self.autonomous_modes = AutonomousModeSelector('autonomous')

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        self.autonomous_modes.run()
        Timer.delay(CONTROL_LOOP_WAIT_TIME)

    def operatorControl(self):
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

        # Resetting encoders
        self.lencoder.reset()
        self.rencoder.reset()

        while self.isOperatorControl() and self.isEnabled():
            leftValue = self.controller.getLeftY()
            rightValue = self.controller.getRightY()

            if self.controller.getLeftBumper(): # Slow button
                leftValue = leftValue/2
                rightValue = rightValue/2
            if self.controller.getRightBumper(): #Straight Button
                rightValue = leftValue

            # Set motor speeds
            self.lmotor.set(leftValue*(-1))
            self.rmotor.set(rightValue)

            # Send encoder data to the smart dashboard
            self.dash.putNumber('Left Encoder Rate', self.lencoder.getRate())
            self.dash.putNumber('Right Encoder Rate', self.rencoder.getRate())
            self.dash.putNumber('Left Encoder Distance', self.lencoder.getDistance())
            self.dash.putNumber('Right Encoder Distance', self.rencoder.getDistance())

    def test(self):
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
