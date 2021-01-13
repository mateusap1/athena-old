import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../src")

from Blockchain import Blockchain


blockchain = Blockchain()

def test_create_block():
    assert True

def test_always_fails():
    assert False