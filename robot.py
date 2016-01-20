#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib
from xbox import XboxController

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """
        self.controller = XboxController(0)
        self.leftMotor = wpilib.Talon(0) # Full speed = leftMotor.set(1)
        self.rightMotor = wpilib.Talon(1)# Reverse = leftMotor.set(-1)
        self.driveTrain = wpilib.RobotDrive(self.leftMotor, self.rightMotor)

    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        self.auto_loop_counter = 0
        MyRobot.run(autonomousPeriodic())
    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""

        # Check if we've completed 100 loops (approximately 2 seconds)

        #if self.auto_loop_counter < 100:
        #    self.robot_drive.drive(-0.5, 0) # Drive forwards at half speed
        #    self.auto_loop_counter += 1
        #else:
        #    self.robot_drive.drive(0, 0)    #Stop robot
        leftMotor.set(1)
        rightMotor.set(1)

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""
        #self.driveTrain.TankDrive(controller.getLeftY(), controller.getRightY())
        while self.isEnabled() : # and self.isOperatorControl()
            #if controller.getLeftY > 0
            #    RobotDrive.Drive(controller.getLeftY(), 0)
            #elifcontroller.getLeftY < 0
            self.leftMotor.set(self.controller.left_y())
            self.rightMotor.set(self.controller.right_y())
            print(self.controller.left_y())
            print(self.controller.right_y())
    def testPeriodic(self):
        """This function is called periodically during test mode."""
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
