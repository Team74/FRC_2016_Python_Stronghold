from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
## noinspect on PyUnresolvedReferences
# Because python is dynamic and can do crazy crap, some IDEs complain that the subsystems
# aren't accessible in this object. They are, and the above comment fixes it for IntelliJ IDEA




class skeletonAutonomous(StatefulAutonomous):
    MODE_NAME = 'Cross the low bar and score in the high goal'
    DEFAULT = True

    spin_direction = -1
    at_goal_state = ''
    drop = False

    def on_iteration(self, tm):

    #    self.drive.auto_drive()
    # insert the initialized drive funciton
    # insert the initialized turn angle function
    # insert the initalized shoot ball function

# turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.at_goal_state)

# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance:
        self.next_state(self.turn_angle)

#turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.at_goal_state)

# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance:
        self.next_state(self.turn_angle)

#turn on an angle
    @state()
    def turn_angle(self):
        if not self.drive.driving_angle:
            self.next_state(self.at_goal_state)


# drive forward
    @state()
    def drive_distance(self):
        self.drive.driving_distance:
        self.next_state(self.turn_angle)

# shoot ball
    @state()
    def shoot_ball(self):
        self.drive.set_angle_goal(28)
        self.at_goal_state = 'move_toward_tote2'
        self.next_state('drive_angle')
