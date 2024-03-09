def __init__(self) -> None:
        self.actions = [
                        "ADCS_IDLE",
                        "ADCS_ACTUATE",
                        "ADCS_OFF"
                        "CAM_CAPTURE",
                        "CAM_OFF",
                        "OBC_LOW_POWER",
                        "OBC_IDLE",
                        "COMMS_IDLE",
                        "COMMS_RX",
                        "COMMS_TX",
                        "COMMS_TX_BEACON",
                        "COMMS_ANT_DEPLOY",
                        "CENT_TEST",
                        "CENT_OFF",
                        "EPS_IDLE",
                        "EPS_LOW_POWER"
                        ]

class stateTracker:
    def __init__(self):
        self.camera    = None;
        self.adcs      = None;
        self.comms     = None;
        self.eps       = None;
        self.obc       = None; 
        self.cent      = None; 

    def setAction(self, actions):
        for action in actions:
            if 'ADCS' in action:
                self.adcs = action
            if 'CAM' in action:
                self.camera = action
            if 'CENT' in action:
                self.cent = action
            if 'COMMS' in action:
                self.comms = action
            if 'EPS' in action:
                self.eps = action
            if 'OBC' in action:
                self.obc = action
        return
    
    def getState(self):
        return [self.adcs, self.camera, self.cent, self.comms, self.eps, self.obc]
    


stateMachine = stateTracker(); 
help = ["ADCS_ACTUATE", "COMMS_TX_BEACON", "CAM_CAPTURE", "EPS_IDLE", "CENT_OFF"]
stateMachine.setAction(help)
print(stateMachine.getState())





