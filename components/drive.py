@@ -16,13 +16,12 @@ class driveTrain(Component) :
        self.robot = robot

        # Constants
        WHEEL_DIAMETER = 6
        WHEEL_DIAMETER = 8
        PI = 3.1415
        ENCODER_TICK_COUNT = 250
        ENCODER_GOAL = 0 # default
        ENCODER_TOLERANCE = 1 # inch
        self.CONTROL_TYPE = 0 # 0 = disable PID components and encoder components
        self.MOTOR_MODE = 1 # 0 = disable the second set of motors
        ENCODER_TOLERANCE = 1 # inch0
        self.CONTROL_TYPE = 1 # 0 = disable PID components

        self.rfmotor = CANTalon(0)
        self.rbmotor = CANTalon(1)
@@ -31,34 +30,58 @@ class driveTrain(Component) :
        self.lfmotor.setInverted(True)
        self.lbmotor.setInverted(True)

        # Initializing the encoders
        self.lfencoder = Encoder(0, 1, False)#, Encoder.EncodingType.k4X) #Creates an object of type Encoder, called lencoder. It counts
        self.rfencoder = Encoder(2, 3, True)#, Encoder.EncodingType.k4X) #the amount that a motor has rotated, and returns it in Direction and Distance variables
        self.lbencoder = Encoder(4, 5, False)#, Encoder.EncodingType.k4x)
        self.rbencoder = Encoder(6, 7, False)#, Encoder.EncodingType.k4x)

        self.drive = RobotDrive(self.lmotor, self.rmotor)
        # Set the distance per encoder tick
        self.lfencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
        self.rfencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
        self.lbencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
        self.rbencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)

        # LiveWindow settings (Encoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Left Front Encoder", self.lfencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Right Front Encoder", self.rfencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Left Back Encoder", self.lbencoder)
        wpilib.LiveWindow.addSensor("Drive Train", "Right Back Encoder", self.rbencoder)

        if self.CONTROL_TYPE:
            # Initializing the encoders
            self.lencoder = Encoder(0, 1, False, Encoder.EncodingType.k4X) #Creates an object of type Encoder, called lencoder. It counts
            self.rencoder = Encoder(2, 3, True, Encoder.EncodingType.k4X) #the amount that a motor has rotated, and returns it in Direction and Distance variables

            # Set the distance per encoder tick
            self.lencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
            self.rencoder.setDistancePerPulse(WHEEL_DIAMETER*PI/ENCODER_TICK_COUNT)
        self.drive = RobotDrive(self.lfmotor, self.rfmotor, self.lbmotor, self.rbmotor)

        if self.CONTROL_TYPE:

            # Initializing PID Controls
            self.pidRight = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.rencoder, self.rmotor, 0.02)
            self.pidLeft = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.lencoder, self.lmotor, 0.02)

            # PID Settings
            self.pidRight.setContinuous(False)
            self.pidLeft.setContinuous(False)
            self.pidRight.setAbsoluteTolerance(0.05)
            self.pidLeft.setAbsoluteTolerance(0.05)
            self.pidRight.setOutputRange(-1, 1)
            self.pidLeft.setOutputRange(-1, 1)

            wpilib.LiveWindow.addSensor("Drive Train", "Left Encoder", self.lencoder)
            wpilib.LiveWindow.addSensor("Drive Train", "Right Encoder", self.rencoder)
            wpilib.LiveWindow.addActuator("Drive Trian", "Right PID", self.pidRight)
            wpilib.LiveWindow.addActuator("Drive Trian", "Left PID", self.pidLeft)
            self.pidRightFront = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.rfencoder, self.rfmotor, 0.02)
            self.pidLeftFront = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.lfencoder, self.lfmotor, 0.02)
            self.pidRightBack = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.rbencoder, self.rbmotor, 0.02)
            self.pidLeftBack = wpilib.PIDController(0.0, 0.0, 0.0, 0.0, self.lbencoder, self.lbmotor, 0.02)

            # PID Continuous Settings
            self.pidRightFront.setContinuous(False)
            self.pidLeftFront.setContinuous(False)
            self.pidRightBack.setContinuous(False)
            self.pidLeftBack.setContinuous(False)

            # PID Absolute Tolerance Settings
            self.pidRightFront.setAbsoluteTolerance(0.05)
            self.pidLeftFront.setAbsoluteTolerance(0.05)
            self.pidRightBack.setAbsoluteTolerance(0.05)
            self.pidLeftBack.setAbsoluteTolerance(0.05)

            # PID OutputRange Settings
            self.pidRightFront.setOutputRange(-1, 1)
            self.pidLeftFront.setOutputRange(-1, 1)
            self.pidRightBack.setOutputRange(-1, 1)
            self.pidLeftBack.setOutputRange(-1, 1)

            # LiveWindow settings (PID)
            wpilib.LiveWindow.addActuator("Drive Trian", "Right Front PID", self.pidRightFront)
            wpilib.LiveWindow.addActuator("Drive Trian", "Left Front PID", self.pidLeftFront)
            wpilib.LiveWindow.addActuator("Drive Trian", "Right Back PID", self.pidRightBack)
            wpilib.LiveWindow.addActuator("Drive Trian", "Left Back PID", self.pidLeftBack)

        self.controller = XboxController(0)

