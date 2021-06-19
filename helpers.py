'''
functions and statuses
----------------------------------
checkIfOpen                 DONE
clickOn                     DONE
geturl                      DONE
inputWrapper                DONE
isRunning                   DONE
isThisScreen                DONE
makeFullScreen              DONE 
openViaStart                DONE
pageHasLoaded               DONE
replaceText                 DONE
----------------------------------
'''

import pyautogui as gui
import pyperclip as clip
import time
import threading
from typing import Union, Tuple, List
from constants import *
import psutil
import _globals as glob

def verbose(func):
    def inner(*args, **kwargs):
        if glob.verboseFlag:
            print(f'starting {func.__name__}({args},{kwargs})')        
        output = func(*args,**kwargs)
        if glob.verboseFlag:
            print(f' ---------- end {func.__name__} with output {output}')
        return output
    return inner

class EnvError(Exception):
    pass


@verbose
def list_dict_vals(DB:dict , tabs:int = 0)->None:
    print('-----------------------------------------')
    list_dict_vals_inner(DB,tabs)
    print('-----------------------------------------')

@verbose
def list_dict_vals_inner(DB :dict, tabs:int = 0)->None:
    for header, val in DB.items():
        print('\t'*tabs, end = '')
        print(f'-{header}:')
        if isinstance(val,dict):
            list_dict_vals_inner(val,tabs+1)
        elif callable(val):
            print('\t'*(tabs+1), end = '')
            print(val.__name__)
        elif isinstance(val,list):
            pass
        elif val:
            print('\t'*(tabs+1), end = '')
            print(val)

@verbose
def doubleclickon(button:Union[int, tuple, list, Program],
            duration:int = MOVEDURATION)->None:
    clickon(button, duration)
    gui.click()

@verbose
def clickon(
            *button:Union[int, tuple, list, Program],
            duration:int = MOVEDURATION)->None:
    currentPos = gui.position()
    if isinstance(button[0],int):
        click_loc = button
    elif isinstance(button[0],tuple):
        click_loc = button[0]
    elif isinstance(button[0],list):
        click_loc = button[0]
    elif isinstance(button[0], Program):
        click_loc = button[0].button_loc
    else:
        raise ValueError
    
    if currentPos == click_loc:
        gui.moveRel((10,10))
        gui.moveRel((-20,-20))
        time.sleep(duration)
    gui.moveTo(click_loc, duration = duration)
    gui.click()

def replaceText(to_replace:str, replacement:str, text:str = None)->None:
    if not text:
        gui.hotkey('ctrl','a')
        gui.hotkey('ctrl','c')
        text = clip.paste()
        gui.write(text.replace(to_replace, replacement))

@verbose
def waitfor(wait_time:int = None)->None:
    print('waitfor running')
    print(wait_time)
    if wait_time:
        time.sleep(wait_time)
    else:
        waitforpagetoload()

@verbose
def inputwrapper(command:List[str])->None:
    command = []
    the_list = input().lower().split()
    for idx, val in enumerate(the_list):
        command[idx] = val

@verbose
def openviastart(program:object)->None:
    gui.press('win')
    time.sleep(1)
    gui.write(program.name)
    time.sleep(1)
    gui.press('enter')

@verbose
def makefullscreen()->None:
    for _ in range(3):
        gui.hotkey('win', 'up')


@verbose
def isrunning(program:Program)->bool:
    for proc in psutil.process_iter():  
        try:
            if proc.name() == program.exe:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

@verbose
def getPageNo(url:str = None)->int:
    if not url:
        url = geturl(True)
    try:
        return int(url.split('#')[-1])
    except ValueError:
        return 0
    
@verbose
def waitforpagetoload(
                      func:callable = None,
                      *args, store_number:int = None, **kwargs)->bool:
    print('wait for load running')
    if store_number == None:
        store_number = getPageNo()
    if func:
        output = func(*args,**kwargs)
    else:
        output = False
    countr = 0
    time.sleep(5)
    while not pagehasloaded(store_number):
        countr += 1
        time.sleep(5)
        if countr > 10:
            return
    return output

