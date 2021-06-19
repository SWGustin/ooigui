import pyautogui as gui
from time import sleep
import json
import re

gui.PAUSE = 2
gui.FAILSAFE = True

class Tracker():

    def __init__(self, commands:dict, procFile:str = None)->None:
        self._procFile = procFile
        self._commands = commands
        self._actions = []
        self._procName = None
        self._private = False
        self._dfltProcName = 'defaultOuterProcess'
        self.nestedLayer = 0

    def getScriptInfo(self, script:str, prvtOrPub:bool)->None:
        #gets info about the script
        print('you can click now')
        if self._procName == None:
            self._procName= input("the script we're building is...")
        print(f"building '{self._procName}'", end = '')
        if prvtOrPub == 'private':
            self._private = True
            print(' (private)')
        else:
            print()
            self._private = False

    def displayCommands(self)->None:
        #displays the possible commands
        print('\t-------------commands-------------')
        for val in self._commands.values():
            print(f'\t{val.keyword}:\t{val.description}')
        print('\tq:\tFinish tracking')
        print('\t--del:\tRemove last command')
        print('\t[] xn:\tRepeat [] n times')
        print('\tpass:\tto skip making an inner proc and reuse the last')
        print('\tOR:\ttype a message to create input')
        print('\t----------------------------------')

    def breakupInput(self, val:str) -> tuple:
        #break down input
        rep = 1
        val_list = val.strip().split()
        if val_list and re.match(r'x\d+', val_list[-1]):
            rep = int(val_list[-1][1:])
            val_list = val_list[:-1]
        args = None
        try:
            key = val_list[0]
            try:
                args = val_list[1:]
            except(IndexError):
                pass
        except(IndexError):
            key = ''
        return rep, key, args

    def parseInput(self, key:str, *args:list)-> None:
        if key == 'r':
            args = [self._procName.split('-')[0]+f'-{self.nestedLayer+1}']
        if key not in self._commands.keys():
            args =  [key]+list(*args)
            key = None
        #get the storing function
        func = self._commands[key].store_process
        #create the stuff to be stored
        
        try:
            outFunc, *outArgs = func(*args)
        except TypeError:
            outFunc = func(*args)
            outArgs = []
        return outFunc, outArgs


    @staticmethod
    def stopInput(key):
        return key == 'q'
    
    def removeDefaults(self)->None:
        #removes any process in the default group
        with open(self._procFile, 'r') as procfile:
            flen = len(procfile.readline())
            procfile.seek(0)
            if flen > 0: 
                processes = json.load(procfile)

        try:
            processes.pop(self._dfltProcName)
        except KeyError:
            pass
        cntr = 0
        while True:
            try:
                processes.pop(self._dfltProcName+f'{-cntr}')
                cntr+=1
            except KeyError:
                break

    def storeProc(self)->None:
        #store the process in the db
        
        processes = dict()
        with open(self._procFile, 'r') as procfile:
            flen = len(procfile.readline())
            procfile.seek(0)
            if flen > 0: 
                processes = json.load(procfile)
        i = 0
        
        if self._private:
            prvtOrPub = 'private'
        else:
            prvtOrPub = 'public'
        
        #if the proc already exists append a num to it's name            
        while self._procName in processes[prvtOrPub].keys() and \
            self._procName[:len(self._dfltProcName)] != self._dfltProcName:
                i+=1
                self._procName = self._procName.split('(')[0]+f'({i})'
                
        #update processes dict
        processes[prvtOrPub][self._procName] = self._actions

        #write out processes dict
        with open(self._procFile,'w') as pfile:
            json.dump(processes, pfile)

    def delPrev(self):
        try:
            removed = self._actions.pop()
            print(f'deleted command: {removed}')
        except IndexError:
            pass

    def recursiveTrack(self, prvtOrPub):
        if self.nestedLayer == 0:
            innerName = self._procName
        else:
            innerName = self._procName.split('-')[0]
        innerName = innerName + f'-{self.nestedLayer+1}'
        tempTrack = Tracker(self._commands, self._procFile)
        tempTrack.nestedLayer = self.nestedLayer + 1
        tempTrack.start(innerName, prvtOrPub)

    def start(self, script:str = None, prvtOrPub:str = 'public')->None:
        #this handles the flow of tracking
        repeate = False
        stop = False

        if script:
            self._procName = script

        self.getScriptInfo(script, prvtOrPub)
        self.displayCommands()

        val = input()
        while not stop and val != 'q':
            rep = 1
            if val == '--del':
                self.delPrev()
            else:
                rep, key, *args = self.breakupInput(val)
                if key == 'pass':
                    return
                func, func_args = self.parseInput(key, *args)
                #store it
                for _ in range(rep):
                    self._actions.append([func, func_args])
                print(f"{func}({func_args})")
                if key == 'r':
                    repeate = True
            val = input()
            stop = self.stopInput(val)
          
        if self._procName != '':
            #cleanup default procs if this is a new one
            if self._procName == self._dfltProcName:
                self.removeDefaults()
                
            if repeate:
                self.recursiveTrack(prvtOrPub)
            self.storeProc()
                
        else:
            print('process not stored')
            print(self._actions)

class PrivateTracker(Tracker):
    def __init__(self, commands, procFile):
        super().__init__(commands, procFile)

    def start(self, script_name = None):
        super().start(script_name, 'private')


if __name__ == "__main__":
    import os
    import sys

    currentDir = os.getcwd()
    parentDir = os.path.dirname(currentDir)
    sys.path.append(parentDir)

    import helpers
    commands = {el.keyword:el.run_process for el in helpers.tracker_commands.values()}

    test = Tracker(commands, os.path.join(currentDir, 'test','test_processes.json'))

    instructions = []
    with open(os.path.join(currentDir,'test','test_from.json'), 'r') as file:
        instructions = json.load(file)
    for instruction in instructions:
        gui.write(instruction)
        gui.press('enter')

    #assert tests
