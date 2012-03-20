#! /usr/local/bin/python3

"""Unit test for astar algorithm. """

import subprocess 
import binascii
import unittest

APP='../main.py'
locfile = '../locations.txt'
confile = '../connections.txt'

class TestAStar(unittest.TestCase):

    def test_NoExclude1(self):
        expOut = ['G2', 'G2b', 'F2', 'D2', 'C2', 'C3', 'C4']
        self._checkSUT(expOut, 'G2', 'C4')

    def test_NoExclude2(self):
        expOut = ['A1', 'B1', 'B2', 'C3', 'C4', 'D4', 'E4', 'E5', 'F5', 'G5']
        self._checkSUT(expOut, 'A1', 'G5')

    def test_Exclude(self):
        expOut = ['A1', 'A2', 'A4', 'B5', 'C5', 'D5', 'F5', 'G5']
        self._checkSUT(expOut, 'A1', 'G5', 'B2')

    def _checkSUT(self, expOut, start, end, exclude=""):
        cmdArgs = ['python3', APP, locfile, confile, start, end, exclude]
        out = subprocess.getoutput(" ".join(cmdArgs))
        self.assertEqual(out.split("->"), expOut)

if __name__ == '__main__':
    unittest.main()


