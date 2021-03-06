"""
File Author: Will Lowry, Will Hescott
File Creation Date: 1/28/2015
File Purpose: To create our drive functions

Transmission gear ratio: 18.74/1

"""
import wpilib
from wpilib import CANTalon, Encoder, Timer, RobotDrive
from wpilib.interfaces import Gyro
from . import Component
import hal



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
        self.RPM = 4320/10.7
        self.INCHES_PER_REV = WHEEL_DIAMETER * 3.1415
        self.CONTROL_TYPE = False # False = disable PID components
        self.LEFTFRONTCUMULATIVE = 0
        self.LEFTBACKCUMULATIVE = 0
        self.RIGHTFRONTCUMULATIVE = 0
        self.RIGHTBACKCUMULATIVE = 0

        self.rfmotor = CANTalon(0)
        self.rbmotor = CANTalon(1)
        self.lfmotor = CANTalon(2)
        self.lbmotor = CANTalon(3)

        self.lfmotor.reverseOutput(True)
        self.lbmotor.reverseOutput(True)
        #self.rfmotor.reverseOutput(True)
        #self.rbmotor.reverseOutput(True)#practice bot only


        self.rfmotor.enableBrakeMode(True)
        self.rbmotor.enableBrakeMode(True)
        self.lfmotor.enableBrakeMode(True)
        self.lbmotor.enableBrakeMode(True)

        absolutePosition = self.lbmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.lbmotor.setEncPosition(absolutePosition)
        absolutePosition = self.lfmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.lfmotor.setEncPosition(absolutePosition)
        absolutePosition = self.rbmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.rbmotor.setEncPosition(absolutePosition)
        absolutePosition = self.rfmotor.getPulseWidthPosition() & 0xFFF; # mask out the bottom12 bits, we don't care about the wrap arounds use the low level API to set the quad encoder signal
        self.rfmotor.setEncPosition(absolutePosition)

        self.rfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.rbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.lfmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)
        self.lbmotor.setFeedbackDevice(CANTalon.FeedbackDevice.CtreMagEncoder_Relative)


        #setting up the distances per rotation
        self.lfmotor.configEncoderCodesPerRev(4096)
        self.rfmotor.configEncoderCodesPerRev(4096)
        self.lbmotor.configEncoderCodesPerRev(4096)
        self.rbmotor.configEncoderCodesPerRev(4096)

        self.lfmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.rfmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.lbmotor.setPID(0.0005, 0, 0.0, profile=0)
        self.rbmotor.setPID(0.0005, 0, 0.0, profile=0)

        self.lbmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.lbmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.lbmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.lfmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.lfmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.lfmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rbmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.rbmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.rbmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rfmotor.configNominalOutputVoltage(+0.0, -0.0)
        self.rfmotor.configPeakOutputVoltage(+12.0, -12.0)
        self.rfmotor.setControlMode(CANTalon.ControlMode.Speed)

        self.rfmotor.setPosition(0)
        self.rbmotor.setPosition(0)
        self.lfmotor.setPosition(0)
        self.lbmotor.setPosition(0)

        self.lfmotor.reverseSensor(True)
        self.lbmotor.reverseSensor(True)


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
        '''
        # Checking the state of the encoders on the Smart Dashboard
        wpilib.SmartDashboard.putBoolean("Right Front Encoder Enabled?", self.rfmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Right Back Encoder Enabled?", self.rbmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Left Front Encoder Enabled?", self.lfmotor.isSensorPresent)
        wpilib.SmartDashboard.putBoolean("Left Back Encoder Enabled?", self.lbmotor.isSensorPresent)
        '''

        if self.CONTROL_TYPE:

            # Initializing PID Controls
            self.pidRightFront = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.rfmotor.feedbackDevice, self.rfmotor, 0.02)
            self.pidLeftFront = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.lfmotor.feedbackDevice, self.lfmotor, 0.02)
            self.pidRightBack = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.rbmotor.feedbackDevice, self.rbmotor, 0.02)
            self.pidLeftBack = wpilib.PIDController(0.002, 0.8, 0.005, 0, self.lbmotor.feedbackDevice, self.lbmotor, 0.02)

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

            '''
            # LiveWindow settings (PID)
            wpilib.LiveWindow.addActuator("Drive Train Right", "Right Front PID", self.pidRightFront)
            wpilib.LiveWindow.addActuator("Drive Train Left", "Left Front PID", self.pidLeftFront)
            wpilib.LiveWindow.addActuator("Drive Train Right", "Right Back PID", self.pidRightBack)
            wpilib.LiveWindow.addActuator("Drive Train Left", "Left Back PID", self.pidLeftBack)
            '''

        self.dashTimer = Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        '''
        # Adding components to the LiveWindow (testing)
        wpilib.LiveWindow.addActuator("Drive Train Left", "Left Front Motor", self.lfmotor)
        wpilib.LiveWindow.addActuator("Drive Train Right", "Right Front Motor", self.rfmotor)
        wpilib.LiveWindow.addActuator("Drive Train Left", "Left Back Motor", self.lbmotor)
        wpilib.LiveWindow.addActuator("Drive Train Right", "Right Back Motor", self.rbmotor)
        '''

    def log(self):
        #The log method puts interesting information to the SmartDashboard. (like velocity information)
        '''
        #no longer implemented because of change of hardware
        wpilib.SmartDashboard.putNumber("Left Front Speed", self.lfmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Right Front Speed", self.rfmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Left Back Speed", self.lbmotor.getEncVelocity())
        wpilib.SmartDashboard.putNumber("Right Back Speed", self.rbmotor.getEncVelocity())
        '''

        wpilib.SmartDashboard.putNumber("RF Mag Enc Position", self.rfmotor.getPosition())
        wpilib.SmartDashboard.putNumber("RB Mag Enc Position", self.rbmotor.getPosition())
        wpilib.SmartDashboard.putNumber("LF Mag Enc Position", self.lfmotor.getPosition())
        wpilib.SmartDashboard.putNumber("LB Mag Enc Position", self.lbmotor.getPosition())

        '''
        wpilib.SmartDashboard.putNumber("Right Front Mag Distance(inches)", self.convertEncoderRaw(self.rfmotor.getPosition()*0.57))
        wpilib.SmartDashboard.putNumber("Right Back Mag Distance(inches)", self.convertEncoderRaw(self.rbmotor.getPosition()*0.57))
        wpilib.SmartDashboard.putNumber("Left Front Mag Distance(inches)", self.convertEncoderRaw(self.lfmotor.getPosition()*0.57))
        wpilib.SmartDashboard.putNumber("Left Back Mag Distance(inches)", self.convertEncoderRaw(self.lbmotor.getPosition()*0.57))
        '''

    # drive forward function
    def drive_forward(self, speed) :
        self.drive.tankDrive(speed, speed, True)

    # manual drive function for Tank Drive
    def xboxTankDrive(self, leftSpeed, rightSpeed, leftB, rightB, leftT, rightT):
        #self.lfmotor.setCloseLoopRampRate(1)
        #self.lbmotor.setCloseLoopRampRate(1)
        #self.rfmotor.setCloseLoopRampRate(1)
        #self.rbmotor.setCloseLoopRampRate(1)



        if (leftB == True): #Straight Button
            rightSpeed = leftSpeed

        if (rightB == True): #Slow Button
            #leftSpeed = leftSpeed/1.75
            #rightSpeed = rightSpeed/1.75
            if(not(leftSpeed < -0.5 and rightSpeed > 0.5 or leftSpeed > -0.5 and rightSpeed < 0.5)):    #only do t if not turning
                leftSpeed = leftSpeed/1.75
                rightSpeed = rightSpeed/1.75

        # Fast button
        if(rightT == True):
            #self.lfmotor.setCloseLoopRampRate(24)
            #self.lbmotor.setCloseLoopRampRate(24)
            #self.rfmotor.setCloseLoopRampRate(24)
            #self.rbmotor.setCloseLoopRampRate(24)
            leftSpeed = leftSpeed*(1.75)
            rightSpeed = rightSpeed*(1.75)



        if(leftT == True):
            leftSpeed = 0.1
            rightSpeed = 0.1



        # Creating margin for error when using the joysticks, as they're quite sensitive
        if abs(rightSpeed) < 0.04 :
            rightSpeed = 0
        if abs(leftSpeed) < 0.04 :
            leftSpeed = 0

        if self.CONTROL_TYPE:
            self.pidRightFront.setSetpoint(rightSpeed)
            self.pidRightBack.setSetpoint(rightSpeed)
            self.pidLeftFront.setSetpoint(leftSpeed)
            self.pidLeftBack.setSetpoint(leftSpeed)
        else:
            self.lfmotor.set(leftSpeed*512)
            self.rfmotor.set(rightSpeed*512)
            self.lbmotor.set(leftSpeed*512)
            self.rbmotor.set(rightSpeed*512)

    #autononmous tank drive (to remove a need for a slow, striaght, or fast button)
    def autonTankDrive(self, leftSpeed, rightSpeed):
        self.log()
        #self.drive.tankDrive(leftSpeed, rightSpeed, True)
        self.rfmotor.set(rightSpeed)
        self.rbmotor.set(rightSpeed*(-1))
        self.lfmotor.set(leftSpeed)
        self.lbmotor.set(leftSpeed*(-1))

    # stop function
    def drive_stop(self) :
        self.drive.tankDrive(0,0)

