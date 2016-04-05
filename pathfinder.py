# Pathfinder script for the Pi2Go robot project for Raspberry Pi
# The robot will follow a line on the floor until it detects and obstacle.
# When it finds one, it turns around until it finds the line again.

import time, pi2go

# Variables
goForward = True
turnLeft = False
turnRight = False
turnAround = False
rightSensorFoundTurnLine = False
foundLineAfterTurn = False
alreadyTurned = False
movingSpeed = 38

# Initialize pi2go
pi2go.init()

# Robot loop
try:
    while True:
        
        # -----------------------------------------------
        # Movement modes
        # -----------------------------------------------
        
        # Go forward
        if (goForward):
            pi2go.go(movingSpeed, movingSpeed)
            
        # Turn right
        if (turnRight):
            # Turn right until right sensor doesn't recognize the line anymore 
            pi2go.go(30, -30)
            if (pi2go.irRightLine()):
                goForward = True
                turnLeft = False
                turnRight = False        
                turnAround = False
        # Turn left
        if (turnLeft):
            # Turn left until left sensor doesn't recognize the line anymore 
            pi2go.go(-30, 30)
            if (pi2go.irLeftLine()):
                goForward = True
                turnLeft = False
                turnRight = False       
                turnAround = False
                
        # Turn around
        while turnAround:     
            # Turn right fast until the both sensor detects a line    
            pi2go.go(70, -70)
       
            if (not pi2go.irRightLine()):
                rightSensorFoundTurnLine = True;
           
            if (not pi2go.irLeftLine() and rightSensorFoundTurnLine):
                # Both sensor detected a line, which means that we are over turned.
                # Slowly turn back now, until right sensor finds the line.
                while (not foundLineAfterTurn):
                    pi2go.go(-35, 35)
                    
                    if (not pi2go.irRightLine()):
                        foundLineAfterTurn = True
                        print "Stop."
                        pi2go.stop()
                        turnAround = False
                        alreadyTurned = True
            
        # -----------------------------------------------
        # Check sensors and set flags for movement modes
        # -----------------------------------------------
            
        # Check right sensor
        if (not pi2go.irRightLine()):
             goForward = False
             turnLeft = False
             turnRight = True
             turnAround = False
             
        # Check left sensor
        if (not pi2go.irLeftLine()):
            goForward = False
            turnLeft = True
            turnRight = False
            turnAround = False
             
        # Check front sensor        
        distance1 = pi2go.getDistance()
        distance2 = pi2go.getDistance()
        # Check distance twice to avoid measuring errors that sometimes occur
        if (distance1 < 8.0 and distance1 < 8.0 and not turnAround and not alreadyTurned):
            print "Obstacle detected. Initializing turn..."
            print "Distance 1: ", distance1
            print "Distance 2: ", distance2
            goForward = False
            turnLeft = False
            turnRight = False
            turnAround = True
             
                          
except KeyboardInterrupt:
    print

finally:
    pi2go.cleanup()
