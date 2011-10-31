#!/usr/bin/python

""" Module to handle squid configuration and setup """

import ConfigParser, os

from osg_configure.modules import exceptions
from osg_configure.modules import utilities
from osg_configure.modules import configfile
from osg_configure.modules import validation
from osg_configure.modules.configurationbase import BaseConfiguration

__all__ = ['SquidConfiguration']


class SquidConfiguration(BaseConfiguration):
  """Class to handle attributes related to squid configuration and setup"""
  
  def __init__(self, *args, **kwargs):
    # pylint: disable-msg=W0142
    super(SquidConfiguration, self).__init__(*args, **kwargs)
    self.logger.debug('SquidConfiguration.__init__ started')
    self.attributes = {'OSG_SQUID_LOCATION' : 'UNAVAILABLE',
                       'OSG_SQUID_POLICY' : 'UNAVAILABLE',
                       'OSG_SQUID_CACHE_SIZE' : 'UNAVAILABLE',
                       'OSG_SQUID_MEM_CACHE' : 'UNAVAILABLE'}        
    self.__mappings = {'location': 'OSG_SQUID_LOCATION', 
                       'policy': 'OSG_SQUID_POLICY',
                       'cache_size': 'OSG_SQUID_CACHE_SIZE',
                       'memory_size': 'OSG_SQUID_MEM_CACHE'}
    self.__local_dir = None
    self.config_section = 'Squid'
    self.logger.debug('SquidConfiguration.__init__ completed')
      
  def parseConfiguration(self, configuration):
    """Try to get configuration information from ConfigParser or SafeConfigParser object given
    by configuration and write recognized settings to attributes dict
    """
    self.logger.debug('SquidConfiguration.parseConfiguration started')
    
    self.checkConfig(configuration)

    if not configuration.has_section(self.config_section):
      self.enabled = False
      self.logger.debug("%s section not in config file" % self.config_section)
      self.logger.debug('SquidConfiguration.parseConfiguration completed')
      return
    
    if not self.setStatus(configuration):
      self.logger.debug('SquidConfiguration.parseConfiguration completed')    
      return True

    for setting in self.__mappings:
      self.logger.debug("Getting value for %s" % setting)
      temp = configfile.get_option(configuration, 
                                   self.config_section, 
                                   setting)
      self.attributes[self.__mappings[setting]] = temp
      self.logger.debug("Got %s" % temp)
    
    if (self.enabled and 
        self.attributes[self.__mappings['location']] is not None):
      location = self.attributes[self.__mappings['location']]
      if '/' in location:
        self.__local_dir = location
        self.attributes[self.__mappings['location']] = \
          "%s:3128" % utilities.get_hostname()        
      elif ":" not in location:        
        self.attributes[self.__mappings['location']] += ":3128"        
        
      
    temp = utilities.get_set_membership(configuration.options(self.config_section),
                                        self.__mappings,
                                        configuration.defaults().keys())
    for option in temp:
      if option == 'enabled':
        continue
      self.logger.warning("Found unknown option %s in %s section" % 
                           (option, self.config_section))   
    self.logger.debug('SquidConfiguration.parseConfiguration completed')

  
# pylint: disable-msg=W0613
  def checkAttributes(self, attributes):
    """Check attributes currently stored and make sure that they are consistent"""
    self.logger.debug('SquidConfiguration.checkAttributes started')
    attributes_ok = True
    if not self.enabled:
      self.logger.debug('squid not enabled')
      self.logger.debug('SquidConfiguration.checkAttributes completed')
      return attributes_ok

    if self.ignored:
      self.logger.debug('Ignored, returning True')
      self.logger.debug('SquidConfiguration.checkAttributes completed')
      return attributes_ok

    # Make sure all settings are present
    for setting in self.__mappings:
      if self.__mappings[setting] not in self.attributes:
        raise exceptions.SettingError("Missing setting for %s in %s section" %
                                      (setting, self.config_section)) 
    if (self.__local_dir is not None and
        not validation.valid_location(self.__local_dir)):
      self.logger.error("In %s section" % self.config_section)
      self.logger.error("Value given in location does not exist: %s" % 
                          self.attributes[self.__mappings['location']])
      attributes_ok = False
    (hostname, port) = self.attributes[self.__mappings['location']].split(':')
    if not validation.valid_domain(hostname, True):
      self.logger.error("In %s section, problem with hostname setting" % self.config_section)
      self.logger.error("Invalid hostname for squid location: %s" % \
                        self.attributes[self.__mappings['location']])
      attributes_ok = False
    try:
      int(port)
    except ValueError:
      self.logger.error("In %s section, problem with squid location setting" % \
                        self.config_section)
      self.logger.error("The port must be a number(e.g. host:3128) for squid " \
                        "location: %s" % self.attributes[self.__mappings['location']])
      
      attributes_ok = False
    
    if not utilities.blank(self.attributes[self.__mappings['memory_size']]):
      try:
        int(self.attributes[self.__mappings['memory_size']])
      except ValueError:
        self.logger.error("In %s section, memory_size must be an integer " \
                          "giving the in memory size of the squid " \
                          "proxy in MB" % self.config_section)      
        attributes_ok = False

    if not utilities.blank(self.attributes[self.__mappings['cache_size']]):
      try:
        int(self.attributes[self.__mappings['cache_size']])
      except ValueError:
        self.logger.error("In %s section, cache_size must be an integer " \
                          "giving the disk cache size of the squid " \
                          "proxy in MB" % self.config_section)      
        attributes_ok = False
        
    self.logger.debug('SquidConfiguration.checkAttributes completed')
    return attributes_ok 
  
# pylint: disable-msg=W0613
  def configure(self, attributes):
    """Configure installation using attributes"""
    self.logger.debug('SquidConfiguration.configure started')

    # disable configuration for now
    self.logger.debug('squid not enabled')
    self.logger.debug('SquidConfiguration.configure completed')
    return True
    
    if not self.enabled:
      self.logger.debug('squid not enabled')
      self.logger.debug('SquidConfiguration.configure completed')
      return True

    if self.ignored:
      self.logger.warning("%s configuration ignored" % self.config_section)
      self.logger.debug('SquidConfiguration.configure completed')
      return True

    self.logger.debug('SquidConfiguration.configure completed')
    return True     

  def moduleName(self):
    """Return a string with the name of the module"""
    return "Squid"
  
  def separatelyConfigurable(self):
    """Return a boolean that indicates whether this module can be configured separately"""
    return True
  
  def parseSections(self):
    """Returns the sections from the configuration file that this module handles"""
    return [self.config_section]
