#!/usr/bin/env python3
import wpilib
from xbox import XboxController
from wpilib.smartdashboard import SmartDashboard
from components.drive import driveTrain
from components.armControl import arm
from components.climberControl import lift
from components.pixy import Pixy
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import USBCamera, CameraServer

CONTROL_LOOP_WAIT_TIME = 0.025

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0)
        self.controller2 = XboxController(1)

        #self.lmotor = wpilib.CANTalon(1)
        #self.rmotor = wpilib.CANTalon(0)

        self.drive = driveTrain(self)
        self.robotArm = arm(self)
        self.climber = lift(self)
        self.pixy = Pixy()

        self.drive.reset()

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Initialize Components functions
        self.components = {
                            'drive' : self.drive,
                            'arm' : self.robotArm,
                            'lift' : self.climber,
                            'pixy' : self.pixy
                            }

        # Initialize Smart Dashboard
        self.dash = SmartDashboard()
        self.autonomous_modes = AutonomousModeSelector('autonomous', self.components)
        self.potentiometer = ('Arm Potentiometer', 0)
        self.dash.putNumber('ControlType', 0)
        self.dash.putBoolean('Front Switch', 0)
        self.dash.putBoolean('Back Switch', 0)

        self.drive.log()


    def disabled(self):
        self.drive.reset()
        #self.drive.disablePIDs()

        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        self.drive.reset()
        self.drive.enablePIDs()

        while self.isAutonomous() and self.isEnabled():

            # Run the actual autonomous mode
            self.potentiometer = ('Arm Potentiometer', self.robotArm.getPOT())
            self.drive.log()
            self.autonomous_modes.run()

    def operatorControl(self):
        # Resetting encoders

        self.drive.reset()
        #self.drive.enablePIDs()

        while self.isOperatorControl() and self.isEnabled():
            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY(), self.controller.getLeftBumper(), self.controller.getRightBumper(), self.controller.getRightTrigger())

            self.robotArm.armUpDown(self.controller2.getLeftTriggerRaw(), self.controller2.getRightTriggerRaw(), rate=0.5)
            self.robotArm.wheelSpin(self.controller2.getLeftY())

            self.climber.climbUpDown(self.controller2.getLeftBumper(), self.controller2.getRightBumper())

            self.drive.log()

            wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

            # Send encoder data to the smart dashboard
            self.dash.putNumber('Arm Potentiometer', self.robotArm.getPOT())

            self.dash.putBoolean('Back Arm Switch', self.robotArm.getFrontSwitch())
            self.dash.putBoolean('Front Arm Switch', self.robotArm.getBackSwitch())


    def test(self):
        wpilib.LiveWindow.run()

        self.drive.reset()
        self.drive.enablePIDs()

        while self.isTest() and self.isEnabled():

            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY(), self.controller.getLeftBumper(), self.controller.getRightBumper(), self.controller.getRightTrigger())
            self.robotArm.armUpDown(self.controller2.getLeftTriggerRaw(), self.controller2.getRightTriggerRaw())

    '''
    def checkPixy():
        distanceFromCenter = 0
        closestBallArea = 0 #meaningless number that any result returned by the function can always beat
        biggestBallID = None
        blocks = self.pixy.getBlocks()

        for i in range(0, len(blocks)):
            area = blocks[i].getArea()
            if(area > closestBallArea):
                closestBallArea = area
                biggestBallID = i
       if(controller.getLeftTriggerRaw() > 0.75):
            distanceFromCenter = blocks[BiggestballID] - 180

            if(distanceFromCenter < 0):#turn right
                self.drive.turnAngle(-2)
            elif(distanceFromCenter > 0):#turn left
                self.drive.turnAngle(2)
    '''

if __name__ == "__main__":
    wpilib.run(MyRobot)
