import pytest
import os
import sys

currentDir = os.getcwd()
parentDir = os.path.dirname(currentDir)
sys.path.append(parentDir)

from funcs import *

#run this in cmd
#cd C:\Users\GustinSa\"OneDrive - Government of Ontario"\Documents\SQRS\script\test
#python -m pytest --html=report.html -s

class TestHelpers():
    def test_isrunning_python(self):
        test_prog = Program(
                'test','python.exe',
                (-1,-1), 'testhost',
                'https://www.testwebsite.ca/api/test#42')
                            
        assert isrunning(test_prog)

    def test_isrunning_blah(self):
        test_prog = Program(
                'test','blah.exe',
                (-1,-1), 'testhost',
                'https://www.testwebsite.ca/api/test#42')
        assert not isrunning(test_prog)

    def test_getPageNo_fortytwo(self):
        assert getPageNo('https://www.testwebsite.ca/api/test#42') == 42

    def test_getPageNo_bad_page(self):
        assert getPageNo('https://www.testwebsite.com/api/test') == 0

    def test_pagehasloaded_0_1(self):
        assert pagehasloaded( 0,'https://www.testwebsite.ca/api/test#1')

    def test_pagehasloaded_0_42(self):
        assert pagehasloaded( 0,'https://www.testwebsite.ca/api/test#42')

    def test_pagehasloaded_0_0(self):
        assert not pagehasloaded(0,'https#0')

    def test_checkifopen_pass(self):
        test_prog = Program(
                'otd','python.exe',
                (-1,-1), 'testhost',
                'https://www.testwebsite.ca/api/test#42')
        assert checkifopen(test_prog,False)

    def test_checkifOpen_OTP(self):        
        test_prog = Program(
                'otp','python.exe',
                (-1,-1), 'testhost',
                'https://www.testwebsite.ca/api/test#42')
        assert not checkifopen(test_prog,False)

    def test_checkifOpen_badEnv(self):
        def getUrl(safe:bool = False)->str:
            return 'https://www.testwebsite.ca/api/test#42'
        
        test_prog = Program(
                'blarg','python.exe',
                (-1,-1), 'testhost',
                'https://www.testwebsite.ca/api/test#42')
        with pytest.raises(EnvError):
            checkifopen(test_prog,False)

    def test_checkifFileOpen_not_open(self):
        assert not checkifFileOpen(HELPFILE)

    def test_checkifFileOpen_open(self):
        with open(HELPFILE, '') as file:
            assert checkifFileOpen(HELPFILE)
    
    

class TestFuncs():
    def test_getHelp(self):
        assert not gethelp()

    def test_getHelpFuncs(self):
        assert not gethelpFuncs()
    


class TestMenu:
    COMMANDS = {'comm1': lambda: print('comm1 ran'),
                'comm2': lambda: print('comm2 ran')
                }
  
    def test_process_commands(self):
        pass

    def test_close_prog(self):
        pass

class TestReport():
    def test_(self):
        pass

class TestTracker():
    def test_(self):
        pass

class TestRepeater():
    def test_(self):
        pass


if __name__ == "__main__":
    print(PROGS.keys())
