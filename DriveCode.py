#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from wpilib import Joystick
from Xbox import XboxController

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        controller = Joystick(2, numAxisTypes = 1, numButtonTypes=None)
    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Check if we've completed 100 loops (approximately 2 seconds)
        if self.auto_loop_counter < 100:
            self.robot_drive.drive(-0.5, 0) # Drive forwards at half speed
            self.auto_loop_counter += 1
        else:
            self.robot_drive.drive(0, 0)    #Stop robot

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        print(controller.getAxis(1))
         #self.robot_drive.tankDrive(self.leftStick, self.rightStick)
    #    if (controller.left_y(self) < 0)
    #        return ("lReverse", "\n")
    #            elif(controller.left_y(self) > 0)
    #                return ("lForward", "\n")
    #    if (controller.right_y(self) < 0)
    #        return ("rReverse", "\n")
    #            elif(controller.right_y(self) > 0)
    #                return ("rForward", "\n ")

    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
