'''
ConfigUtil.py : Configuration properties utility python class
@author: Smit2
Created on Dec 5 2019
'''

import configparser
import os
from project import ConfigConst

class ConfigUtil(object):
    '''
    ConfigUtil - Utility class to load and get configuration properties.
    @variable configConst:  ConfigConst instance.
    @variable isLoaded: boolean to check whether configuration file is loaded or not.
    @variable configFilePath: path of configuration file.
    @variable configData: configparser instance.
    '''
    configConst = None
    isLoaded = False
    configFilePath = None
    configData = None


    def __init__(self):
        '''
        ConfigUtil Constructor to initialize.
        '''
        if (self.configData == None):
            self.configData = configparser.ConfigParser()
        if (self.configConst == None):
            self.configConst = ConfigConst.ConfigConst()

        self.configFilePath = self.configConst.DEFAULT_CONFIG_FILE_NAME
    
    
    def isConfigDataLoaded(self):
        '''
        checks whether configuration file is loaded.
        @return: 'isLoaded' - True, if configuration file is loaded else False. 
        '''
        return self.isLoaded

    
    def loadConfig(self):
        '''
        reads the properties from configuration file and sets 'isLoaded' member variable.
        '''
        if (os.path.exists(self.configFilePath)):
            self.configData.read(self.configFilePath)
            self.isLoaded = True

            
    def getConfigFile(self):
        '''
        returns the configuration file path.
        @return: 'configFilePath' - path of the configuration file.
        '''
        return self.configFilePath


    def getConfigData(self, forceReload = False):
        '''
        loads the configuration properties data and return's it.
        @param forceReload: False, to forcefully reload the configuration file else True.
        @return: 'configData' - configuration file data.
        '''
        if (self.isLoaded == False or forceReload):
            self.loadConfig()
        return self.configData

    
    def getProperty(self, section, key, forceReload = False):
        '''
        returns the individual property's value under the given section.
        @param section: name of the section in configuration file.
        @param key: name of the key under the section whose value is needed.
        @return: value of a given property.
        '''
        return self.getConfigData(forceReload).get(section, key)    
