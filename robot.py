#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.drive import driveTrain
from components.armControl import arm
from components.climberControl import lift
from robotpy_ext.autonomous.selector import AutonomousModeSelector
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
        self.controller2 = XboxController(1)

        #self.lmotor = wpilib.CANTalon(1)
        #self.rmotor = wpilib.CANTalon(0)

        self.drive = driveTrain(self)
        self.robotArm = arm(self)
        self.climber = lift(self)

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            'drive' : self.drive,
                            'arm' : self.robotArm,
                            'lift' : self.climber
                            }

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.dash.putNumber('Left Encoder Rate', 0)
        self.dash.putNumber('Right Encoder Rate', 0)
        self.dash.putNumber('Left Encoder Distance', 0)
        self.dash.putNumber('Right Encoder Distance', 0)
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)


        # Reset all the things
#        self.drive.reset()
#        self.pid.reset()
#        self.pid.enable()

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

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

            #self.lmotor.set(currentSpeed)           #it is multiplied by -1 because of the motor polarity, switiching the wires would
            #self.rmotor.set(currentSpeed*(-1))

    def operatorControl(self):
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

        # Resetting encoders

        while self.isOperatorControl() and self.isEnabled():
            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY())
            #self.robotArm.armUpDown(self.controller.getTriggers(), rate=0.3)
            self.robotArm.armUpDown(self.controller2.getLeftTriggerRaw(), self.controller2.getRightTriggerRaw())
            self.climber.climbUpDown(self.controller2.getLeftBumper(), self.controller2.getRightBumper())
            # Send encoder data to the smart dashboard
#            self.dash.putNumber('Left Encoder Rate', self.lencoder.getRate())
#            self.dash.putNumber('Right Encoder Rate', self.rencoder.getRate())
#            self.dash.putNumber('Left Encoder Distance', self.lencoder.getDistance())
#            self.dash.putNumber('Right Encoder Distance', self.rencoder.getDistance())

    def test(self):
        wpilib.LiveWindow.run()

        while self.isTest() and self.isEnabled():
            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY())

if __name__ == "__main__":
    wpilib.run(MyRobot)
