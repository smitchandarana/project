'''
ActuatorData.py : Python class to define ActuatorData object.
@author: Smit2
Created on Dec 5 2019I
'''

import os
from datetime import datetime

class ActuatorData(object):
    '''
    ActuatorData - class defines the ActuatorData object of Actuator
    @param timeStamp: contains the present date and time 
    @param name: name of actuator data
    @param hasError: boolean to check error
    @param command: type of command
    @param errCode: type of error
    @param statusCode: type of status 
    @param stateData: data of the ActuatorData's state
    @param val: ActuatorData value
    '''

    temperatureactuator = 0
    humidityactuator = 0
    pressureactuator = 0
    

    def __init__(self):
        '''
        ActuatorData Constructor
        '''
        self.updateTimeStamp()

    def updateData(self, data):
        '''
        function to update the ActuatorData
        @param data: ActuatorData 
        '''
        self.temperatureactuator = data.temperatureactuator
        self.humidityactuator = data.humidityactuator
        self.pressureactuator = data.pressureactuator


    def updateTimeStamp(self):
        '''
        function to update the date and time 
        '''
        self.timeStamp = str(datetime.now())


    def __str__(self):
        '''
        returns the string representation of the ActuatorData object.
        @return: 'customStr' - ActuatorData object in string.
        '''
        customStr = \
        os.linesep + '\ttimeStamp: ' + self.timeStamp + \
        os.linesep + '\ttemperatureactuator ' + str(self.temperatureactuator) + \
        os.linesep + '\thumidityactuator: ' + str(self.humidityactuator) + \
        os.linesep + '\tpressureactuator: ' + str(self.pressureactuator)
        return customStr
