import json
import pyautogui as gui
import time
from datetime import datetime
from collections.abc import Iterable

class ProcessKeyError(Exception):
    pass

class ProcessIterError(Exception):
    pass


class Repeater(): 
    def __init__(self, nonLocalActions:dict, processSource:str, \
                 procName:str, sleepTime:int = 1):

        self._procName = procName
        self._procSource = processSource
        self._localFuncs = nonLocalActions
        self._localFuncs['run_process']  = self.runProcess
        self._localFuncs['write'] = self.writeWrapper
        self.sleepTime = sleepTime

        self._theProcess = ProcessIter(self._localFuncs, processSource,\
                                 self._procName)
        
        for instruction in self._theProcess:
            if isinstance(instruction, Iterable):
                func,*args = instruction
                self.runWithDelay(func, *args)
            else:
                print(f'{self._procName}:{instruction.__name__}')
                instruction()

        print(f'repeater done at {datetime.now().strftime("%H:%M:%S")}')
        time.sleep(1)

    def runWithDelay(self, func, *args):
        if func != self._localFuncs['wait']:
            time.sleep(self.sleepTime)
        func(*args)
        if func == self._localFuncs['wait']:
            time.sleep(self.sleepTime)

    def __str__(self):
        return str(self._theProcess)

    def writeWrapper(self,*args):
        to_write = ' '.join(*args)
        print(to_write)
        gui.write(to_write)

    def runProcess(self, process):
        print(f'running "{process}"')
        process = process[0]
        Repeater(self._localFuncs, self._procSource, process,\
                    sleepTime = self.sleepTime)


class ProcessIter:
    
    def __init__(self, functions, processDB, processName):
        self._process = None
        self._processName = processName
        self._functions = functions
        self.index = 0

        self.fileToProc(processDB, processName)
        
    def __str__(self):
        return str(self.process)

    @property
    def process(self):
        return self._process

    def fileToProc(self,file_name, proc_name):
        with open(file_name,'r') as f:
            process_dict = json.load(f)
            print(proc_name)
            try:
                self._process = process_dict['public'][proc_name]
            except(KeyError):
                print(f'{proc_name} is not a valid public process')
                return
        
    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self._process):
            raise StopIteration
        next_instruction = self._process[self.index]
        self.index += 1
        func_name, *args = next_instruction
        func = self._functions[func_name]
        if args in (None,[],()):
            return func
        return (func,*args)
    

class ListRepeater(Repeater):
    def __init__(
                self, nonLocalActions,
                ProcessList, sleepTime = 1):
        super().__init__()
        


#repeater tests
if __name__ == "__main__":
    import os
    import sys

    currentDir = os.getcwd()
    parentDir = os.path.dirname(currentDir)
    sys.path.append(parentDir)

    import helpers
    commands = {el.keyword:el.run_process for el in helpers.tracker_commands.values()}
    
    test = Repeater(commands,\
                    os.path.join(currentDir, 'test','test_processes.json'),\
                     'test')
    print(test)
