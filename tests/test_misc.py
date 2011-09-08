#!/usr/bin/env python

import os, imp, sys, unittest, ConfigParser, logging

# setup system library path if it's not there at present
try:
  from osg_configure.modules import utilities
except ImportError:
  pathname = '../'
  sys.path.append(pathname)
  from osg_configure.modules import utilities

from osg_configure.modules import exceptions


from osg_configure.configure_modules import misc

global_logger = logging.getLogger('test misc configuration')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
global_logger.addHandler(console)

class TestLocalSettings(unittest.TestCase):
  """
  Unit test class to test MiscConfiguration class
  """

  def testParsing1(self):
    """
    Test misc parsing
    """
    
    config_file = os.path.abspath("./configs/misc/misc1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'OSG_GLEXEC_LOCATION' : './configs/misc',
                 'OSG_CERT_UPDATER' : 'Y',
                 'enable_webpage_creation' : 'Y',
                 'gums_host' : 'my.gums.org',
                 'authorization_method' : 'prima'}
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
    Test misc parsing with negative values
    """
    
    config_file = os.path.abspath("./configs/misc/misc2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'OSG_GLEXEC_LOCATION' : './configs/misc',
                 'OSG_CERT_UPDATER' : 'N',
                 'enable_webpage_creation' : 'N',
                 'gums_host' : 'my.gums.org',
                 'authorization_method' : 'prima'}
    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var,                                             
                                            attributes[var],
                                            variables[var]))
    

  def testParsingAuthentication(self):
    """
    Test misc parsing with negative values
    """
    
    config_file = os.path.abspath("./configs/misc/misc_prima.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnless(attributes.has_key('authorization_method'), 
                    "Attribute authorization_method missing")
    self.failUnlessEqual(attributes['authorization_method'], 
                         'prima', 
                         "Wrong value obtained for %s, got %s but " \
                         "expected %s" % ('authorization_method',                                             
                                          attributes['authorization_method'],
                                          'prima'))

    config_file = os.path.abspath("./configs/misc/misc_xacml.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnless(attributes.has_key('authorization_method'), 
                    "Attribute authorization_method missing")
    self.failUnlessEqual(attributes['authorization_method'], 
                         'xacml', 
                         "Wrong value obtained for %s, got %s but " \
                         "expected %s" % ('authorization_method',                                             
                                          attributes['authorization_method'],
                                          'xacml'))

    config_file = os.path.abspath("./configs/misc/misc_gridmap.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnless(attributes.has_key('authorization_method'), 
                    "Attribute authorization_method missing")
    self.failUnlessEqual(attributes['authorization_method'], 
                         'gridmap', 
                         "Wrong value obtained for %s, got %s but " \
                         "expected %s" % ('authorization_method',                                             
                                          attributes['authorization_method'],
                                          'gridmap'))

    config_file = os.path.abspath("./configs/misc/misc_local_gridmap.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnless(attributes.has_key('authorization_method'), 
                    "Attribute authorization_method missing")
    self.failUnlessEqual(attributes['authorization_method'], 
                         'local-gridmap', 
                         "Wrong value obtained for %s, got %s but " \
                         "expected %s" % ('authorization_method',                                             
                                          attributes['authorization_method'],
                                          'local-gridmap'))

  def testMissingAttribute(self):
    """
    Test the parsing when attributes are missing, should get exceptions
    """
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    mandatory = ['gums_host',
                 'authorization_method']
    for option in mandatory:
      config_file = os.path.abspath("./configs/misc/misc1.ini")
      configuration = ConfigParser.SafeConfigParser()
      configuration.read(config_file)
      configuration.remove_option('Misc Services', option)

      settings = misc.MiscConfiguration(logger=global_logger)
      self.failUnlessRaises(exceptions.SettingError, 
                            settings.parseConfiguration, 
                            configuration)

  def testPrimaMissingGums(self):
    """
    Test the checkAttributes function when prima is specified but the
    gums host isn't given
    """
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/misc_prima_missing_gums.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      print "a"
      print e
      print "b"
      self.fail("Received exception while parsing configuration")

    attributes = settings.attributes
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice missing gums host")

  def testXacmlMissingGums(self):
    """
    Test the checkAttributes function when xacml is specified but the
    gums host isn't 
    """
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/misc_xacml_missing_gums.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration")

    attributes = settings.attributes
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice missing gums host")
    
  def testXacmlBadGums(self):
    """
    Test the checkAttributes function when xacml is specified but the
    gums host isn't valid
    """
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/misc_xacml_bad_gums.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.attributes
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice bad gums host")

  def testPrimaBadGums(self):
    """
    Test the checkAttributes function when prima is specified but the
    gums host isn't valid
    """
        

    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/misc_prima_bad_gums.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    attributes = settings.attributes
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice bad gums host")

  def testValidSettings(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/valid_settings.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
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
    config_file = os.path.abspath("./configs/misc/valid_settings2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as invalid")

  def testInvalidSettings(self):
    """
    Test the checkAttributes function to see if it flags bad attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/misc/invalid_settings1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = misc.MiscConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Bad config incorrectly flagged as okay")    
if __name__ == '__main__':
    unittest.main()
