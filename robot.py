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
        # Reset all the things
#        self.drive.reset()
#        self.pid.reset()
#        self.pid.enable()
        self.drive.log()
        '''
        # Setting up our USB Camera
        vision = USBCamera()
        #vision.setFPS(15)
        #vision.setSize(640, 360)
        #vision.setExposureAuto()
        #vision.setWhiteBalanceAuto()
        #vision.startCapture()
        visionServer = CameraServer()
        visionServer.camera = vision
        visionServer.setSize(visionServer.kSize160x120)
        visionServer.setQuality(20)
        visionServer.startAutomaticCapture(vision)
        '''

    def disabled(self):
        self.drive.reset()
        self.drive.disablePIDs()

        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        #self.autonomous_modes.run()
        #wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)
        self.drive.reset()
        self.drive.enablePIDs()
        #self.lencoder.reset() #sets the encoder values to 0 at the start of each call
        #self.rencoder.reset()
        ###############################################################################
        currentSpeed = 0.1 #Set this to the desired speed
        ###############################################################################

        while self.isAutonomous() and self.isEnabled(): #Here just in case I have put the While loop in the wrong place(Hescott)             # remove the need to multiply by -1

            # Run the actual autonomous mode
            self.potentiometer = ('Arm Potentiometer', self.robotArm.getPOT())
            self.autonomous_modes.run()

            #self.lmotor.set(currentSpeed)           #it is multiplied by -1 because of the motor polarity, switiching the wires would
            #self.rmotor.set(currentSpeed*(-1))

    def operatorControl(self):
        # Resetting encoders

        self.drive.reset()
        self.drive.disablePIDs()

        while self.isOperatorControl() and self.isEnabled():
            self.drive.xboxTankDrive(self.controller.getLeftY(), self.controller.getRightY(), self.controller.getLeftBumper(), self.controller.getRightBumper(), self.controller.getRightTrigger())

            self.robotArm.armUpDown(self.controller2.getLeftTriggerRaw(), self.controller2.getRightTriggerRaw())
            self.robotArm.wheelSpin(self.controller2.getLeftY())

            self.climber.climbUpDown(self.controller2.getLeftBumper(), self.controller2.getRightBumper())

            self.drive.log()

            wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME)

            # Send encoder data to the smart dashboard
#            self.dash.putNumber('Left Encoder Rate', self.lencoder.getRate())
#            self.dash.putNumber('Right Encoder Rate', self.rencoder.getRate())
#            self.dash.putNumber('Left Encoder Distance', self.lencoder.getDistance())
#            self.dash.putNumber('Right Encoder Distance', self.rencoder.getDistance())
            self.dash.putNumber('Arm Potentiometer', self.robotArm.getPOT())
            #self.dash.putNumber('Control Type', self.drive.get())
            self.dash.putBoolean('Back Switch', self.robotArm.getFrontSwitch())
            self.dash.putBoolean('Front Switch', self.robotArm.getBackSwitch())


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
