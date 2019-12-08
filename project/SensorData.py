'''
Created on Dec 05, 2019
SensorData.py : python class to calculate and categorize required value from sensor data 
@author: Smit2
'''

import os
from datetime import datetime

class SensorData(object):
    '''
    SensorData - class to calculate and categorize required value from sensor data.
    @var timeStamp: present date and time.
    '''
    temperature = 0
    pressure = 0
    humidity = 0
    
    def __init__(self):
        '''
        SensorData constructor, initializes the time.
        '''
        self.timeStamp = str(datetime.now())
        self.totValue = [0, 0, 0]
        self.avgValue = [0, 0, 0]
        self.sampleCount = 0
        
        
    def addValue(self, newVal):
        '''
        calculates and categorizes required values from sensor readings.
        @param newVal: new sensor value.
        '''
        print('\n--------------------')
        print('Sensor readings : ' + str(newVal) )
        
        self.sampleCount += 1
        self.timeStamp = str(datetime.now())
        self.temperature = newVal[0]
        self.pressure = newVal[1]
        self.humidity = newVal[2]
        self.totValue[0] += newVal[0]
        self.totValue[1] += newVal[1]
        self.totValue[2] += newVal[2]
        
        i = 0
        for x in self.totValue :
            if (x != 0 and self.sampleCount > 0):
                self.avgValue[i] = (x / self.sampleCount)
            i += 1


    def __str__(self):
        '''
        returns the string representation of the SensorData object.
        @return: 'customStr' - SensorData object in string.
        '''
        customStr = \
        os.linesep + '\ttimeStamp: ' + self.timeStamp + \
        os.linesep + '\ttemperature: ' + str(self.temperature) + \
        os.linesep + '\tpressure: ' + str(self.pressure) + \
        os.linesep + '\thumidity: ' + str(self.humidity)
        return customStr
