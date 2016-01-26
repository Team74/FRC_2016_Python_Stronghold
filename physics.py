import wpilib
from pyfrc.physics.drivetrains import mecanum_drivetrain
from hal_impl.data import hal_data
class PhysicsEngine:


    def __init__(self, controller):
        self.controller = controller

        # keep track of the tote encoder position

        # keep track of the can encoder position
        self.toteAct = 1000
        self.canAct = 7000
        self.canCalibrated = False
    def initialize(self, hal_data):
        hal_data['dio'][0]['value'] = True
        hal_data['dio'][1]['value'] = True
        hal_data['dio'][2]['value'] = True
        hal_data['dio'][3]['value'] = True
        self.controller.add_gyro_channel(0)

    def update_sim(self, hal_data, now, tm_diff):
        if not self.canCalibrated:
            try:
                hal_data['CAN'][15]['limit_switch_closed_rev'] = True
            except:
                pass

        if hal_data['control']['enabled']:
        # Simulate the tote forklift
            try:
                toteDict = hal_data['CAN'][5]
                canDict = hal_data['CAN'][15]
                totePercentVal = int(toteDict['value']*tm_diff*2333/1023)
                canPercentVal = int(canDict['value']*tm_diff*2333/1023)
                posVal = int(tm_diff*2333)

            except:

                pass

            else:
                if toteDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus:
                    self.toteAct += totePercentVal
                    toteDict['enc_position'] += totePercentVal

                elif toteDict['mode_select'] == wpilib.CANTalon.ControlMode.Position:

                    if toteDict['enc_position']<toteDict['value']:
                        self.toteAct += posVal
                        toteDict['enc_position'] += posVal
                    else:
                        self.toteAct = posVal
                        toteDict['enc_position'] -= posVal


                if canDict['mode_select'] == wpilib.CANTalon.ControlMode.PercentVbus:
                    self.canAct += canPercentVal
                    canDict['enc_position'] += canPercentVal

                elif canDict['mode_select'] == wpilib.CANTalon.ControlMode.Position:

                    if canDict['enc_position'] < canDict['value']:
                        self.toteAct += posVal
                        canDict['enc_position'] += posVal

                    else:
                        self.toteAct -= posVal
                        canDict['enc_position'] -= posVal

                if canDict['enc_position'] < 0 and self.canCalibrated:
                    canDict['enc_position'] = 0
                elif canDict['enc_position'] >11000:
                    canDict['enc_position'] = 11000

                if self.toteAct in range (-50, 50):
                    hal_data['dio'][2]['value'] = False

                if self.canAct in range (-50, 50):
                    hal_data['CAN'][15]['limit_switch_closed_rev'] = False
                    self.canCalibrated = True
            # Simulate the can forklift

            # Do something about the distance sensors?

            # Gyro

            # Simulate the drivetrain
            lf_motor = hal_data['pwm'][0]['value']
            lr_motor = hal_data['pwm'][1]['value']
            rf_motor = -hal_data['pwm'][2]['value']
            rr_motor = -hal_data['pwm'][3]['value']

            vx, vy, vw = mecanum_drivetrain(lr_motor, rr_motor, lf_motor, rf_motor, speed=3)
            self.controller.vector_drive(vx, vy, vw, tm_diff)
