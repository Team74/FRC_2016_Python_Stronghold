from robotpy_ext.autonomous import StatefulAutonomous, state, timed_state
from robotpy_ext.autonomous.selector import AutonomousModeSelector
from wpilib import SendableChooser
from components.drive import driveTrain

class spinIncessantlyAutonomous(StatefulAutonomous):

    MODE_NAME = 'Spin Incessantly'
    DEFAULT = True

    spin_direction = -1
    at_goal_state = ''
    drop = False

    chooser = SendableChooser()
    default_modes = []

    dt = driveTrain()

    def Initialize(self):
        pass

    '''
    def on_iteration(self, tm):
        print("Hello!")
        self.next_state(drive_distance())
    #    self.drive.auto_drive()
    # insert the initialized drive funciton
    # insert the initialized turn angle function
    # insert the initalized shoot ball function
    '''

# initially stopping the bot using a timed state
    @timed_state(first=True, duration=0.5, next_state='drive_distance')
    def drive_stop(self) :
        self.dt.drive_stop()

# drive forward
    @state()
    def drive_distance(self):
#        self.dt.drive_forward(0.4)
        self.dt.lmotor.set(.4)
        self.dt.rmotor.set(-.4)
        #self.next_state(self.done)

    def done(self) :
        pass
