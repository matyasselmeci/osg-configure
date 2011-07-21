#!/usr/bin/env python

import os, imp, sys, unittest, ConfigParser, logging

# setup system library path
if "CONFIGURE_OSG_LOCATION" in os.environ:
    pathname = os.path.join(os.environ['CONFIGURE_OSG_LOCATION'], 'bin')
else:
    if "VDT_LOCATION" in os.environ:
        pathname = os.path.join(os.environ['VDT_LOCATION'], 'osg', 'bin')
        if not os.path.exists(os.path.join(pathname, 'configure-osg')):
          pathname = '../lib/python/'
    else:
      pathname = '../lib/python/'
          
sys.path.append(pathname)


from configure_osg.modules import exceptions
from configure_osg.modules import utilities

from configure_osg.configure_modules import condor

global_logger = logging.getLogger('test condor configuration')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
global_logger.addHandler(console)

class TestCondor(unittest.TestCase):
  """
  Unit test class to test CondorConfiguration class
  """


  def testParsing(self):
    """
    Test condor parsing
    """
    
    config_file = os.path.abspath("./configs/condor/condor1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    options = {'OSG_JOB_MANAGER_HOME' : '/opt/condor',
               'OSG_CONDOR_LOCATION' : '/opt/condor',
               'OSG_CONDOR_CONFIG' : '/etc/condor/condor_config',
               'OSG_JOB_CONTACT' : 'my.domain.com/jobmanager-condor',
               'OSG_UTIL_CONTACT' : 'my.domain.com/jobmanager',
               'OSG_WS_GRAM' : 'Y',
               'OSG_JOB_MANAGER' : 'Condor'}
    for option in options:
      value = options[option]
      self.failUnless(attributes.has_key(option), 
                      "Attribute %s missing" % option)
      err_msg = "Wrong value obtained for %s, " \
                "got %s instead of %s" % (option, attributes[option], value)
      self.failUnlessEqual(attributes[option], value, err_msg)




  def testParsingDisabled(self):
    """
    Test condor parsing when disabled
    """
    
    config_file = os.path.abspath("./configs/condor/condor_disabled.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnlessEqual(len(attributes), 0, 
                         "Disabled configuration should have no attributes")
    
  def testParsingIgnored(self):
    """
    Test condor parsing when ignored
    """
    
    config_file = os.path.abspath("./configs/condor/ignored.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnlessEqual(len(attributes), 0, 
                         "Disabled configuration should have no attributes")


  def testParsingDefaults(self):
    """
    Test handling of defaults when parsing a configuration
    """
    
    config_file = os.path.abspath("./configs/condor/condor_defaults1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    # test getting defaults from vdtsetup variables
    # check getting values from VDTSETUP variables
    os.environ['VDTSETUP_CONDOR_LOCATION'] = '/my/condor'
    os.environ['VDTSETUP_CONDOR_CONFIG'] = '/my/condor/etc/condor_config'
    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/my/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/my/condor/etc/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')

    # does condor_config get calculated properly if 
    # vdtsetup_condor_config is missing?
    del os.environ['VDTSETUP_CONDOR_CONFIG']      
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/my/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/my/condor/etc/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')

    # check to see if we can get values from condor_* variables
    del os.environ['VDTSETUP_CONDOR_LOCATION']
    os.environ['CONDOR_LOCATION'] = '/my/condor'
    os.environ['CONDOR_CONFIG'] = '/my/condor/etc/condor_config'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/my/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/my/condor/etc/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')
    
    # check when condor_config is not present
    del os.environ['CONDOR_CONFIG']
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/my/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/my/condor/etc/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')


    # check to make sure that config values take precedence over 
    # environment variables
    config_file = os.path.abspath("./configs/condor/condor1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
    os.environ['CONDOR_LOCATION'] = '/my/condor1'
    os.environ['VDTSETUP_CONDOR_LOCATION'] = '/my/condor2'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/opt/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/etc/condor/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')

    # check to see if jobmanager home values get used in preference to other values
    config_file = os.path.abspath("./configs/condor/condor_defaults2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
    os.environ['CONDOR_LOCATION'] = '/my/condor1'
    os.environ['VDTSETUP_CONDOR_LOCATION'] = '/my/condor2'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_CONDOR_LOCATION'), 
                    'Attribute OSG_CONDOR_LOCATION missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_LOCATION'], '/usr/local/condor', 
                         'Wrong value obtained for OSG_CONDOR_LOCATION')
  
    self.failUnless(attributes.has_key('OSG_CONDOR_CONFIG'), 
                    'Attribute OSG_CONDOR_CONFIG missing')
    self.failUnlessEqual(attributes['OSG_CONDOR_CONFIG'], 
                         '/usr/local/condor/etc/condor_config', 
                         'Wrong value obtained for OSG_CONDOR_CONFIG')

  def testAttributeGeneration1(self):
    """
    Test the creation of a config file given attributes
    """
    
    config_file = os.path.abspath("./configs/condor/condor1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    new_config = ConfigParser.SafeConfigParser()
    settings.generateConfigFile(attributes.items(), new_config)
    section_name = 'Condor'
    self.failUnless(new_config.has_section(section_name), 
                    "%s section not created in config file" % section_name)
    
    options = {'enabled' : 'True',
               'job_contact' : 'my.domain.com/jobmanager-condor',
               'util_contact' : 'my.domain.com/jobmanager',
               'wsgram' : 'True',               
               'condor_location' : '/opt/condor',
               'condor_config' : '/etc/condor/condor_config'}
    for option in options:      
      self.failUnless(new_config.has_option(section_name, option), 
                      "Option %s missing" % option)
      self.failUnlessEqual(new_config.get(section_name, option), 
                           options[option], 
                           "Wrong value obtained for %s, expected %s, got %s" %
                           (option,
                            options[option],
                            new_config.get(section_name, option)))
                            
    
  def testAttributeGeneration2(self):
    """
    Test the creation of a config file given attributes
    """
    
    config_file = os.path.abspath("./configs/condor/condor_disabled.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()    
    new_config = ConfigParser.SafeConfigParser()
    settings.generateConfigFile(attributes.items(), new_config)
    section_name = 'Condor'
    self.failIf(new_config.has_section(section_name), 
                "%s section created in config file" % section_name)
    
                            
  def testMissingCondorLocation(self):
    """
    Test the checkAttributes function to see if it catches missing condor location
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/condor/missing_location.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()    
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice missing condor location")

  def testMissingCondorConfig(self):
    """
    Test the checkAttributes function to see if it catches missing
    condor config locations
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    for filename in ["./configs/condor/missing_config1.ini", 
                     "./configs/condor/missing_config2.ini"]:
      config_file = os.path.abspath(filename)
      configuration = ConfigParser.SafeConfigParser()
      configuration.read(config_file)
  
      settings = condor.CondorConfiguration(logger=global_logger)
      try:
        settings.parseConfiguration(configuration)
      except Exception, e:
        self.fail("Received exception while parsing configuration: %s" % e)
   
      attributes = settings.getAttributes()      
      self.failIf(settings.checkAttributes(attributes), 
                  "Did not notice missing condor config location: " + 
                  attributes['OSG_CONDOR_CONFIG'] )

  def testValidSettings(self):
    """
    Test the checkAttributes function to see if it works on valid settings
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/condor/check_ok.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct settings incorrectly flagged as missing")

  def testValidSettings2(self):
    """
    Test the checkAttributes function to see if it works on valid settings
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/condor/check_ok2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct settings incorrectly flagged as missing")

    
  def testInvalidJobContact(self):
    """
    Test the checkAttributes function to see if it catches invalid job contacts
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/condor/invalid_job_contact.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid host in jobcontact option")

  def testInvalidUtilityContact(self):
    """
    Test the checkAttributes function to see if it catches invalid
    utility contacts
    """
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/condor/invalid_utility_contact.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = condor.CondorConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid host in utility_contact option")
    
if __name__ == '__main__':
    unittest.main()