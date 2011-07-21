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

from configure_osg.configure_modules import cemon

global_logger = logging.getLogger('test cemon configuration')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
global_logger.addHandler(console)

class TestLocalSettings(unittest.TestCase):
  """
  Unit test class to test CemonConfiguration class
  """

  def testParsing1(self):
    """
    Test cemon parsing
    """
    
    config_file = os.path.abspath("./configs/cemon/cemon.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'ress_servers' : 'https://osg-ress-1.fnal.gov:8443/ig/services/CEInfoCollector[OLD_CLASSAD]',
                 'bdii_servers' : 'http://is1.grid.iu.edu:14001[RAW], http://is2.grid.iu.edu:14001[RAW]' }

    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))
    
  def testParsingITBDefaults(self):
    """
    Test cemon parsing to make sure it picks up ITB defaults
    """
    
    config_file = os.path.abspath("./configs/cemon/itb_defaults.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'ress_servers' : 'https://osg-ress-4.fnal.gov:8443/ig/' \
                                  'services/CEInfoCollector[OLD_CLASSAD]',
                 'bdii_servers' : 'http://is-itb1.grid.iu.edu:14001[RAW],'\
                                  'http://is-itb2.grid.iu.edu:14001[RAW]'}

    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))

  def testParsingProductionDefaults(self):
    """
    Test cemon parsing to make sure it picks up production defaults
    """
    
    config_file = os.path.abspath("./configs/cemon/prod_defaults.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'ress_servers' : 'https://osg-ress-1.fnal.gov:8443/ig/' \
                                  'services/CEInfoCollector[OLD_CLASSAD]',
                 'bdii_servers' : 'http://is1.grid.iu.edu:14001[RAW],' \
                                  'http://is2.grid.iu.edu:14001[RAW]'}

    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))

  def testParsingMissingITBDefaults(self):
    """
    Test cemon parsing to make sure it picks up ITB defaults 
    when the cemon section is missing
    """
    
    config_file = os.path.abspath("./configs/cemon/itb_defaults2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'ress_servers' : 'https://osg-ress-4.fnal.gov:8443/ig/' \
                                  'services/CEInfoCollector[OLD_CLASSAD]',
                 'bdii_servers' : 'http://is-itb1.grid.iu.edu:14001[RAW],'\
                                  'http://is-itb2.grid.iu.edu:14001[RAW]'}

    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))

  def testParsingMissingProductionDefaults(self):
    """
    Test cemon parsing to make sure it picks up production defaults 
    when the cemon section is missing
    """
    
    config_file = os.path.abspath("./configs/cemon/prod_defaults2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    variables = {'ress_servers' : 'https://osg-ress-1.fnal.gov:8443/ig/' \
                                  'services/CEInfoCollector[OLD_CLASSAD]',
                 'bdii_servers' : 'http://is1.grid.iu.edu:14001[RAW],' \
                                  'http://is2.grid.iu.edu:14001[RAW]'}

    for var in variables:      
      self.failUnless(attributes.has_key(var), 
                      "Attribute %s missing" % var)
      self.failUnlessEqual(attributes[var], 
                           variables[var], 
                           "Wrong value obtained for %s, got %s but " \
                           "expected %s" % (var, 
                                            attributes[var], 
                                            variables[var]))

  def testParsingDisabled(self):
    """
    Test cemon parsing when set to disabled
    """
    
    config_file = os.path.abspath("./configs/cemon/disabled.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnlessEqual(len(attributes), 0, 
                         "Disabled configuration should have no attributes")

  def testParsingIgnored(self):
    """
    Test cemon parsing when set to ignored
    """
    
    config_file = os.path.abspath("./configs/cemon/ignored.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.attributes
    self.failUnlessEqual(len(attributes), 0, 
                         "Disabled configuration should have no attributes")

  def testIgnoredServices(self):
    """
    Test cemon parsing when ignoring just bdii or ress
    """
    
    config_file = os.path.abspath("./configs/cemon/ignore_ress.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    self.failUnlessEqual(settings.ress_servers, {}, 
                         "Should not have ress subscriptions when being ignored")

    config_file = os.path.abspath("./configs/cemon/ignore_bdii.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)

    self.failUnlessEqual(settings.bdii_servers, {}, 
                         "Should not have BDII subscriptions when being ignored")

  def testInvalidRess1(self):
    """
    Test the checkAttributes function to see if it catches invalid
    ress servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_ress1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    self.failUnlessRaises(exceptions.SettingError, 
                          settings.parseConfiguration,
                          configuration = configuration)

  def testInvalidRess2(self):
    """
    Test the checkAttributes function to see if it catches invalid
    ress servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_ress2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid ress server")

  def testInvalidRess3(self):
    """
    Test the checkAttributes function to see if it catches invalid
    ress servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_ress3.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid ress server")

  def testInvalidBDII1(self):
    """
    Test the checkAttributes function to see if it catches invalid
    bdii servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_bdii1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    self.failUnlessRaises(exceptions.SettingError, 
                          settings.parseConfiguration,
                          configuration = configuration)

  def testInvalidBDII2(self):
    """
    Test the checkAttributes function to see if it catches invalid
    bdii servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_bdii2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid bdii server")

  def testInvalidBDII3(self):
    """
    Test the checkAttributes function to see if it catches invalid
    bdii servers
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()

    config_file = os.path.abspath("./configs/cemon/invalid_bdii3.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failIf(settings.checkAttributes(attributes), 
                "Did not notice invalid bdii server")

  def testValidSettings(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/check_ok.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct settings incorrectly flagged as invalid")
    
  def testValidSettings2(self):
    """
    Test the checkAttributes function to see if it oks a disabled section
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/disabled.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Disabled section incorrectly flagged as invalid")


  def testValidITBDefaults(self):
    """
    Test the checkAttributes function to see if it oks the itb defaults
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/itb_defaults.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "ITB defaults incorrectly flagged as invalid")

  def testValidProductionDefaults(self):
    """
    Test the checkAttributes function to see if it oks the production defaults
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/prod_defaults.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "production defaults incorrectly flagged as invalid")

  def testMissingCEITBDefaults(self):
    """
    Test the checkAttributes function to see if it oks the itb defaults
    set when the cemon section is missing
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/itb_defaults2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "ITB defaults incorrectly flagged as invalid")

  def testMissingProductionDefaults(self):
    """
    Test the checkAttributes function to see if it oks the production defaults
    set when the cemon section is missing
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/prod_defaults2.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "production defaults incorrectly flagged as invalid")

  def testMultipleRessServers(self):
    """
    Test the checkAttributes function to see if it oks the production defaults
    set when the cemon section is missing
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/multiple_ress.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    self.failUnless(len(settings.ress_servers) == 3, 
                    "Did not parse ress servers correctly")

  def testMultipleBDIIServers(self):
    """
    Test the checkAttributes function to see if it oks the production defaults
    set when the cemon section is missing
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/cemon/multiple_bdii.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = cemon.CemonConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    self.failUnless(len(settings.bdii_servers) == 3, 
                    "Did not parse bdii servers correctly")
if __name__ == '__main__':
    unittest.main()