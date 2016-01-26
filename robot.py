#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from xbox import XboxController
from robotpy_ext.autonomous import AutonomousModeSelector
#from pyfrc.sim.pygame_joysticks import UsbJoysticks
#import pygame
#from xbox2 import XboxController

# to stay in sync with our driver station
CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        #self.robot_drive = wpilib.RobotDrive(0,1)
        self.controller = XboxController(0)
        #self.stick = wpilib.Joystick(0)

        self.lmotor = wpilib.CANTalon(0)
        self.rmotor = wpilib.CANTalon(1)

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        self.autonomous_modes = AutonomousModeSelector('autonomous')
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
        self.autonomous_modes.run()
        Timer.delay(CONTROL_LOOP_WAIT_TIME)

    def operatorControl(self):
        #self.robot_drive.TankDrive(self.controller1.)
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

        while self.isOperatorControl() and self.isEnabled():

            #for i in range( self.axes ):
            #    axis = self.joys.get_axis( i )
                #print(axis)

            #self.lmotor.set(self.controller1.getLeftY())
            #self.rmotor.set(self.controller1.getRightY())

            self.lmotor.set(self.controller.getLeftY())
            self.rmotor.set(self.controller.getRightY())

    def test(self):
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
