'''
Created on Dec 5 2019
ActuatorAdaptor.py : class to process actuator message and set message to SenseHat
@author: Smit2
'''

from project import ActuatorData
from project import SenseHatLedActivator
from project import SmtpClientConnector

class ActuatorAdaptor(object):
    '''
    ActuatorAdaptor - class to process actuator message, update it and set message to SenseHat
    @variable ActuatorData: instance of ActuatorData class
    @variable SenseHatLedActivator: instance of SenseHatLedActivator class
    '''

    ActuatorData = None
    SenseHatLedActivator = None
    
    def __init__(self):
        '''
        ActuatorAdaptor Constructor
        '''
        self.ActuatorData = ActuatorData.ActuatorData()
        self.connector = SmtpClientConnector.SmtpClientConnector()
        self.SenseHatLedActivator = SenseHatLedActivator.SenseHatLedActivator()
        self.SenseHatLedActivator.setEnableLedFlag(True)    #Enable the SenseHatLedActivator Thread
        self.SenseHatLedActivator.start()   #Start the SenseHatLedActivator Thread


    def processMessage(self, key, pActuatorData):
        '''
        function to process ActuatorData, update it and set message to SenseHat
        @param pActuatorData: ActuatorData that needs to be processed
        '''
        if (key != None):
            if(self.ActuatorData != pActuatorData):
                if (key == "tempact"):
                    self.SenseHatLedActivator.setDisplayMessage('temperature set to ' + str(pActuatorData.temperatureactuator) + ' ˚C ');
                    self.connector.publishMessage('Alert ! Temperature range breached' , 'setting temperature to' + str(abs(pActuatorData.temperatureactuator)) + ' ˚C ')
                elif(key == "preact"):
                    self.SenseHatLedActivator.setDisplayMessage('pressure set to ' + str(pActuatorData.pressureactuator) + ' Pa ');
                    self.connector.publishMessage('Alert ! Pressure range breached' , 'setting pressure to ' + str(abs(pActuatorData.pressureactuator)) + ' Pa ')
                elif(key == "humidact"):
                    self.SenseHatLedActivator.setDisplayMessage('humidity set to ' + str(pActuatorData.humidityactuator) + ' RH ');
                    self.connector.publishMessage('Alert ! Humidity range breached', 'setting humidity to ' + str(abs(pActuatorData.humidityactuator)) + ' RH ')
        self.ActuatorData.updateData(pActuatorData)
