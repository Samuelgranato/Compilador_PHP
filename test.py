import unittest
import main

# import urllib.request
# a = urllib.request.urlopen(url)
# eval(a.read())

class TestSum(unittest.TestCase):

    def test_sum(self):
        source = '14+1'
        expected = 15
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum2(self):
        source = '1+120'
        expected = 121
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum3(self):
        source = '1+1'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum4(self):
        source = '99999+1'
        expected = 100000
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum5(self):
        source = '99999+10'
        expected = 100009
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum6(self):
        source = '1-3'
        expected = -2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))
        
    def test_sum7(self):
        source = '1-30          '
        expected = -29
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum8(self):
        source = '10- 30'
        expected = -20
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum9(self):
        source = ' 10- 30'
        expected = -20
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))
    
    def test_sum10(self):
        source = ' 10  -  30  '
        expected = -20
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum10(self):
        source = ' 10  -30  '
        expected = -20
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_sum11(self):
        source = '1'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_error(self):
        source = '1+'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error1(self):
        source = '+1'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error2(self):
        source = '1 1'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error3(self):
        source = '+1+'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error4(self):
        source = '1 1-3'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error5(self):
        source = '1-30+'
        self.assertRaises(TypeError,main.Parser.run,source)
    

    def test_error6(self):
        source = '+1-30'
        self.assertRaises(TypeError,main.Parser.run,source)
    

    def test_error7(self):
        source = '-1-30-'
        self.assertRaises(TypeError,main.Parser.run,source)
    

    def test_error8(self):
        source = '1-3 0'
        self.assertRaises(TypeError,main.Parser.run,source)
    

    def test_error9(self):
        source = '1--30'
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error10(self):
        source = '   1   -  3    0   '
        self.assertRaises(TypeError,main.Parser.run,source)


    def test_error11(self):
        source = '   1   --  3    0   '
        self.assertRaises(TypeError,main.Parser.run,source)

    def test_error12(self):
        source = '   1   --  3    0   '
        self.assertRaises(TypeError,main.Parser.run,source)
    


if __name__ == '__main__':
    unittest.main()
