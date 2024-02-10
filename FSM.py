class FiniteStateMachine:
    def __init__(self):
        # Define states
        self.states = [
                        "idle", 
                        "photo",
                        "centrifuge",
                        "power_low",
                        "ground_pass",
                        "safe",
                        "detumbling",
                        "initialBoot"
                       ]
        # Define actions
        self.actions = [
            
        ]
        self.antennaStatus = None #Bool determining deploy status of antenna    
        self.current_state = None
        self.action = None
        self.powerConsumptionDict = {}
        return

    def initialBoot(self):

        #initial boot --{post boot}--> safe mode 
        return
    

    
    def idle(self, action): # Decrement running power by x per second
        
        #idle --{picture command }--> camera
        #idle --{start transmission}--> ground pass
        #idle --{centrifuge command}--> centrifuge
        #idle --{orientation command}--> detumbling
        #idle --{critical SoC}--> low power mode
        #idle --{error}--> safe mode

        return
    
    def camera(self, action): # Decrement running power by x per second

        #The camera state automatically assumes that a photo is successful
        #camera --{None}--> idle 
        #camera --{Error}--> safe mode

        return
    
    def safe_mode(self, action): #When there is an error returns to low power state.

        #camera --{None and self.antenna = true}--> idle 
        #camera --{Error}--> safe mode


        return
    
    def detumbling(self, action, time): #When there is an error returns to low power state.
        """
        complete command will be None. Automatically assumes completed movement**
        """
        #detumbling --{complete}--> idle 
        #detumbling --{Error}--> safe mode

        return
    
    def centrifuge(self, action, time): #Accounts for centrifuge running for x amount of time
        
        """
        complete command will be None. Automatically assumes completed movement if no error**
        """
        #detumbling --{complete}--> idle 
        #detumbing--{Error}--> safe mode


        return

    def ground_pass(self, action, time):

        #ground pass --{complete}--> idle 
        #ground pass --{Error}--> safe mode

        return
    
    def low_power(self, action, time):
        
        #low power --{nominal SoC}--> idle 
        #ground pass --{Error}--> safe mode

        return
    
    