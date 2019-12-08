'''
Created on Jan 26, 2019
SenseHatLedActivator.py : SenseHat activator class for LED to show message
@author: GANESHRAM KANAKASABAI
'''

from time import sleep
from sense_hat import SenseHat
import threading

class SenseHatLedActivator(threading.Thread):
    '''
    SenseHatLedActivator : SenseHat activator class for LED to show message
    @param enableLed: to enable LED display thread
    @param rateInSec: LED display rate
    @param rotateDeg: angle of display
    @param sh: instance of SenseHat
    @param displayMsg: Message to display
    '''
    enableLed = False
    rateInSec = 1
    rotateDeg = 270
    sh = None
    displayMsg = None
     
     
    def __init__(self, rotateDeg = 270, rateInSec = 1):
        '''
        SenseHatLedActivator constructor
        @param rotateDeg: angle of rotation in degree
        @param rateInSec: time in seconds
        '''
        super(SenseHatLedActivator, self).__init__()
        
        if rateInSec > 0:
            self.rateInSec = rateInSec
        if rotateDeg >= 0:
            self.rotateDeg = rotateDeg
            
        self.sh = SenseHat()
        self.sh.set_rotation(self.rotateDeg)
         
         
    def run(self):
        '''
        SenseHatLedActivator thread function
        '''
        while True:
            if self.enableLed:
                if self.displayMsg != None:
                    self.sh.show_message(str(self.displayMsg))  #show scrolling LED message
                else:
                    #self.sh.show_letter(str('R'))
                    self.sh.show_letter('')
    
                sleep(self.rateInSec)
                self.sh.clear()

            sleep(self.rateInSec)
     
     
    def getRateInSeconds(self):
        '''
        function to get display rate
        @return: 'rateInSec' - time in seconds
        '''
        return self.rateInSec
 
 
    def setEnableLedFlag(self, enable):
        '''
        function to enable LED display
        @param enable: True, to set the LED flag else False 
        '''
        self.sh.clear()
        self.enableLed = enable
     
     
    def setDisplayMessage(self, msg):
        '''
        function to set the message to be displayed in LED
        @param msg: String message to be displayed
        '''
        self.displayMsg = msg
