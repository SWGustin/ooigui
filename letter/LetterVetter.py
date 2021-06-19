import json
import pyautogui as gui
import pyperclip as clip

class SingletonError(Exception):
    pass

class LetterVetter:

    _instance = None

    @property
    def configFile(self):
        return self._configFile

    @configFile.setter
    def configFile(self, val):
        self._configFile = val
        with open(self._configFile, 'r') as f:
            self._configDict = json.load(f)

    @property
    def configDict(self):
        return self._configDict
    
    @staticmethod
    def getInstance(configFile):
        if not LetterVetter._instance:
            return LetterVetter(configFile)
        else:
            return LetterVetter._instance

    def __init__(self, configFile):
        _configFile = None
        _configDict = None
        if LetterVetter._instance is not None:
            raise SingletonError('you can only have 1 letter vetter at a time')
        else:
            self.configFile = configFile
            LetterVetter._instance = self

    def checkForChar(self, chars:list[string])->dict:
        gui.hotkey('alt','a')
        gui.hotkey('ctrl','c')
        out = dict()
        text = clip.paste()
        for char in chars:
            if char in text:
                out[char] = out.get(char,0)+1
        

if __name__ == '__main__':
    test = LetterVetter.getInstance('C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\letterVetter\\letter_config.json')
    test2 = LetterVetter.getInstance('C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\letterVetter\\letter_config.json')
