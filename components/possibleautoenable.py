logger.info("Begin autonomous")

    if iter_fn is None:
        iter_fn = lambda: None

    # keep track of how much time has passed in autonomous mode
    timer = wpilib.Timer()
    timer.start()

    try:
        self._on_autonomous_enable()
    except:
        if not self.ds.isFMSAttached():
            raise

    #
    # Autonomous control loop
    #

    delay = PreciseDelay(control_loop_wait_time)

    while self.ds.isAutonomous() and self.ds.isEnabled():

        try:
            self._on_iteration(timer.get())
        except:
            if not self.ds.isFMSAttached():
                raise

        iter_fn()

        delay.wait()

    #
    # Done with autonomous, finish up
    #

    try:
        self._on_autonomous_disable()
    except:
        if not self.ds.isFMSAttached():
            raise

    logger.info("Autonomous mode ended")

#
#   Internal methods used to implement autonomous mode switching, and
#   are called automatically
#

def _on_autonomous_enable(self):

    '''Selects the active autonomous mode and enables it'''
    self.active_mode = self.chooser.getSelected()
    if self.active_mode is not None:
        logger.info("Enabling '%s'" % self.active_mode.MODE_NAME)
        self.active_mode.on_enable()
    else:
        logger.warn("No autonomous modes were selected, not enabling autonomous mode")

def _on_autonomous_disable(self):
    '''Disable the active autonomous mode'''
    if self.active_mode is not None:
        logger.info("Disabling '%s'" % self.active_mode.MODE_NAME)
        self.active_mode.on_disable()

    self.active_mode = None

def _on_iteration(self, time_elapsed):
    '''Run the code for the current autonomous mode'''
    if self.active_mode is not None:
        self.active_mode.on_iteration(time_elapsed)