# fucntion to reset the PID's and encoder values
    def reset(self):
        self.rfmotor.setPosition(0)
        self.rbmotor.setPosition(0)
        self.lfmotor.setPosition(0)
        self.lbmotor.setPosition(0)

        if self.CONTROL_TYPE:
            self.LEFTFRONTCUMULATIVE = 0
            self.RIGHTFRONTCUMULATIVE = 0
            self.LEFTBACKCUMULATIVE= 0
            self.RIGHTBACKCUMULATIVE = 0
            self.pidLeftBack.setSetpoint(0)
            self.pidLeftFront.setSetpoint(0)
            self.pidRightBack.setSetpoint(0)
            self.pidRightFront.setSetpoint(0)

    # def getDistance(self)
    #    return (abs(self.convertEncoderRaw(LEFTFRONTCUMULATIVE) + abs(self.convertEncoderRaw(LEFTBACKCUMULATIVE)) + abs(self.convertEncoderRaw(RIGHTFRONTCUMULATIVE)) + abs(self.convertEncoderRaw(RIGHTBACKCUMULATIVE)))

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
        '''
        #No longer required because we swapped from analog encoders to magnetic encoders
        self.pidLeftFront.enable()
        self.pidLeftBack.enable()
        self.pidRightFront.enable()
        self.pidRightBack.enable()
        '''
    # Disable PID Controllers
    def disablePIDs(self):
        '''
        #see explaination above
        self.pidLeftFront.disable()
        self.pidLeftBack.disable()
        self.pidRightFront.disable()
        self.pidRightBack.disable()
        '''

    def getAutonDistance(self):
        return (self.convertEncoderRaw(abs(self.rfmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.rbmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.lfmotor.getPosition()*0.57))
                + self.convertEncoderRaw(abs(self.lbmotor.getPosition()*0.57)))/4

        #detirmines how many ticks the encoder has processed
    def getMotorDistance(self, motor, cumulativeDistance):
        currentRollovers = 0 #number of times the encoder has gone from 1023 to 0
        previousValue = cumulativeDistance #variable for comparison
        currentValue = motor.getEncPosition() #variable for comparison
        if(previousValue > currentValue): #checks to see if the encoder reset itself from 1023 to 0
            currentRollovers += 1 #notes the rollover
        return currentValue + (currentRollovers * 1024) #adds current value to the number of rollovers, each rollover == 1024 ticks

        #converts ticks from getMotorDistance into inches
    def convertEncoderRaw(self, selectedEncoderValue):
        return selectedEncoderValue * self.INCHES_PER_REV
