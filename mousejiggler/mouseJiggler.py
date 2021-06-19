import pyautogui as gui
from datetime import datetime
import time
import json

class JiglrMeta(type):
    def __init__(cls, *args, **kwargs):
        cls._instance = None
        cls._scheduleFile = None
        cls._scheduleDict = None
        cls._timeBetween = None
        cls._weekdays = ["Monday", "Tuesday", "Wednesday", \
                   "Thursday", "Friday", "Saturday", "Sunday"]
        cls._duration = 0.1

    @property
    def scheduleFile(cls):
        return cls._scheduleFile

    @scheduleFile.setter
    def scheduleFile(cls, fileName):
        cls._scheduleFile = fileName
        with open(cls._scheduleFile, 'r') as f:
            cls._scheduleDict = json.load(f)
        
    @property
    def scheduleDict(cls):
        return cls._scheduleDict

    @scheduleDict.setter
    def scheduleDict(cls, dictn):
        cls._scheduleDict = dictn        

    @property
    def duration(cls):
        return cls._duration

    @duration.setter
    def duration(cls, dur):
        cls._duration = dur

    @property
    def timeBetween(cls):
        return cls._timeBetween

    @timeBetween.setter
    def timeBetween(cls, time_):
        cls._timeBetween = time_

    @property
    def weekdays(cls):
        return cls._weekdays


class Jiggler(metaclass = JiglrMeta):
    _instance = None
        
    @classmethod
    def getinstance(cls, * , T = None):
        if T:
            Jiggler.timeBetween = T
        if Jiggler._instance == None:
            return Jiggler()
        else:
            return Jiggler._instance

        
    def __init__(self):
        if Jiggler._instance != None:
            raise Exception('only one mouse jiggler allowed')
        else:
            Jiggler._instance = self
            self._position = None
            
    def mousejiggle(self):
        while True:
            if Jiggler.scheduleDict:
                if Jiggler.weekdays[datetime.today().weekday()] \
                   not in Jiggler.scheduleDict['days']:
                    return none
                idx = 0
                for times in Jiggler.scheduleDict['times']:
                    H,M = map(int,times[0].split(':'))
                    sched_time = datetime.now()\
                                 .replace(hour = H, minute = M\
                                    , second = 0, microsecond = 0)
                    if sched_time.time() < datetime.now().time():
                       idx+=1
                    else:
                        break
                if idx == 0 or Jiggler.scheduleDict['times'][idx-1][1] == 'OFF':
                    time_to_sleep = (sched_time - datetime.now()).total_seconds()
                    if time_to_sleep < 0:
                        return
                    time.sleep(time_to_sleep)
                    
            if self._position == gui.position():
                gui.moveTo((1065,750))
                time.sleep(0.1)
                gui.click()
                gui.moveTo(self._position)
                gui.hotkey('alt','tab')
                
            self._position = gui.position()
            time.sleep(Jiggler.timeBetween)
        

if __name__ == "__main__":
    mj = Jiggler()
    Jiggler.scheduleFile = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\MouseJiggler\\mj_sched.json'
    mj.mousejiggle()
