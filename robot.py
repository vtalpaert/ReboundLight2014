'''
Created on 7 mai 2014

@author: victor-clevo
'''
# In this file are listed functions specific to the Raspberry Pi

import logging
try:
    import RPi.GPIO as GPIO
    rpi = True
except ImportError as details :
    logging.error(' no RPi library found ({})'.format(details))
    rpi = False


class BaseRobot(object):
    def __init__ (self):
        # initialize
        self.task = 'stop'
        self.last_task = 'stop'
        self.arret()

    # Full definition of the 7 functions
    def zero(self):
        logging.info('Robot : LED goes to 0 (simulation)')

    def un(self):
        logging.info('Robot : LED goes to 1 (simulation)')

    def arret(self):
        logging.info('Robot : Robot stops (simulation)')

    def avance(self):
        logging.info('Robot : Goes forward (simulation)')

    def recule(self):
        logging.info('Robot : Goes backward (simulation)')

    def droite(self):
        logging.info('Robot : Goes right (simulation)')

    def gauche(self):
        logging.info('Robot : Goes left (simulation)')

    # function working for both LED or motors setups
    def execute(self):
        if self.last_task == self.task:
            return
        elif self.task == 'stop':
            self.arret()
        elif self.task == 'avance':
            self.marche()
        elif self.task == 'droite':
            self.droite()
        elif self.task == 'gauche':
            self.gauche()
        elif self.task == 'recule':
            self.recule()
        elif self.task == '0':
            self.zero()
        elif self.task == '1':
            self.un()
        else:
            logging.info('Robot : ERROR, unexpected command. Did client send a compatible string?')
        self.last_task = self.task

    # when quitting, executed from server.py
    def quit(self):
        logging.info('End of simulation')

class Robot(BaseRobot):
    try:
        import RPi.GPIO as GPIO
    except ImportError as details :
        logging.error(' no RPi library found ({})'.format(details))


    def __init__ (self):
        
        # parameters
        self.n = 11  # GPIO number for the LED
        self.h = 15  # input 1
        self.j = 16  # input 2
        self.k = 18  # input 3
        self.l = 22  # input 4

        # GPIO initialisation
        GPIO.cleanup()  # used to avoid bugs if restarting the server
        GPIO.setmode(GPIO.BOARD)
        for i in [self.n, self.h, self.j, self.k, self.l]:
            GPIO.setup(i, GPIO.OUT)
            GPIO.output(i, GPIO.LOW)

        BaseRobot.__init__(self)


    # Full definition of the 7 functions
    def zero(self):
        logging.info('Robot : LED goes to 0')
        GPIO.output(self.n, GPIO.LOW)

    def un(self):
        logging.info('Robot : LED goes to 1')
        GPIO.output(self.n, GPIO.HIGH)

    def arret(self):
        logging.info('Robot : Robot stops')
        GPIO.output(self.n, GPIO.LOW)
        GPIO.output(self.h, GPIO.LOW)
        GPIO.output(self.k, GPIO.LOW)
        GPIO.output(self.j, GPIO.LOW)
        GPIO.output(self.l, GPIO.LOW)

    def avance(self):
        logging.info('Robot : Goes forward')
        GPIO.output(self.j, GPIO.LOW)
        GPIO.output(self.l, GPIO.LOW)
        GPIO.output(self.h, GPIO.HIGH)
        GPIO.output(self.k, GPIO.HIGH)

    def recule(self):
        logging.info('Robot : Goes backward')
        GPIO.output(self.h, GPIO.LOW)
        GPIO.output(self.k, GPIO.LOW)
        GPIO.output(self.j, GPIO.HIGH)
        GPIO.output(self.l, GPIO.HIGH)

    def droite(self):
        logging.info('Robot : Goes right')
        GPIO.output(self.j, GPIO.LOW)
        GPIO.output(self.k, GPIO.LOW)
        GPIO.output(self.h, GPIO.HIGH)
        GPIO.output(self.l, GPIO.HIGH)

    def gauche(self):
        logging.info('Robot : Goes left')
        GPIO.output(self.h, GPIO.LOW)
        GPIO.output(self.l, GPIO.LOW)
        GPIO.output(self.j, GPIO.HIGH)
        GPIO.output(self.k, GPIO.HIGH)

    # clean end of program
    def quit(self):
        GPIO.cleanup()
        logging.info('Cleaned GPIOs')



