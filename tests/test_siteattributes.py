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

from configure_osg.configure_modules import siteattributes

global_logger = logging.getLogger('test siteattributes configuration')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
global_logger.addHandler(console)

class TestSiteAttributesSettings(unittest.TestCase):
  """
  Unit test class to test SiteAttributes class
  """


  def testParsing1(self):
    """
    Test siteattributes parsing
    """
    
    config_file = os.path.abspath("./configs/siteattributes/siteattributes1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    variables = {'OSG_GROUP' : 'OSG-ITB',
                 'OSG_HOSTNAME' : 'my.host.com',
                 'OSG_SITE_NAME': 'MY_SITE',
                 'OSG_SPONSOR' : 'osg:100',
                 'OSG_SITE_INFO' : 'http://example/com/policy.html',
                 'OSG_CONTACT_NAME' : 'Admin Name',
                 'OSG_CONTACT_EMAIL' : 'myemail@example.com',
                 'OSG_SITE_CITY' : 'Chicago',
                 'OSG_SITE_COUNTRY' : 'US',
                 'OSG_SITE_LONGITUDE' : '84.23',
                 'OSG_SITE_LATITUDE' : '23.32'}
    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))
        
  def testParsing2(self):
    """
    Test siteattributes parsing
    """
    
    config_file = os.path.abspath("./configs/siteattributes/siteattributes2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    variables = {'OSG_GROUP' : 'OSG',
                 'OSG_HOSTNAME' : 'my.host.com',
                 'OSG_SITE_NAME': 'MY_SITE',
                 'OSG_SPONSOR' : 'osg:50 atlas:50',
                 'OSG_SITE_INFO' : 'http://example/com/policy.html',
                 'OSG_CONTACT_NAME' : 'Admin Name',
                 'OSG_CONTACT_EMAIL' : 'myemail@example.com',
                 'OSG_SITE_CITY' : 'Chicago',
                 'OSG_SITE_COUNTRY' : 'US',
                 'OSG_SITE_LONGITUDE' : '-84.23',
                 'OSG_SITE_LATITUDE' : '-23.32'}
    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))


  def testParsing3(self):
    """
    Test siteattributes parsing
    """
    
    config_file = os.path.abspath("./configs/siteattributes/siteattributes3.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    variables = {'OSG_GROUP' : 'OSG',
                 'OSG_HOSTNAME' : 'my.host.com',
                 'OSG_SITE_NAME': 'MY_SITE',
                 'OSG_SPONSOR' : 'osg:50 atlas:50',
                 'OSG_SITE_INFO' : 'http://example/com/policy.html',
                 'OSG_CONTACT_NAME' : 'Admin Name',
                 'OSG_CONTACT_EMAIL' : 'myemail@example.com',
                 'OSG_SITE_CITY' : 'Chicago',
                 'OSG_SITE_COUNTRY' : 'US',
                 'OSG_SITE_LONGITUDE' : '-84.23',
                 'OSG_SITE_LATITUDE' : '-23.32',
                 'resource_group' : 'RESOURCE_GROUP'}
    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))

  def testAttributeGeneration1(self):
    """
    Test the creation of a config file given attributes
    """
    
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/siteattributes/siteattributes1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    new_config = ConfigParser.SafeConfigParser()
    settings.generateConfigFile(attributes.items(), new_config)
    section_name = 'Site Information'
    self.failUnless(new_config.has_section(section_name), 
                    "%s section not created in config file" % section_name)
    
    options = {'group' : 'OSG-ITB',
               'host_name' : 'my.host.com',
               'site_name' : 'MY_SITE',
               'sponsor' : 'osg:100',
               'site_policy' : 'http://example/com/policy.html',
               'contact' : 'Admin Name',
               'email' : 'myemail@example.com',
               'city' : 'Chicago',
               'country' : 'US',
               'longitude' : '84.23', 
               'latitude' : '23.32'}
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
    
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/siteattributes/siteattributes2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    new_config = ConfigParser.SafeConfigParser()
    settings.generateConfigFile(attributes.items(), new_config)
    section_name = 'Site Information'
    self.failUnless(new_config.has_section(section_name), 
                    "%s section not created in config file" % section_name)
    
    options = {'group' : 'OSG',
               'host_name' : 'my.host.com',
               'site_name' : 'MY_SITE',
               'sponsor' : 'osg:50 atlas:50',
               'site_policy' : 'http://example/com/policy.html',
               'contact' : 'Admin Name',
               'email' : 'myemail@example.com',
               'city' : 'Chicago',
               'country' : 'US',
               'longitude' : '-84.23', 
               'latitude' : '-23.32'}
    for option in options:      
      self.failUnless(new_config.has_option(section_name, option), 
                      "Option %s missing" % option)
      self.failUnlessEqual(new_config.get(section_name, option), 
                           options[option], 
                           "Wrong value obtained for %s, expected %s, got %s" %
                           (option,
                            options[option],
                            new_config.get(section_name, option)))

    
                                                            

  def testMissingAttribute(self):
    """
    Test the parsing when attributes are missing, should get exceptions
    """
    config_file = os.path.abspath("./configs/siteattributes/siteattributes2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    mandatory = ['host_name',
                 'sponsor',
                 'site_policy',
                 'contact',
                 'email',
                 'city',
                 'country',
                 'longitude',
                 'latitude']
    for option in mandatory:
      config_file = os.path.abspath("./configs/siteattributes/siteattributes1.ini")
      configuration = ConfigParser.SafeConfigParser()
      configuration.read(config_file)
      configuration.remove_option('Site Information', option)

      settings = siteattributes.SiteAttributes(logger=global_logger)
      self.failUnlessRaises(exceptions.SettingError, 
                            settings.parseConfiguration, 
                            configuration)

  def testInvalidLatitude(self):
    """
    Test the checkAttributes with invalid latitude values
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_latitude1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid latitude ignored")
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_latitude2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid latitude ignored")
  
  def testInvalidLongitude(self):
    """
    Test the checkAttributes with invalid longitude values
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_longitude1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid latitude ignored")
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_longitude2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid latitude ignored")

  def testInvalidHostname(self):
    """
    Test the checkAttributes with invalid hostname
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_hostname.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid hostname ignored")
    
  def testInvalidEmail(self):
    """
    Test the checkAttributes with invalid email
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_email.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid email ignored")

  def testInvalidSponsor1(self):
    """
    Test the checkAttributes where the sponsor percentages 
    add up to more than 100
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_sponsor1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid email ignored")

  def testInvalidSponsor2(self):
    """
    Test the checkAttributes where the sponsor percentages 
    add up to less than 100
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_sponsor2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid email ignored")

  def testInvalidSponsor3(self):
    """
    Test the checkAttributes where the sponsor isn't on list 
    of allow VOs
    """
    
    
    config_file = os.path.abspath("./configs/siteattributes/" \
                                  "invalid_sponsor2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)
  
    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
    
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes),
                "Invalid email ignored")

  def testValidSettings(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/siteattributes/valid_settings.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as missing")

  def testValidSettings2(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/siteattributes/siteattributes3.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = siteattributes.SiteAttributes(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as missing")
if __name__ == '__main__':
    unittest.main()