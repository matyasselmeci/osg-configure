#!/usr/bin/env python

import os, imp, sys, unittest, ConfigParser, types

# setup system library path if it's not there at present
try:
  from osg_configure.modules import exceptions
except ImportError:
  pathname = '../'
  sys.path.append(pathname)
  from osg_configure.modules import exceptions


pathname = os.path.join('../scripts', 'configure-osg')

try:
    has_configure_osg = False
    fp = open(pathname, 'r')
    configure_osg = imp.load_module('test_module', fp, pathname, ('', '', 1))
    has_configure_osg = True
except:
    raise

from osg_configure.modules import exceptions
from osg_configure.modules import utilities

class TestUtilities(unittest.TestCase):

    def test_get_gums_host(self):
      """
      Check the functionality of get_gums_host
      """
      
      failed = False
      message = None
      gums_host = 'gums-host.test.com'

      os.environ['VDT_GUMS_HOST'] = gums_host
      self.failUnlessEqual(utilities.get_gums_host(), 
                           (gums_host, 8443), 
                           "Gums host not found from environment")
      del os.environ['VDT_GUMS_HOST']
        

    def test_write_attribute_file(self):
      """
      Check to make sure that write_attribute_file writes out files properly
      """
      attribute_file = os.path.abspath("./test_files/temp_attributes.conf")
      attribute_standard = os.path.abspath("./test_files/attributes_output.conf")
      try:
        attributes = {'Foo' : 123,
                      'test_attr' : 'abc-234#$',
                      'my-Attribute' : 'test_attribute'}
        utilities.write_attribute_file(attribute_file, attributes)
        self.failUnlessEqual(open(attribute_file).read(), 
                             open(attribute_standard).read(), 
                             'Attribute files are not equal')
        if os.path.exists(attribute_file):
          os.unlink(attribute_file)
      except Exception, ex:
        print ex
        self.fail('Got exception while testing wite_attribute_file' \
                  "functionality:\n%s" % ex)
        if os.path.exists(attribute_file):
          os.unlink(attribute_file)
      
    def test_get_set_membership(self):
      """
      Test get_set_membership functionality
      """
      
      test_set1 = [1, 2, 3, 4, 5, 6, 7]
      reference_set1 = [1, 2, 3, 4, 5]
      default_set1 = [5, 6, 7]
      
      self.failUnlessEqual(utilities.get_set_membership(test_set1, 
                                                        reference_set1), 
                            [6, 7],
                            'Did not get [6, 7] as missing set members')

      self.failUnlessEqual(utilities.get_set_membership(test_set1, 
                                                        reference_set1,
                                                        default_set1), 
                            [],
                            'Did not get [] as missing set members')

      self.failUnlessEqual(utilities.get_set_membership(reference_set1, 
                                                        reference_set1), 
                            [],
                            'Did not get [] as missing set members')

      test_set2 = ['a', 'b', 'c', 'd', 'e']
      reference_set2 = ['a', 'b', 'c']
      default_set2 = ['d', 'e']
      self.failUnlessEqual(utilities.get_set_membership(test_set2, 
                                                        reference_set2), 
                            ['d', 'e'],
                            'Did not get [d, e] as missing set members')

      self.failUnlessEqual(utilities.get_set_membership(test_set2, 
                                                        reference_set2,
                                                        default_set2), 
                            [],
                            'Did not get [] as missing set members')

      self.failUnlessEqual(utilities.get_set_membership(reference_set2, 
                                                        reference_set2), 
                            [],
                            'Did not get [] as missing set members')

    def test_blank(self):
      """
      Test functionality of blank function
      """
      
      self.failIf(utilities.blank(1), 
                  'blank indicated 1 was a blank value')
      self.failIf(utilities.blank('a'), 
                  'blank indicated a was a blank value')
      self.failUnless(utilities.blank('unavailable'), 
                      'blank did not indicate unavailable was a blank value')
      self.failUnless(utilities.blank(None), 
                      'blank did not indicate None was a blank value')
      self.failUnless(utilities.blank('unavAilablE'), 
                      'blank did not indicate unavAilablE was a blank value')

    def test_get_vos(self):
      """
      Test get_vos function
      """  
      
      vo_file = os.path.abspath('./test_files/sample-vos.txt')
      self.failUnlessEqual(utilities.get_vos(vo_file), 
                           ['osg', 'LIGO', 'cdf'], 
                           "Correct vos not found")
      


if __name__ == '__main__':
    unittest.main()

