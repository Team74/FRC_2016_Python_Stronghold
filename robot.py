#!/usr/bin/env python3
"""
    This is a good foundation to build your robot code on
"""

import wpilib                           #Importing required packages
from xbox import XboxController         #^
#from pyfrc.sim.pygame_joysticks import UsbJoysticks  #Not using these right now, but may be
#import pygame                                        #useful later, so we will
#from xbox2 import XboxController                     #save them until someone
                                                      #who knows better deletes them
                                                      #(Hescott)

CONTROL_LOOP_WAIT_TIME = 0.01#0.025 # waits, in order to stay in sync with our driver station

class MyRobot(wpilib.SampleRobot):

    def robotInit(self):
        self.controller = XboxController(0) #creates object of type XboxController, called controller.
                                            # It is expected to be at index location 0
        #self.stick = wpilib.Joystick(0) #Save for later

        self.lmotor = wpilib.CANTalon(1) #Creates an object called lMotor(Left Motor), and sets it to a CANTalon object
        self.rmotor = wpilib.CANTalon(0) #The CANTalon lets us mess with motor settings, which is why we create a motor object
                                         #of type CANTalon instead of mapping it directly to the Power Control Board
                                         #This also prevents the motor from recieving extra power "leaking" from the power Board,
                                         #which would make the motor randomly run when we didn't want it to.

        self.dashTimer = wpilib.Timer()     # Timer for SmartDashboard updating
        self.dashTimer.start()

        self.lencoder = wpilib.Encoder(0, 1) #Creates an object of type Encoder, called lencoder. It counts
        self.rencoder = wpilib.Encoder(2, 3) #the amount that a motor has rotated, and returns it in Direction and Distance variables

        #self.lsource = wpilib.interfaces.PIDSource.from_obj_or_callable(self.lencoder.setPIDSourceType(self.lencoder.getDistance()))
        #self.rsource = wpilib.interfaces.PIDSource.from_obj_or_callable(self.rencoder.setPIDSourceType(self.rencoder.getDistance()))
            #Requires testing, but is supposed to create 2 PIDSource objects from the getDistance() methods of each Encoder.
            #If it works, remove this comment and replace it with something more constructive(1/24/16, Hescott)
        #self.lpidcontroller = wpilib.PIDController(0, 0, 0, lsource, loutput)#Proportional, Integral, Derivative, Source, output
        #self.rpidcontroller = wpilib.PIDController(0, 0, 0, rsource, routput)
#test of PIDControllers,
#Link to PIDController page : http://robotpy.readthedocs.org/en/latest/wpilib/PIDController.html#wpilib.pidcontroller.PIDController
        self.routput = wpilib.interfaces.PIDOutput()
        self.loutput = wpilib.interfaces.PIDOutput()
        #Remember to make the output go to the SmartDashboard(1/24/16, Hescott)

    def disabled(self):
        while self.isDisabled():
            wpilib.Timer.delay(0.01)              # Wait for 0.01 seconds

    def autonomous(self):
        #while self.isAutonomous() and self.isEnabled():
        self.lencoder.reset() #sets the encoder values to 0 at the start of each call
        self.rencoder.reset()
###############################################################################
        currentSpeed = 0 #Set this to the desired speed
###############################################################################


        while self.isAutonomous() and self.isEnabled(): #Here just in case I have put the While loop in the wrong place(Hescott)             # remove the need to multiply by -1

            self.lmotor.set(currentSpeed)           #it is multiplied by -1 because of the motor polarity, switiching the wires would
            self.rmotor.set(currentSpeed*(-1))

            if currentSpeed == 0 or self.rencoder.getDistance() == 0 or self.lencoder.getDistance() == 0:
                LToRRatio = 1
                RToLRatio = 1
            else:
                LToRRatio = self.rencoder.getDistance() / self.lencoder.getDistance()
                RToLRatio = self.lencoder.getDistance() / self.rencoder.getDistance()     #Sets up ratios of left/right motor distance moved

            if LToRRatio != 0:                 #Checks for inconsistency. If it exists,
                correctValue = LToRRatio * currentSpeed#self.lencoder.getDistance() #here, it finds the difference
                self.lmotor.set(correctValue)                     #and here, it slows down the offending motor to match the lagging one
            elif RToLRatio != 0:               #Same as above, but for the opposite motor
                correctValue = RToLRatio * currentSpeed#self.rencoder.getDistance() #^
                self.rmotor.set(correctValue*(-1))                     #^
            elif (LToRRatio == 1) and (RToLRatio == 1):  #If they both work, continue to transmit the same speed
                self.rmotor.set(currentSpeed*(-1))
                self.lmotor.set(currentSpeed)

            if currentSpeed < 1:
                currentSpeed += 0.002
            print(self.rencoder.getDistance())
            print(self.lencoder.getDistance())
            wpilib.Timer.delay(0.05)
    def operatorControl(self): #This needs to be called OperatorControl and nothing else, this is a problem with wpilib(Hescott)
        wpilib.Timer.delay(CONTROL_LOOP_WAIT_TIME) #This is probably important?(Hescott)

        while self.isOperatorControl() and self.isEnabled(): #When both the robot is enabled and we are in TeleOp

            self.lmotor.set(self.controller.getLeftY()*(-1)) #Sets speed of the motor equal to the Y input of the left stick
            self.rmotor.set(self.controller.getRightY())     #Sets speed of the motor equal to the Y input of the right stick

#Both of these work, but the code above specifies for the xbox controller
# object, for the sake of overall cohesion

            #self.lmotor.set(self.stick.getRawAxis(1))
            #self.rmotor.set(self.stick.getRawAxis(5))

    def test(self):
        wpilib.LiveWindow.run()

if __name__ == "__main__":
    wpilib.run(MyRobot)