@verbose
def pagehasloaded(number:int, url:str = None)->bool:
    return getpageno(url) != number

@verbose
def getpageno(url:str = None, safe:bool = True)->int:
    if not url:
        url = geturl(safe = safe)
    try:
        out = int(url.split('#')[-1])
    except ValueError:
        out = 0
    return out

@verbose
def geturl(safe:bool = False)->str:
    gui.hotkey('ctrl','l')
    if safe:
        gui.hotkey('ctrl','c')
        time.sleep(.25)
        output = clip.paste()
        return output
    if clip.paste() != '':
        gui.press('right')
        gui.press('space')
        gui.hotkey('ctrl','a')
    gui.hotkey('ctrl','c')
    gui.press('right')
    url = clip.paste()
    
    if url != '':
        gui.press('backspace')
        output = url
    else:
        output = url
    return output

@verbose
def isthisscreen(url:str)->bool:
    return ((url != '') and (url in geturl()))
    

@verbose
def readyto_(action:str = '')->bool:
    if input(f"confirm {action}: [y]/n") not in ('y','Y',''):
        print('cancelled')
        return False
    else:
        print('starting')
        time.sleep(1)
        gui.hotkey('alt','tab')
        return True

@verbose
def openFile(filename):
    openviastart(PROGS['file_explorer'])
    makefullscreen()
    gui.hotkey('ctrl','l')
    gui.write(filename)
    gui.press('enter')
    
@verbose
def checkifFileOpen(filePath:str)->bool:
    try:
        with open(filePath,'w') as f:
            pass
    except IOError:
        return True
    return False

@verbose
def checkifopen(program:Program, click:bool = True)->bool:
    if program.name == 'otp':
        print('cannot access otp programatically')
        return False
    if program.name not in PROGS.keys():
        print('bad env')
        raise EnvError
        return False
    if click:
        clickon(program)
    cntr = 0
    time.sleep(1)
    first_url = geturl()
    url_to_check_for = program.address
    url = ''
    
    if url_to_check_for in first_url:
        return True

    if first_url == ' ':
        gui.write('.')
        first_url = '. '
    
    while url_to_check_for not in url\
          and url != first_url: 
        cntr += 1
        if cntr == 10:
            break
        gui.hotkey('ctrl','tab')
        url = geturl()

    if first_url == '. ':
        gui.press('backspace')

    if not url or url == first_url and cntr>0:
        return False

    gui.press('esc')
    return True

@verbose
def displayProcesses():
    pass

@verbose
def reduceList(ls:List[str])->List[str]:
    while ls and ls[0] and isinstance(ls[0],list):
        ls = ls[0]
    return ls

#funcs for storing tracking
@verbose
def store_click(args)->List[Union[str,List[int]]]:
    pos = gui.position()
    return ('click',*pos)

@verbose
def store_hotkey(*keys:List[Union[List,str]])->List[Union[str,List[str]]]:
    keys = reduceList(keys)
    return ['hotkey',*keys]

@verbose        
def store_repeat(args:str)->List[str]:
    return ['run_process', args]

@verbose
def store_wait(_time:int = None)->List[int]:
    _time=reduceList(_time)
    if _time:
        return ['wait', _time]
    else:
        return ['wait']

@verbose
def store_press(key:List[str])->Tuple[Union[str,List[str]]]:
    key = reduceList(key)
    return('press', *key)

@verbose
def store_replace(vals:List[str])->Tuple[str]:
    return ('replace', *vals)

@verbose
def store_getconfirm()->List[str]:
    return['confirm']

@verbose
def store_openwindow()->List[str]:
    return['open window']

@verbose
def store_scroll(amount:int)->List[Union[str,int]]:
    x,y = gui.size()
    while not isinstance(amount,int):
        try:
            amount = int(*amount)
        except ValueError:
            amount = input('must be a valid amount to scroll try again')
            if amount[0] == 'scroll':
                amount = amount[-1]
            return store_scroll([amount])
        
    amount /= -100
    amount= int(amount*y)
    gui.hotkey('alt','tab')
    time.sleep(0.5)
    print(f'scrolling {amount}')
    gui.scroll(amount)
    time.sleep(0.5)
    gui.hotkey('alt','tab')
    return ['scroll',amount]

