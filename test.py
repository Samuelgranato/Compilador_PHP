#by samuelvgb

import unittest
import main
from io import StringIO 
import sys
import os
test_fileName = 'testfile.temp'

def create_tempTestfile():
    f = open(test_fileName, "w")
    f.close()

def write_testFile(source):
    f = open(test_fileName, "w")
    f.write(source)
    f.close()

class TestSum(unittest.TestCase):
    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()
        sys.argv.append(test_fileName)
        create_tempTestfile()

    def tearDown(self):
        os.remove(test_fileName)

    def test_1(self):
        source = '''<?php{echo 1+2;}?>'''
        write_testFile(source)
        expected = '3\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_2(self):
        source = '''<?php{echo 3-2;}?>'''
        write_testFile(source)
        expected = '1\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_3(self):
        source = '''<?php{echo 11+22-33;}?>'''
        write_testFile(source)
        expected = '0\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_4(self):
        source = '''<?php{echo 789   +345  -    123;}?>'''
        write_testFile(source)
        expected = '1011\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_5(self):
        source = '''<?php{echo 1+1+1+1+1;}?>'''
        write_testFile(source)
        expected = '5\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_6(self):
        source = '''<?php{echo /* a */ 1 /* b */;}?>'''
        write_testFile(source)
        expected = '1\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_7(self):
        source = '''<?php{echo 3-2;}?>'''
        write_testFile(source)
        expected = '1\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_8(self):
        source = '''<?php{echo 11+22-33 /* a */;}?>'''
        write_testFile(source)
        expected = '0\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_9(self):
        source = '''<?php{echo 4/2+3;}?>'''
        write_testFile(source)
        expected = '5\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_10(self):
        source = '''<?php{echo 3+4/2;}?>'''
        write_testFile(source)
        expected = '5\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_11(self):
        source = '''<?php{echo 2 + 3 */* a */5;}?>'''
        write_testFile(source)
        expected = '17\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_12(self):
        source = '''<?php{ echo 3+ /* a */;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
    def test_13(self):
        source = '''<?php{echo /* a */;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()

    def test_14(self):
        source = '''<?php{echo 3- 3 /* a;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
  
    def test_15(self):
        source = '''<?php{echo 10  -  30;  }?>'''
        write_testFile(source)
        expected = '-20\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))  
    
    def test_16(self):
        source = '''<?php{echo 1;}?>'''
        write_testFile(source)
        expected = '1\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_17(self):
        source = '''<?php{echo +1}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main() 
    
    def test_18(self):
        source = '''<?php{echo 1 1;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    def test_19(self):
        source= '''<?php{echo +1+;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    def test_20(self):
        source= '''<?php{echo 1 1-3;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()   
    
    def test_21(self):
        source= '''<?php{echo 1-30+;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
    
    def test_22(self):
        source= '''<?php{echo +1-30-;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
    
    def test_23(self):
        source= '''<?php{echo -1-30-;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    def test_24(self):
        source= '''<?php{echo    1   --  3    0   ;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
  
    def test_25(self):
        source= '''<?php{echo   2  *  2   ;}?>'''
        write_testFile(source)
        expected = '4\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))  
    
    def test_26(self):
        source= '''<?php{echo 8/3; }?>''' #corta a parte decimal
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected)) 
    
    def test_27(self):
        source= '''<?php{echo *3**2*;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    def test_28(self):
        source= '''<?php{echo *;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    ## Comentarios
    def test_29(self):
        source= '''<?php{echo 1+1/*a2*/;}?>'''
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))   
    
    def test_30(self):
        source= '''<?php{echo /*a2*/1+1;}?>'''
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
     
    def test_31(self):
        source= '''<?php{echo /*a2*/ /*a2*/ /*a2*/ /*a2*/ 1+1/*a2*//*a2*//*a2*/;}?>'''
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))       
    
    def test_32(self):
        source= '''<?php{echo /*a2*//*a2*/1/*a2*/+/*a2*/3/*a2*//*a2*//*a2*//*a2*//*a2*//*a2*//*a2*/;}?>'''
        write_testFile(source)
        expected = '4\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    def test_33(self):
        source= '''<?php{echo 1+1/*a2;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
    
    def test_34(self):
        source= '''<?php{echo /**/''' #vazio
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()
    
    def test_35(self):
        source= '''<?php{echo +--++3;}?>'''
        write_testFile(source)
        expected = '3\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    
    def test_36(self):
        source= '''<?php{echo 3 - -2/4;}?>'''
        write_testFile(source)
        expected = '4\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    def test_37(self):
        source= '''<?php{echo (((1+1)))*2;}?>'''
        write_testFile(source)
        expected = '4\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    
    def test_38(self):
        source= '''<?php{echo (((1+1))+3);}?>'''
        write_testFile(source)
        expected = '5\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    def test_39(self):
        source= '''<?php{echo (((1+++1))+3);}?>'''
        write_testFile(source)
        expected = '5\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))
    
    def test_40(self):
        source= '''<?php{echo 2*(1/*)*/);}?>'''
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))    
    
    def test_41(self):
        source= '''<?php{echo 1+;}?>'''
        write_testFile(source)
        with self.assertRaises(Exception):
            main.main()  
    
    def test_42(self):
        source= '''<?php{echo (10*(9*9));}?>'''
        write_testFile(source)
        expected = '810\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))    
    
    def test_43(self):
        source= '''<?php{echo (((1+1)));}?>'''
        write_testFile(source)
        expected = '2\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))    
    
    def test_44(self):
        source= '''<?php{
$x1 = 3; /* bla bla $x1 = 9999998 */
$y2 = 4;
$z_final = $x1 + $y2 *33;
echo $z_final;
}?>'''
        write_testFile(source)
        expected = '135\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))    
    
    def test_45(self):
        source= '''<?php{
$x1 = 3;
$y2 = 4;
$z_final = ($x1 + $y2) *33;
echo $z_final;
}?>'''
        write_testFile(source)
        expected = '231\n'
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))    
    
    def test_46(self):
        source= '''<?php{
echo 1;
Echo 2;
ecHo 3;
ECHO 4;
}?>'''
        write_testFile(source)
        expected = '''1
2
3
4
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_47(self):
        source= '''<?php{
    $a = 5;
    $cnt = 0;

    while($a > $cnt){
        echo $cnt;
        $cnt = $cnt + 1;
    }
}?>'''
        write_testFile(source)
        expected = '''0
1
2
3
4
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_48(self):
        source= '''<?php{
echo 1;
Echo 2;
ecHo 3;
ECHO 4;
}?>'''
        write_testFile(source)
        expected = '''1
2
3
4
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_49(self):
        source= '''<?php{
echo 1;
Echo 2;
ecHo 3;
ECHO 4;
}?>'''
        write_testFile(source)
        expected = '''1
2
3
4
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

    def test_50(self):
        source= '''<?php{
echo 1;
Echo 2;
ecHo 3;
ECHO 4;
}?>'''
        write_testFile(source)
        expected = '''1
2
3
4
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))


    def test_51(self):
        source= '''<?php
{
$x1 = 3;
$x1 = $x1 +1;

echo $x1;

$y1 = $x1 *100;
echo $y1;
}?>'''
        write_testFile(source)
        expected = '''4
400
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))


    def test_52(self):
        source= '''<?php
    if (1 == 1){
        echo 1;
    }
?>'''
        write_testFile(source)
        expected = '''1
'''
        main.main()
        self.assertEqual(sys.stdout.getvalue(), expected, "Should be {0}".format(expected))

if __name__ == '__main__':
    unittest.main()