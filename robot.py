#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from xbox import XboxController
#from pyfrc.sim.pygame_joysticks import UsbJoysticks
#import pygame
#from xbox2 import XboxController

# to stay in sync with our driver station
CONTROL_LOOP_WAIT_TIME = 0.01#0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        #self.robot_drive = wpilib.RobotDrive(0,1)
        self.controller = XboxController(0)
        #self.stick = wpilib.Joystick(0)

        self.lmotor = wpilib.CANTalon(1)
        self.rmotor = wpilib.CANTalon(0)

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()


        self.lencoder = wpilib.Encoder(0, 1)
        self.rencoder = wpilib.Encoder(2, 3)
        # Initialize the joysticks
        #pygame.joystick.init()

        #self.joys = pygame.joystick.Joystick(0)
        #self.joys.init()
        #self.axes = self.joys.get_numaxes()

        #joys = UsbJoysticks(1)
        #for x in joys.getUsbJoystickList():
        #    print(x.get_name())

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
       while self.isAutonomous() and self.isEnabled():
           lencoder.reset()
           rencoder.reset()
###############################################################################
           currentSpeed = 0 #Set this to the desired speed
###############################################################################
        #while self.isAutonomous() and self.isEnabled():
            self.lmotor.set(currentSpeed)
            self.rmotor.set(currentSpeed)
            LToRRatio = rencoder.getDistance() / lencoder.getDistance()
            RToLRatio = lencoder.getDistance() / rencoder.getDistance()
            if (LToRRatio > 0)
                correctValue = LToRRatio * lencoder.getDistance()
                self.lmoter.set(correctValue)
            elif (RToLRatio > 0)
                correctValue = RToLRatio * rencoder.getDistance()
                self.rmotor.set(correctValue)
            elif (LToRRatio = 0 and RToLRatio = 0)
                self.rmotor.set(currentSpeed)
                self.rmotor.set(CurrentSpeed)
            #self.lmotor.set(0.5)
            #self.rmotor.set(0.5 * -1)

    def operatorControl(self):
        #self.robot_drive.TankDrive(self.controller1.)
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

        while self.isOperatorControl() and self.isEnabled():

            #for i in range( self.axes ):
            #    axis = self.joys.get_axis( i )
                #print(axis)

            self.lmotor.set(self.controller.getLeftY()*(-1))
            self.rmotor.set(self.controller.getRightY())

            #self.lmotor.set(self.stick.getRawAxis(1))
            #self.rmotor.set(self.stick.getRawAxis(5))      # Forks for right stick x axisqqqqqqqqqqqqqqqqqqq
    def test(self):
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
