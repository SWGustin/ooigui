from abc import ABC
import os
from datetime import datetime, timedelta

class Report(ABC):
    def __init__(self, rel_file_path, reportname):
        self.templateStr = ''
        self._reportStr = ''
        self.reportname = reportname
        filename = os.path.join(os.getcwd(),rel_file_path)

        with open(filename,'r') as file:
            self.templateStr = file.read()
        self.templateStr.rstrip('/n')
        self._compiled = False

    @property
    def report(self):
        return self._reportStr

    @report.setter
    def report(self, string):
        self._reportStr = string

    def compile(self):
        pass

    
class ProdMigration(Report):
    def __init__(self, reportName):
        super().__init__(r'templates\prod_migration_report.txt', reportName)
        self._testedBy = set()
        self._testedIn = set()
        self.background = ''
        self.solution = ''
        self.summary = ''
        self._sqlScripts = False
        self._defaultScriptText = 'No additional scripts or manual activities are required for this migration'
        self._scriptText = self._defaultScriptText

    def __str__(self):
        return self.report

    @property
    def sqlScripts(self)->bool:
        return self._sqlScripts

    @sqlScripts.setter
    def sqlScripts(self, script:bool):
        self._sqlScripts = script
        if script:
            self._scriptText = 'Additional scripts are required and are outlined in the "Manual Activities" excel sheet for this migration date'
        else:
            self._scriptText = 'No additional scripts or manual activities are required for this migration'
        
    @property
    def testedBy(self) -> list:
        return self._testedBy

    @property
    def testedIn(self) -> list:
        return self._testedIn

    def setTestedBy(self, name:str) -> object:
        if len(name)>0:
            name = name[0].upper()+name[1:].lower()
        self._testedBy.add(name)
        return self


    def setTestedIn(self, name:str) -> object:
        self._testedIn.add(name.upper())
        return self

    def compile(self):
        self.report = self.templateStr \
                    .replace('<MIGRATION DATE>',self.getWednesday())\
                    .replace('<SUMMARY>',self.summary)\
                    .replace('<BACKGROUND>',self.background)\
                    .replace('<SOLUTION>',self.solution)\
                    .replace('<TESTEDBY>',', '.join(self.testedBy))\
                    .replace('<ENVS>',', '.join(self.testedIn))\
                    .replace('<SCRIPTS>',self._scriptText)
        self._compiled = True

    @staticmethod
    def getWednesday()->str:
        days_ahead = 2-datetime.weekday(datetime.today())
        if days_ahead <= 0:
            days_ahead +=7
        
        return datetime.strftime(
                    datetime.today()
                    + timedelta(days = days_ahead),
                    "%d/%b/%Y")

    def writeToFile(self, path):
        if not self._compiled:
            self.compile()
        filepath = path+'/'+self.reportname+'_Prod_Migration.txt'
        cntr = 1
        while os.path.isfile(filepath):
            filepath = filepath.replace('.txt', f'({cntr}).txt')
            cntr+=1
        with open(filepath, 'w+') as outfile:
            outfile.write(self.report)

if __name__ == '__main__':

    test = ProdMigration('testreport')
    test.background =  'test background info'
    test.summary = 'summary stuff'
    test.setTestedBy('Will Roche').setTestedBy('Steph Hamer')
    test.writeToFile(r'C:\Users\GustinSa\OneDrive - Government of Ontario\Documents\SQRS\24046 new cohb financial expenditure report')
    print(test.report)
