'''
Created on Feb 13, 2019
TempManagementApp.py : Temperature sensor and actuator python application
@author: GANESHRAM KANAKASABAI
'''

from project import SensorAdaptor
'''
TempSensorAdaptor instance variable
'''
Emulator = None  
'''
getting singleton instance of the TempSensorAdaptor
'''
Emulator = SensorAdaptor.SensorAdaptor().getInstance()  
'''
initiating the daemon
'''
Emulator.daemon = True  
'''
enabling the thread to begin TempSensorAdaptor
'''
Emulator.setSensorAdaptor(True)  
'''
starting the TempSensorAdaptor thread
'''
Emulator.start()  

'''
An infinite loop is being created
'''
while(True):
    pass
