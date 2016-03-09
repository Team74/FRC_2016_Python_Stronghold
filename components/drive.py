"""
File Author: Will Lowry, Will Hescott
File Creation Date: 1/28/2015
File Purpose: To create our drive functions
"""
import wpilib
from wpilib import CANTalon, Encoder, Timer, RobotDrive
from wpilib.interfaces import Gyro
from . import Component

class driveTrain(Component) :

    def __init__(self, robot):
        super().__init__()
        self.robot = robot

        # Constants
        WHEEL_DIAMETER = 8
        PI = 3.1415
        ENCODER_TICK_COUNT_250 = 250
        ENCODER_TICK_COUNT_360 = 360
        ENCODER_GOAL = 0 # default
        ENCODER_TOLERANCE = 1 # inch0
        self.INCHES_PER_DEGREE = 8 * 3.1415 / 360
        self.CONTROL_TYPE = False # False = disable PID components

        self.rfmotor = CANTalon(0)
        self.rbmotor = CANTalon(1)
        self.lfmotor = CANTalon(2)
        self.lbmotor = CANTalon(3)

        self.lbmotor.setInverted(True)
        self.rfmotor.setInverted(True)
        self.rbmotor.setInverted(True)

        '''
        #setting up the distances per rotation
        self.lfmotor.configEncoderCodesPerRev(3.2*4*3.14159)
        self.rfmotor.configEncoderCodesPerRev(1024)
        self.lbmotor.configEncoderCodesPerRev(1024)
        self.rbmotor.configEncoderCodesPerRev(1024)
        '''
        #add distance tracking, USING ROLLOVER

        '''
        # changing the encoder output from DISTANCE to RATE (we're dumb)
        self.lfencoder.setPIDSourceType(wpilib.PIDController.PIDSourceType.kRate)
        self.lbencoder.setPIDSourceType(wpilib.PIDController.PIDSourceType.kRate)
        self.rfencoder.setPIDSourceType(wpilib.PIDController.PIDSourceType.kRate)
        self.rbencoder.setPIDSourceType(wpilib.PIDController.PIDSourceType.kRate)

        # LiveWindow settings (Encoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Left Front Encoder", self.lfencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Right Front Encoder", self.rfencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Left Back Encoder", self.lbencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Right Back Encoder", self.rbencoder)
        '''

        # Checking the state of the encoders on the Smart Dashboard
        wpilib.SmartDashboard.putBoolean("Right Front Encoder Enabled?", self.rfmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Right Back Encoder Enabled?", self.rbmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Left Front Encoder Enabled?", self.lfmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Left Back Encoder Enabled?", self.lbmotor.isSensorPresent)

        if self.CONTROL_TYPE:

            # Initializing PID Controls
            self.pidRightFront = wpilib.PIDController(0.001, 0.8, 0.005, 0, self.rfencoder, self.rfmotor, 0.02)
            self.pidLeftFront = wpilib.PIDController(0.001, 0.8, 0.005, 0, self.lfencoder, self.lfmotor, 0.02)
            self.pidRightBack = wpilib.PIDController(0.001, 0.8, 0.005, 0, self.rbencoder, self.rbmotor, 0.02)
            self.pidLeftBack = wpilib.PIDController(0.001, 0.8, 0.005, 0, self.lbencoder, self.lbmotor, 0.02)

            # PID Absolute Tolerance Settings
            self.pidRightFront.setAbsoluteTolerance(0.05)
            self.pidLeftFront.setAbsoluteTolerance(0.05)
            self.pidRightBack.setAbsoluteTolerance(0.05)
            self.pidLeftBack.setAbsoluteTolerance(0.05)


            # PID Output Range Settings
            self.pidRightFront.setOutputRange(-1, 1)
            self.pidLeftFront.setOutputRange(-1, 1)
            self.pidRightBack.setOutputRange(-1, 1)
            self.pidLeftBack.setOutputRange(-1, 1)


            # Enable PID
            #self.enablePIDs()

            # LiveWindow settings (PID)
            wpilib.LiveWindow.addActuator("Drive Train Right", "Right Front PID", self.pidRightFront)
            wpilib.LiveWindow.addActuator("Drive Train Left", "Left Front PID", self.pidLeftFront)
            wpilib.LiveWindow.addActuator("Drive Train Right", "Right Back PID", self.pidRightBack)
            wpilib.LiveWindow.addActuator("Drive Train Left", "Left Back PID", self.pidLeftBack)


        self.dashTimer = Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        # Adding components to the LiveWindow (testing)
        wpilib.LiveWindow.addActuator("Drive Train Left", "Left Front Motor", self.lfmotor)
        wpilib.LiveWindow.addActuator("Drive Train Right", "Right Front Motor", self.rfmotor)
        wpilib.LiveWindow.addActuator("Drive Train Left", "Left Back Motor", self.lbmotor)
        wpilib.LiveWindow.addActuator("Drive Train Right", "Right Back Motor", self.rbmotor)


    def log(self):
        #The log method puts interesting information to the SmartDashboard. (like velocity information)
        wpilib.SmartDashboard.putNumber("Left Front Speed", self.lfmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Right Front Speed", self.rfmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Left Back Speed", self.lbmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Right Back Speed", self.rbmotor.getEncVelocity())

    # drive forward function
    def drive_forward(self, speed) :
        self.drive.tankDrive(speed, speed, True)

    # manual drive function for Tank Drive
    def xboxTankDrive(self, leftSpeed, rightSpeed, leftB, rightB, rightT):

        if (leftB == True): #Straight Button
            rightSpeed = leftSpeed

        if (rightB == True): #Slow Button
            leftSpeed = leftSpeed/1.75
            rightSpeed = rightSpeed/1.75
            if(leftSpeed < -0.5 and rightSpeed > 0.5 or leftSpeed > -0.5 and rightSpeed < 0.5):
                leftSpeed = leftSpeed
                rightSpeed = rightSpeed

        # Fast button
        if(rightT == True):
            leftSpeed = leftSpeed*(1.75)
            rightSpeed = rightSpeed*(1.75)

        # Creating margin for error when using the joysticks, as they're quite sensitive
        if abs(rightSpeed) < 0.07 :
            rightSpeed = 0
        if abs(leftSpeed) < 0.07 :
            leftSpeed = 0

        # Setting up new encoders on the Smart Dashboard
        wpilib.SmartDashboard.putNumber("Right Front Mag Distance", self.rfmotor.getEncPosition())
        wpilib.SmartDashboard.putNumber("Right Back Mag Distance", self.rbmotor.getEncPosition())
        wpilib.SmartDashboard.putNumber("Left Front Mag Distance", self.lfmotor.getEncPosition())
        wpilib.SmartDashboard.putNumber("Left Back Mag Distance", self.lbmotor.getEncPosition())

        if self.CONTROL_TYPE:
            self.pidRightFront.setSetpoint(rightSpeed*(-100))
            self.pidRightBack.setSetpoint(rightSpeed*(-100))
            self.pidLeftFront.setSetpoint(leftSpeed*100)
            self.pidLeftBack.setSetpoint(leftSpeed*100)
        else:
            self.lfmotor.set(leftSpeed*(-.6))
            self.rfmotor.set(rightSpeed*(-.6))
            self.lbmotor.set(leftSpeed*(.6))
            self.rbmotor.set(rightSpeed*(.6))

    #autononmous tank drive (to remove a need for a slow, striaght, or fast button)
    def autonTankDrive(self, leftSpeed, rightSpeed):

        #self.drive.tankDrive(leftSpeed, rightSpeed, True)
        self.pidRightFront.setSetpoint(rightSpeed*(100))
        self.pidRightBack.setSetpoint(rightSpeed*(100))
        self.pidLeftFront.setSetpoint(leftSpeed*-100)
        self.pidLeftBack.setSetpoint(leftSpeed*-100)

    # stop function
    def drive_stop(self) :
        self.drive.tankDrive(0,0)

# fucntion to reset the gyro
    def reset(self):
        if self.CONTROL_TYPE:
            self.lfencoder.reset()
            self.rfencoder.reset()
            self.lbencoder.reset()
            self.rbencoder.reset()
            self.pidLeftBack.setSetpoint(0)
            self.pidLeftFront.setSetpoint(0)
            self.pidRightBack.setSetpoint(0)
            self.pidRightFront.setSetpoint(0)

    def getDistance(self):
        return (abs(self.lfencoder.getDistance()) + abs(self.lbencoder.getDistance()) + abs(self.rfencoder.getDistance()) + abs(self.rbencoder.getDistance()))/4.0


# function to turn a certain number of degrees
    def turn_angle(self, degrees):
        desired_inches = self.INCHES_PER_DEGREE * degrees
        if degrees < 0:
            while (abs(self.lfencoder.getDistance()) + abs(self.rfencoder.getDistance())) <= desired_inches :
                self.autonTankDrive(0.4, -0.4)
        elif degrees > 0:
            while (abs(self.lfencoder.getDistance()) + abs(self.rfencoder.getDistance())) <= desired_inches :
                self.autonTankDrive(-0.4, 0.4)

    # Enable PID Controllers
    def enablePIDs(self):
        self.pidLeftFront.enable()
        self.pidLeftBack.enable()
        self.pidRightFront.enable()
        self.pidRightBack.enable()

    # Disable PID Controllers
    def disablePIDs(self):
        self.pidLeftFront.disable()
        self.pidLeftBack.disable()
        self.pidRightFront.disable()
        self.pidRightBack.disable()
