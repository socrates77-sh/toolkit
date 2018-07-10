import unittest

from chk_bus import *


class TestFunc(unittest.TestCase):

    def test_match_start(self):
        valid_case = [
            '    123456: .SUBCKT a670 iop0[7]',
            '        22: .SUBCKT a670 iop0[7]',
            '1323123456: .SUBCKT  a670  iop0[7]',
            '    123456:  .SUBCKT a670 iop0[6] ',
            '    123456:   .SUBCKT a670 iop0[6] '
        ]
        illegal_case = [
            '    123456:.SUBCKT a670 iop0[7]',
            '    123456:SUBCKT a670 iop0[7]',
            '    123456:.SUBCKT a671 iop0[7]',
            '    123456:.subckt a670 iop0[6] ',
            '    123456:.SUBCKTX a670 iop0[6] ',
            '   123456: .SUBCKT a670 iop0[7]',
            'SUBCKT a670 iop0[7]',
            '.SUBCKT a671 iop0[7]',
            '.subckt a670 iop0[6] ',
            '.SUBCKTX a670 iop0[6] '
        ]

        for case in valid_case:
            self.assertTrue(match_start(case, 'a670'), case)

        for case in illegal_case:
            self.assertFalse(match_start(case, 'a670'), case)

    def test_match_end(self):
        valid_case = [
            '    123456: .ENDS',
            '    123456:  .ENDS',
            '    123456: .ENDS '
        ]
        illegal_case = [
            '    123456:.ENDS',
            '    12345: .ENDS',
            '    123456: .ends',
            '    123456: .END',
            '    123456: .ENDS a'
            '.ends',
            '.END',
            '.ENDS a'
        ]

        for case in valid_case:
            self.assertTrue(match_end(case), case)

        for case in illegal_case:
            self.assertFalse(match_end(case), case)


if __name__ == '__main__':
    unittest.main()
