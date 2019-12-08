'''
Created on Feb 13, 2019
DataUtil.py : Python class to convert Sensor Data to json and vice versa
@author: GANESHRAM KANAKASABAI
'''

import json
from project import SensorData
from project import ActuatorData


class DataUtil(object):
    '''
    DataUtil.py : Class to convert Sensor Data to json and vice versa
    @variable sensorData: Sensor Data object
    @variable ActuatorData: Actuator Data object
    @variable sJSONobj: Sensor Data string in JSON form
    @variable aJSONobj: Actuator Data string in JSON form
    @variable dict: JSON string
    @variable Sdata: default Sensor Data
    @variable Adata: default Actuator Data
    '''
    sensorData = None
    ActuatorData = None
    sJSONobj = None
    aJSONobj = None
    dict = None
    key = None
    Sdata = '{"timeStamp":"0", "temperature":"0", "pressure":"0", "humidity":"0"}'
    Adata = '{"timeStamp":"0", "temperatureactuator":"0", "humidityactuator":"0", "pressureactuator":"0"}'

    def __init__(self):
        '''
        DataUtil Constructor
        '''
        self.sensorData = SensorData.SensorData()
        self.sJSONobj = json.dumps(self.Sdata)
        self.ActuatorData = ActuatorData.ActuatorData()
        self.aJSONobj = json.dumps(self.Adata)
        
    def toJsonFromSensorData(self, sensorData):
        '''
        Function to convert Sensor Data to JSON
        @param sensordata: Sensor Data object
        @return sJSONobj: sJSONobj JSON string on success, null on failure
        '''
        self.dict = {}
        self.dict['temperature'] = sensorData.temperature
        self.dict['pressure'] = sensorData.pressure
        self.dict['humidity'] = sensorData.humidity
        self.sJSONobj = json.dumps(self.dict)
        if (self.sJSONobj != None):
            sOutfile = open('SensorDatatoJSON.txt', 'w')
            sOutfile.write(self.sJSONobj)
            return self.sJSONobj
    
        return None
    
    def toSensorDataFromJson(self, JSON):
        '''
        Function to convert JSON to Sensor data
        @param JSON: JSON string
        @return sensorData: Sensor Data object on success, null on failure
        '''
        self.dict = json.loads(JSON)


        if (self.dict != None):
            self.sensorData.temperature = self.dict['temperature']
            self.sensorData.pressure = self.dict['pressure']
            self.sensorData.humidity = self.dict['humidity']
            return self.sensorData
        
        return None
        
    def toJsonFromActuatorData(self, ActuatorData):
        '''
        Function to convert Actuator Data to JSON
        @param ActuatorData: Actuator Data object
        @return aJSONobj: aJSONobj JSON string on success, null on failure
        '''
        self.aJSONobj = json.dumps(ActuatorData.__dict__)
        if (self.aJSONobj != None):
            aOutfile = open('ActuatorDatatoJSON.txt', 'w')
            aOutfile.write(self.aJSONobj)
            return self.aJSONobj
    
        return None
    
    def toActuatorDataFromJson(self, JSON):
        '''
        Function to convert JSON to Sensor data
        @param JSON: JSON string
        @return actuatorData: Sensor Data object on success, null on failure
        '''
        self.dict = json.loads(JSON)
        if (self.dict != None):
            self.ActuatorData.timeStamp = self.dict["timeStamp"]
            self.ActuatorData.temperatureactuator = self.dict["tempact"]
            self.ActuatorData.humidityactuator = self.dict["humidact"]
            self.ActuatorData.pressureactuator = self.dict["preact"]
            return self.ActuatorData
        
        return None
        '''
        Function to update the Actuator Data
        @param topic :This indicates the value from the endpoint
        @param JSON : JSON String
        '''
    def updateActuatorData(self, topic, JSON):
        print('Inside updateActuatorData ' + topic +'JSON :' + JSON)
        self.dict = json.loads(JSON)
        self.key = self.parseTopic(topic)
        print('key is ' + self.key)
        if (self.key != None):
            if (self.key == "tempact"):
                self.ActuatorData.temperatureactuator = self.dict["value"]
            elif(self.key == "preact"):
                self.ActuatorData.pressureactuator = self.dict["value"]
            elif(self.key == "humidact"):
                self.ActuatorData.humidityactuator = self.dict["value"]
                
        print(self.ActuatorData)
            
        '''
        Function to parse the end point value to get the topic
        @param  topic : This indicates the value from the endpoint
        '''
    def parseTopic(self, topic):
        return topic.rsplit('/', 1)[-1]