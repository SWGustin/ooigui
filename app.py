import tkinter as tk
from tkinter import messagebox, font, ttk
import sqlite3
import json
import menu
from constants import *
import re

class Display():
    def __init__(self):
        self.root = tk.Tk()
        #self.root.geometry('500x400')
        self.root.configure(bg = '#121212')
        #use this to modify font globaly
        default_font = font.nametofont("TkDefaultFont")
        self.dropdowndefault = 'None'
    #variables
        self.toOpen_GENTAX = tk.StringVar(value = self.dropdowndefault)
        self.toOpen_SQL = tk.StringVar(value = self.dropdowndefault)
        self.envs = ['OTD', 'OT2', 'OTT','OS2','OTS']
        self.procToRun = tk.StringVar(value = self.dropdowndefault)
        self.userProcs = []

        self.jiggler = tk.IntVar()
        self.jigglerSchedule = tk.IntVar()
        self.verbose = tk.IntVar()
        self.toScreen = tk.IntVar()

    #jigFrame
        jigFrame = tk.LabelFrame(
                        self.root, text = 'jiggler controls',
                        padx = 5, pady = 5)
        
        jigFrame.configure(width = 40, height = 40)
    #                    background = '#555555', fg = 'white')

        cbjiggler = tk.Checkbutton(
                        jigFrame, text = 'jiggler', variable = self.jiggler,
                        command = self.runJiggler, anchor = tk.W)
        cbjiggler.deselect()
        
        self.cbjigsched = tk.Checkbutton(
                        jigFrame, text = 'run on schedule',
                        variable = self.jigglerSchedule, anchor = tk.W)
        self.cbjigsched.deselect()
        self.cbjigsched.pack(side = tk.BOTTOM, anchor = tk.W)
        cbjiggler.pack(side = tk.BOTTOM, anchor = tk.W)
        

    #open self.envs

        openEnvFrame = tk.LabelFrame(
                        self.root, text = 'open Gentax Env',
                        padx = 5, pady = 5)
        btnOpener = tk.Button(
                    openEnvFrame, text = 'run...', command = self.openGentax)

        openOptions = tk.OptionMenu(openEnvFrame, self.toOpen_GENTAX, *self.envs,'links')
        openOptions.configure(width = 10)

        openOptions.grid(row = 0, column = 0)
        btnOpener.grid(row = 1, column = 0)

    #open self.envs
        openSqlFrame = tk.LabelFrame(
                        self.root, text = 'open SQL Env',
                        padx = 5, pady = 5)
        btnOpener = tk.Button(
                    openSqlFrame, text = 'run...', command = self.openSql)

        openOptions = tk.OptionMenu(openSqlFrame, self.toOpen_SQL, *self.envs)
        openOptions.configure(width = 10)

        openOptions.grid(row = 0, column = 0)
        btnOpener.grid(row = 1, column = 0)

    #repeaters
        repeaterFrame = tk.LabelFrame(
                        self.root, text = 'repeaters',
                        padx = 5, pady = 5)
        repeaterFrame.configure(padx = 20)

        #tracker                
        trackFrame = tk.LabelFrame(
                    repeaterFrame, text = 'tracker',
                    padx = 5, pady = 5)

        btnTrack = tk.Button(
                    trackFrame, text = 'track', command = self.trackProc)

        btnTrack.grid(row = 0, column = 0)

        inTrack = tk.Entry(trackFrame, width =25, text = 'Enter process Name')
        inTrack.grid(row = 0, column = 1, padx = [10,0])

        trackToScreen = tk.Checkbutton(
                        jigFrame, text = 'to_screen', variable = self.toScreen,
                        command = self.toScreenProc)#, anchor = tk.W)
        trackToScreen.deselect()
        
        
        trackFrame.grid(row = 0, column = 0, sticky =  tk.W+tk.E)

        #run user proc
        runProcFrame = tk.LabelFrame(
                    repeaterFrame, text = 'Run User Process',
                    padx = 5, pady = 5)

        btnRunProc = tk.Button(
                    runProcFrame, text = 'run',
                    command = self.runUserProc)

        userProcs = self.buildUserProcDropDown()
            
        menuRunProc = tk.OptionMenu(
                            runProcFrame, self.procToRun, *userProcs)
        menuRunProc.config(width = 20)

        btnRunProc.grid(row = 0, column = 0)
        menuRunProc.grid(row = 0, column = 1)
        
        runProcFrame.grid(row = 1, column = 0, sticky = tk.W+tk.E)



    #goto
        #mail
            
        goToFrame = tk.LabelFrame(
                    self.root, text = 'goto',
                    padx = 5, pady = 5)
        
        self.mailFrame = tk.LabelFrame(
                    goToFrame, text = 'mail',
                    padx = 5, pady = 5)

        btnTrack = tk.Button(
                    goToFrame, text = 'mail', command = self.openMail)

        btnTrack.grid(row = 0, column = 0)

        self.mail = tk.Entry(goToFrame, width =25, text = 'Enter self.mail Name')
        self.mail.grid(row = 0, column = 1, padx = [10,0])
        
        
        goToFrame.grid(row = 0, column = 0, sticky =  tk.W+tk.E)

        #report
        reportFrame = tk.LabelFrame(
                    goToFrame, text = 'report',
                    padx = 5, pady = 5)

        btnTrack = tk.Button(
                    goToFrame, text = 'report', command = self.openReport)

        btnTrack.grid(row = 1, column = 0)

        report = tk.Entry(goToFrame, width =25, text = 'Enter report Name')
        report.grid(row = 1, column = 1, padx = [10,0])
        
        
        goToFrame.grid(row = 0, column = 0, sticky =  tk.W+tk.E)
        
        
    #other stuff
    #verbose
        otherFrame = tk.LabelFrame(self.root, text = 'other functions')

        cbVerbose = tk.Checkbutton(
                        otherFrame, text = 'verbose',
                        variable = self.verbose, command = self.setVerbose,
                        pady = 5)
        cbVerbose.pack()

    #web teams
       
            
        btnWebTeams = tk.Button(otherFrame, text = 'web teams',
                                command = self.startWebTeams)
        btnWebTeams.pack()

    #web self.mail
        btnWebMail = tk.Button(otherFrame, text = 'webmail',
                                command = self.startWebMail, padx = 7)
        btnWebMail.pack(pady = 5)

    #help   
        btnWebMail = tk.Button(otherFrame, text = 'HELP',
                                command = self.startHelp, padx = 7)
        btnWebMail.pack(pady = 5)

    #functions help   
        btnWebMail = tk.Button(otherFrame, text = 'GenTax Funcs',
                                command = self.startFuncsHelp, padx = 7)
        btnWebMail.pack(pady = 5)

    #self.root
        openEnvFrame.grid(row = 0, column = 0, padx =5, pady = 5, ipadx = 5)
        openSqlFrame.grid(row = 0, column = 1, padx =5, pady = 5, ipadx = 5)
        jigFrame.grid(
            row = 0, column = 2, padx = 5,pady = 5, ipady = 4, ipadx = 5)
        repeaterFrame.grid(
            row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, ipadx = 5)
        goToFrame.grid(
            row = 1, column = 2, columnspan = 1, padx = 5, pady = 5, ipadx = 5)
        otherFrame.grid(row = 0, column = 3, rowspan = 2, pady = 5,
                        padx = 5, ipadx = 10, sticky = tk.N+tk.S)

        self.root.mainloop()
    
    def openSql(self):
        if self.toOpen_SQL.get() == self.dropdowndefault:
            return
        print(f'open sql env {self.toOpen_SQL.get()}')
        menu.process_commands(['open','sql',self.toOpen_SQL.get().lower()])

    def openGentax(self):
        if self.toOpen_GENTAX.get() == self.dropdowndefault:
            return
        print(f'open_gentax env {self.toOpen_GENTAX.get()}')
        menu.process_commands(['open',self.toOpen_GENTAX.get().lower()])

    def trackProc(self):
        if inTrack.get() == self.dropdowndefault:
            return
        print(f'track proc {inTrack.get()}')
        menu.process_commands(['track',inTrack.get()])
        updateUserProcDropDown()

    def toScreenProc(self):
        if self.toScreen.get():
            inTrack.set('')
            inTrack.config(state = tk.DISABLED)
        else:
            inTrack.config(state = tk.ACTIVE)

    def runUserProc(self):
        if self.procToRun.get() in ('--public--','--private--','None'):
            return
        print(f'runUserProc {procToRun.get()}')
        menu.app_process_repeater(process = self.procToRun.get())
        #menu.process_commands(['run', self.procToRun.get()])

    def buildUserProcDropDown(self):
        with open(PROCESSESFILE, 'r+') as file:
            procDict = json.load(file)
            procList = list(procDict['public'].keys())
            #remove defaults
            procList = [el for el in procList \
                        if not re.match(DFLTOUTERPROC,el)]
            #remove child queries
            procList = [el for el in procList \
                        if not re.match(r'(.*-\d+)$',el)]
            return ['--public--',
                     *procList,
                    '--private--',
                     *list(procDict['private'].keys())
                     ]
    
    def openMail(self):
        if self.mail.get() == self.dropdowndefault:
            return
        print(f'open mail: {self.mail.get()}')
        menu.process_commands(['mail',self.mail.get()])
        self.mail.set('')

    def openReport(self):
        if self.report.get() == self.dropdowndefault:
            return
        print(f'open report: {report.get()}')
        menu.process_commands(['report',self.report.get()])
        self.report.set('')

    def setVerbose(self):
        print('verbose is on')
        menu.process_commands(['v',])
    

    def startWebMail(self):
        print('starting web mail')
        menu.process_commands(['open','outlook_web'])

    def startWebTeams(self):
        print('starting web teams')
        menu.process_commands(['open','teams_web'])

    def startHelp(self):
        print('starting Help')
        menu.process_commands(['help',])

    def startHelp(self):
        print('starting Function Help')
        menu.process_commands(['help',])
        
    def runJiggler(self):
        if self.jiggler.get():
            print('run self.jiggler', end = '')
            if self.jigglerSchedule.get():
                print(' with schedule')
            else:
                print()
            self.cbjigsched.config(state = tk.DISABLED)

            menu.process_commands(['jiggleon',self.jigglerSchedule.get])
        else:
            print('turn off schedule')
            self.cbjigsched.config(state = tk.ACTIVE)

            menu.process_commands(['jiggleoff',])


def updateMenueOption(mo):
    pass


if __name__ == "__main__":
    app = Display()
