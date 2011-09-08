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


from osg_configure.configure_modules import managedfork

global_logger = logging.getLogger('test managedfork configuration')
console = logging.StreamHandler()
console.setLevel(logging.ERROR)
global_logger.addHandler(console)

class TestManagedFork(unittest.TestCase):
  """
  Unit test class to test ManagedForkConfiguration class
  """

  def testParsing1(self):
    """
    Test managedfork parsing
    """
    
    config_file = os.path.abspath("./configs/managedfork/managedfork1.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_MANAGEDFORK'), 
                    'Attribute OSG_MANAGEDFORK missing')
    self.failUnlessEqual(attributes['OSG_MANAGEDFORK'], 'Y', 
                         'Wrong value obtained for OSG_MANAGEDFORK')
    


  def testParsingDisabled(self):
    """
    Test managedfork parsing when disabled
    """
    
    config_file = os.path.abspath("./configs/managedfork/managedfork_disabled.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_MANAGEDFORK'), 
                    'Attribute OSG_MANAGEDFORK missing')
    self.failUnlessEqual(attributes['OSG_MANAGEDFORK'], 'N', 
                         'Wrong value obtained for OSG_MANAGEDFORK')
    
  def testParsingIgnored(self):
    """
    Test managedfork parsing when ignored
    """
    
    config_file = os.path.abspath("./configs/managedfork/ignored.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    os.environ['VDT_LOCATION'] = '/opt/osg'
    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 

    attributes = settings.getAttributes()
    self.failUnless(attributes.has_key('OSG_MANAGEDFORK'), 
                    'Attribute OSG_MANAGEDFORK missing')
    self.failUnlessEqual(attributes['OSG_MANAGEDFORK'], 'N', 
                         'Wrong value obtained for OSG_MANAGEDFORK')
                                                        
  def testValidSettings(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/managedfork/check_ok.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as missing")


  def testAcceptLimitedTrue(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/managedfork/check_accept_limited_true.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as missing")


  def testAcceptLimitedFalse(self):
    """
    Test the checkAttributes function to see if it oks good attributes
    """
        
    os.environ['VDT_LOCATION'] = os.getcwd()
    config_file = os.path.abspath("./configs/managedfork/check_accept_limited_false.ini")
    configuration = ConfigParser.SafeConfigParser()
    configuration.read(config_file)

    settings = managedfork.ManagedForkConfiguration(logger=global_logger)
    try:
      settings.parseConfiguration(configuration)
    except Exception, e:
      self.fail("Received exception while parsing configuration: %s" % e)
 
    attributes = settings.getAttributes()
    self.failUnless(settings.checkAttributes(attributes), 
                    "Correct locations incorrectly flagged as missing")

    
    
if __name__ == '__main__':
    unittest.main()
