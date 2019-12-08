'''
Created on Feb 13, 2019
TempSensorAdaptor.py : Temperature sensor adaptor python class
@author: GANESHRAM KANAKASABAI
'''

import threading
import random  # import to generate random values within a range 
from project import SensorData
from project import ActuatorData
from project import ActuatorAdaptor
from sense_hat import SenseHat
from time import sleep
from project import DataUtil
from project import MqttPubClient
from project import MqttSubClient
from project import HTTPClientPublisher

UBIDOTS_DEVICE_LABEL = "warehouse"
UBIDOTS_VARIABLE_TEMPERATURE_LABEL = "tempact"
UBIDOTS_VARIABLE_PRESSURE_LABEL = "preact"
UBIDOTS_VARIABLE_HUMIDITY_LABEL = "humidact"
UBIDOTS_VARIABLES = [UBIDOTS_VARIABLE_TEMPERATURE_LABEL, UBIDOTS_VARIABLE_PRESSURE_LABEL, UBIDOTS_VARIABLE_HUMIDITY_LABEL]


class SensorAdaptor(threading.Thread):
    '''
    TempSensorAdaptor - Class to get system's temperature sensor readings, send mail and take action.
    @var __instance: singleton TempSensorAdaptor class instance variable.
    @var sensorData: instance of SensorData class.
    @var connector: instance of SmtpClientConnector class.
    @var ActuatorData: instance of ActuatorData class.
    @var ActuatorEmulator: instance of ActuatorEmulator class.
    @var SenseHat: instance of SenseHat class.
    @var curTemp: current temperature sensor value.
    @var prevTemp: previous temperature sensor value.
    @var lowVal: lowest value in temperature sensor value range.
    @var highVal: highest value in temperature sensor value range.
    @var isPrevSensorReadingsSet: boolean to check whether previous sensor readings value is set or not.
    @var alertDiff: temperature sensor difference threshold value to trigger alert.
    @var timeInterval: regular time intervals to sense and process temperature sensor value. 
    @var tempDiff: temperature difference.
    @var nominalTemp: normal temperature value.    
    '''
    __instance = None
    sensorData = None 
    ActuatorData = None
    ActuatorEmulator = None
    SenseHat = None
    sensorReading = None
    curTemp = 0
    prevTemp = 0
    curPressure = 0
    prevPressure = 0
    curHumidity = 0
    prevHumidity = 0
    isPrevSensorReadingsSet = False
    timeInterval = 0
    DataUtil = None
     
    @staticmethod 
    def getInstance():
        '''
        Static access method for singleton implementation.
        @return: '__instance' - singleton TempSensorEmulator class instance.
        '''
        if SensorAdaptor.__instance == None:
            SensorAdaptor()
        return SensorAdaptor.__instance

    def __init__(self):
        '''
        TempSensorEmulator Constructor to initialize.
        '''
        if SensorAdaptor.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.beginEmulator = False
            self.threadName = "SensorAdaptor"
            self.sensorData = SensorData.SensorData()
            self.sensorReading = [0, 0, 0]
            self.curTemp = 0
            self.prevTemp = 0
            self.curPressure = 0
            self.prevPressure = 0
            self.curHumidity = 0
            self.prevHumidity = 0
            self.tempDiff = 0
            self.isPrevSensorReadingsSet = False
            self.timeInterval = 120
            self.ActuatorData = ActuatorData.ActuatorData()
            self.ActuatorAdaptor = ActuatorAdaptor.ActuatorAdaptor()
            self.SenseHat = SenseHat()
            self.DataUtil = DataUtil.DataUtil()
            
            self.MQTTsubscriber = MqttSubClient.MqttSubClient()
            self.HTTPpublisher = HTTPClientPublisher.HTTPClientPublisher()
            threading.Thread.__init__(self)
            SensorAdaptor.__instance = self

    def setSensorAdaptor(self, value):
        '''
        Function to begin the Sensor Adaptor.
        @param value: True to start the Sensor Adaptor else False.  
        '''
        self.beginEmulator = value 
        
    def run(self):
        '''
        Thread function
        '''
        self.MQTTsubscriber.connect()
        self.MQTTsubscriber.subscribe(UBIDOTS_VARIABLES)
        while True:
            if self.beginEmulator:
                '''
                getting the temperature data from the SenseHat
                '''
                self.curTemp = self.SenseHat.get_temperature()  
                self.sensorReading[0] = self.curTemp
                '''
                getting the pressure data  from the SenseHat
                '''
                self.curPressure = self.SenseHat.get_pressure() 
                self.sensorReading[1] = self.curPressure
                '''
                getting the humidity data from the SenseHat
                '''
                self.curHumidity = self.SenseHat.get_humidity()  
                self.sensorReading[2] = self.curHumidity
                
                self.sensorData.addValue(self.sensorReading)
                
                if self.isPrevSensorReadingsSet == False:
                    self.prevTemp = self.curTemp
                    self.prevPressure = self.curPressure
                    self.prevHumidity = self.curHumidity
                    self.isPrevSensorReadingsSet = True
                else:
                    print("Sensor json data : " + self.DataUtil.toJsonFromSensorData(self.sensorData))
                    self.MQTTsubscriber.subscribe(UBIDOTS_VARIABLES)
                    
                    if self.HTTPpublisher.publish(UBIDOTS_DEVICE_LABEL, self.DataUtil.toJsonFromSensorData(self.sensorData)) == False:
                        return
                    
                    #self.ActuatorAdaptor.processMessage(self.MQTTsubscriber.connector.dataUtil.key, self.MQTTsubscriber.connector.dataUtil.ActuatorData)     
            #sleep(self.timeInterval)
        self.MQTTsubscriber.disconnect()
