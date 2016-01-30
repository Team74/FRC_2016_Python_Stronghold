from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
## noinspect on PyUnresolvedReferences
# Because python is dynamic and can do crazy crap, some IDEs complain that the subsystems
# aren't accessible in this object. They are, and the above comment fixes it for IntelliJ IDEA




class simpleAutonomous(StatefulAutonomous):

    MODE_NAME = 'Cross the low bar and score in the high goal'
    DEFAULT = True

    spin_direction = -1
    at_goal_state = ''
    drop = False

    chooser = SendableChooser()
    default_modes = []

    def on_iteration(self, tm):
        print("Hello!")
    #    self.drive.auto_drive()
    # insert the initialized drive funciton
    # insert the initialized turn angle function
    # insert the initalized shoot ball function

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='turn_angle')
    def drive_stop(self) :
        self.lmotor.set(0)
        self.rmotor.set(0)

# turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.drive_distance)

# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance()
        self.next_state(self.turn_angle)

#turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.drive_distance)

# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance()
        self.next_state(self.turn_angle)

#turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.at_goal_state)


# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance()
        self.next_state(self.shoot_ball)

# shoot ball
    @state()
    def shoot_ball(self):
        self.drive.set_angle_goal(28)
        self.at_goal_state = 'move_toward_tote2'
        self.next_state(self.done)

    def done(self) :
        pass