def storeWrite(*args:List[str])->List[str]:
    to_write = ' '.join(args)
    return ['write', to_write]

def store_moveRel(
            args:Union[Tuple[int],List[int]])->List[Union[str,List[int]]]:
    x,y = map(int, args)
    return ['move rel', [x,y]]

def store_clickRel(
            args:Union[Tuple[int],List[int]])->List[Union[str,List[int]]]:
    x,y = map(int, args)
    return ['click rel', [x,y]]

def store_doubleclickRel(
            args:Union[Tuple[int],List[int]])->List[Union[str,List[int]]]:
    try:
        x,y = map(int, args)
    except(ValueError):
        args = input('need to input x-movement y-movement (as ints)')
        args = args.split()
        return store_doubleclickRel(args)
    return ['double_click_rel', [x,y]]

def store_double_click(
            args:Union[Tuple[int], List[int]])->List[Union[str,List[int]]]:
    pos = gui.position()
    return ['double_click', *pos]


def doubleclickWrapper(args:Tuple[int])->None:
    gui.click()
    gui.click()

def doubleclickRelWrapper(args:Tuple[int])->None:
    gui.moveRel(*args)
    gui.click()
    gui.click()

def clickRelWrapper(args:Tuple[int])->None:
    gui.moveRel(*args)
    gui.click()

def moveRelWrapper(args:Tuple[int])->None:
    gui.moveRel(*args)

#functions to run
@verbose
def getconfirmation(*args)->None:
    gui.hotkey('alt','tab')
    conf = input('please confirm by pressing enter')
    gui.hotkey('alt','tab')

@verbose
def hotkeywrapper(keys:List[str])->None:
    gui.hotkey(*keys)

@verbose
def presswrapper(keys:List[str])->None:
    gui.press(keys)

@verbose
def replacewrapper(vals:List[str])->None:
    replaceText(*vals)

@verbose
def waitWrapper(vals:Union[int,List[int]])->None:
    vals = None
    try:
        vals = int(vals)
    except (TypeError):
        pass
    if isinstance(vals,int):
        waitfor(vals)
    elif isinstance(vals,list):
        vals = vals[0]
        waitWrapper(vals)
    else:
        waitfor()

@verbose
def openwindow(loc:Tuple[int])->None:
    clickon(loc)
    waitFor()
    clickon(loc)    

@verbose
def scroll(amount:int)->None:
    print(f'scrolling {amount}')
    gui.scroll(*amount)

@dataclass
class Trackable:
    keyword:str 
    store_process: any
    description:str
    run_process:any = None

#dict of tracker funcs
tracker_commands = {
            '': Trackable('click', store_click,'click at mouse position', clickon),
            'dcr': Trackable('double_click_rel', store_doubleclickRel,'click at mouse position', doubleclickRelWrapper),
            'dc': Trackable('double_click', store_double_click,'click at mouse position', doubleclickWrapper),
            'hk': Trackable('hotkey', store_hotkey, '("key other_key") to show a hotkey',hotkeywrapper),
            'r': Trackable('run_process', store_repeat,'repeate (perform inner process'),
            'w': Trackable('wait', store_wait, '[optional time] pause for [time] or until load', waitWrapper), 
            'p': Trackable('press', store_press, 'press a key', presswrapper),
            'replace':Trackable('replace',store_replace, '(text1, text2) replace text1 with text2', replacewrapper),
            'confirm':Trackable('confirm', store_getconfirm, 'get confirmation', getconfirmation),
            'o-w': Trackable('open window', store_openwindow, 'open a window in mail', openwindow),
            'scroll':Trackable('scroll', store_scroll, 'scroll the screen', scroll),
            None:Trackable('write', storeWrite, 'write a message', gui.write),
            'mr':Trackable('move rel', store_moveRel, 'move relative to last mouse loc', moveRelWrapper),
            'cr':Trackable('click rel', store_clickRel, 'click in a spot relative to last loc', clickRelWrapper)}

##end tracker funcs
