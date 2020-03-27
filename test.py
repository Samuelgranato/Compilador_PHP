import unittest
import main

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
        self.assertRaises(Exception,main.Parser.run,source)

    # def test_error1(self):
        # source = '+1'
        # self.assertRaises(Exception,main.Parser.run,source)

    def test_error2(self):
        source = '1 1'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_error3(self):
        source = '+1+'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_error4(self):
        source = '1 1-3'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_error5(self):
        source = '1-30+'
        self.assertRaises(Exception,main.Parser.run,source)
    

    # def test_error6(self):
    #     source = '+1-30'
    #     self.assertRaises(Exception,main.Parser.run,source)
    

    def test_error7(self):
        source = '-1-30-'
        self.assertRaises(Exception,main.Parser.run,source)
    

    def test_error8(self):
        source = '1-3 0'
        self.assertRaises(Exception,main.Parser.run,source)
    

    # def test_error9(self):
    #     source = '1--30'
    #     self.assertRaises(Exception,main.Parser.run,source)

    def test_error10(self):
        source = '   1   -  3    0   '
        self.assertRaises(Exception,main.Parser.run,source)


    def test_error11(self):
        source = '   1   --  3    0   '
        self.assertRaises(Exception,main.Parser.run,source)

    def test_error12(self):
        source = '   1   --  3    0   '
        self.assertRaises(Exception,main.Parser.run,source)



    ##### MULT DIV
    def test_multdiv(self):
        source = '2*2'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv2(self):
        source = ' 2*2 '
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv3(self):
        source = ' 2 *2 '
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv4(self):
        source = '  2  *  2   '
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv5(self):
        source = '2*23 '
        expected = 46
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv6(self):
        source = '12*2 '
        expected = 24
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv7(self):
        source = '33*33 '
        expected = 1089
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv8(self):
        source = '1000*1000'
        expected = 1000000
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv9(self):
        source = '2/2 '
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv10(self):
        source = '2/2'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv11(self):
        source = '22/2 '
        expected = 11
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv12(self):
        source = '1+1 +  10 / 5     '
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv13(self):
        source = '8/3 ' #corta a parte decimal
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv14(self):
        source = '1 + 1 + 3/2 '
        expected = 3
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv15(self):
        source = '2000/5+1+2/2'
        expected = 402
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_multdiv_error(self):
        source = '3**2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error2(self):
        source = '3*2 2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error3(self):
        source = '3 3*2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error4(self):
        source = '3*2*'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error5(self):
        source = '*3*2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error6(self):
        source = '*3**2*'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error7(self):
        source = '*'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error8(self):
        source = '3//2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error10(self):
        source = '3/2 2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error11(self):
        source = '3 3/2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error12(self):
        source = '3/2/'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error13(self):
        source = '/3/2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error14(self):
        source = '/3//2/'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_multdiv_error15(self):
        source = '/'
        self.assertRaises(Exception,main.Parser.run,source)



    ## Comentarios
    def test_multdiv_comment(self):
        source = '1+1/*a2*/'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv_comment2(self):
        source = '/*a2*/1+1'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv_comment3(self):
        source = '/*a2  awdad    */        1+1'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv_comment4(self):
        source = '/*a2*/ /*a2*/ /*a2*/ /*a2*/ 1+1/*a2*//*a2*//*a2*/'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv_comment5(self):
        source = '/*a2*/1+1/*a2*/'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_multdiv_comment6(self):
        source = '/*a2*//*a2*/1/*a2*/*/*a2*/10/*a2*/'
        expected = 10
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))
    
    def test_multdiv_comment7(self):
        source = '/*a2*//*a2*/1/*a2*/+/*a2*/3/*a2*//*a2*//*a2*//*a2*//*a2*//*a2*//*a2*/'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))
    
    def test_multdiv_comment8(self):
        source = '/* /* /* /* 1+3 */ 3+2/2'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))


    def test_comment_error(self):
        source = '1+1/*a2'
        self.assertRaises(Exception,main.Parser.run,source)
    
    def test_comment_error2(self):
        source = '1 + 1 */ comentario invertido /*'
        self.assertRaises(Exception,main.Parser.run,source)
    
    def test_comment_error3(self):
        source = '/**/' #vazio
        self.assertRaises(Exception,main.Parser.run,source)
    
    def test_comment_error4(self):
        source = '/*1+1*/' #vazio
        self.assertRaises(Exception,main.Parser.run,source)

    def test_comment_error4(self):
        source = '/*1+1*/'
        self.assertRaises(Exception,main.Parser.run,source)


    def test_basetest_roteiro2_1(self):
        source = '/* a */ 1 /* b */'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_2(self):
        source = '3-2'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_3(self):
        source = '11+22-33 /* a */'
        expected = 0
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_4(self):
        source = '4/2+3'
        expected = 5
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_5(self):
        source = '3+4/2'
        expected = 5
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_6(self):
        source = '2 + 3 */* a */5'
        expected = 17
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro2_7(self):
        source = '3+ /* a */'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_basetest_roteiro2_8(self):
        source = '/*a*/'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_basetest_roteiro2_9(self):
        source = '3- 3 /* a'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_basetest_roteiro3_1(self):
        source = '(3 + 2) /5'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_2(self):
        source = '+--++3'
        expected = 3
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_3(self):
        source = '3 - -2/4'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_4(self):
        source = '4/(1+1)*2'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_5(self):
        source = '(2*2'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_basetest_roteiro3_6(self):
        source = '(10*(9*9))'
        expected = 810
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_7(self):
        source = '(((1+1)))'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_8(self):
        source = '(((1+1)))*2'
        expected = 4
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_9(self):
        source = '(((1+1))+3)'
        expected = 5
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_basetest_roteiro3_10(self):
        source = '(((1+1))'
        self.assertRaises(Exception,main.Parser.run,source)

    def test_basetest_roteiro3_11(self):
        source = '(((1+++1))+3)'
        expected = 5
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses1(self):
        source = '(1)'
        expected = 1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses2(self):
        source = '(-1)'
        expected = -1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses3(self):
        source = '(--++++-1)'
        expected = -1
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses4(self):
        source = '(2*(2*(2*(++++-1))))'
        expected = -8
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses5(self):
        source = '2*(1/*)*/)'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    def test_parentheses6(self):
        source = '2/(1)'
        expected = 2
        result = main.Parser.run(source)
        self.assertEqual(result, expected, "Should be {0}".format(expected))

    

if __name__ == '__main__':
    unittest.main()