@@ -76,12 +99,15 @@ class driveTrain(Component) :

    def log(self):
        '''The log method puts interesting information to the SmartDashboard.'''
        if self.CONTROL_TYPE:
            wpilib.SmartDashboard.putNumber("Left Distance", self.lencoder.getDistance())
            wpilib.SmartDashboard.putNumber("Right Distance", self.rencoder.getDistance())
            wpilib.SmartDashboard.putNumber("Left Speed", self.lencoder.getRate())
            wpilib.SmartDashboard.putNumber("Right Speed", self.rencoder.getRate())
            #wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())
        wpilib.SmartDashboard.putNumber("Left Front Distance", self.lfencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Right Front Distance", self.rfencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Left Back Distance", self.lbencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Right Back Distance", self.rbencoder.getDistance())
        wpilib.SmartDashboard.putNumber("Left Front Speed", self.lfencoder.getRate())
        wpilib.SmartDashboard.putNumber("Right Front Speed", self.rfencoder.getRate())
        wpilib.SmartDashboard.putNumber("Left Back Speed", self.lbencoder.getRate())
        wpilib.SmartDashboard.putNumber("Right Back Speed", self.rbencoder.getRate())
        #wpilib.SmartDashboard.putNumber("Gyro", self.gyro.getAngle())

# drive forward function
    def drive_forward(self, speed) :
@@ -92,6 +118,13 @@ class driveTrain(Component) :

# manual drive function for Tank Drive
    def xboxTankDrive(self, leftSpeed, rightSpeed):

        if (controller.leftBumperPressed == True): #Straight Button
            rightSpeed = leftSpeed
        if (controller.rightBumperPressed == True): #Slow Button
            rightSpeed = rightSpeed/2
            leftSpeed = leftSpeed/2

        self.lfmotor.set(leftSpeed)
        self.rfmotor.set(rightSpeed)
        self.lbmotor.set(leftSpeed)
@@ -103,8 +136,8 @@ class driveTrain(Component) :
        self.rfmotor.set(0)
        self.lbmotor.set(0)
        self.rbmotor.set(0)

'''

        '''
# function to tell us whether or not the goal distance has been reached
    def at_distance_goal(self):
        l_error = self.encoder_goal - self.l_encoder.getDistance()
@@ -117,7 +150,7 @@ class driveTrain(Component) :
            self.drive_forward(self.autonomousSpeed)

        self.drive_stop()
'''
        '''
# fucntion to reset the gyro
    def reset(self):
        if self.CONTROL_TYPE:
