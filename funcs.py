from mousejiggler.mouseJiggler import Jiggler
from helpers import *
from repeater.repeater import Repeater
from tracker.tracker import Tracker, PrivateTracker
import multiprocessing
import os
import _globals as glob
import json


@verbose
def toggle_verbose()->None:
    glob.verboseFlag = not(glob.verboseFlag)
    if glob.verboseFlag:
        print('verbose is now ON')
    else:
        print('verbose is now OFF')

@verbose
def endprogram()->bool:
    return True

@verbose
def gethelp()->bool:
    openFile(HELPFILE)
    return False

@verbose
def gethelpFuncs()->bool:
    openFile(GENTAXFUNCSFILE)
    return False
    
@verbose
def oneoffrepeater(prompts:bool = True, default_delay:int = None)->None:
    if not default_delay:
        default_delay = input('if you wish to put in a default delay add it now in seconds')
    if prompts:
    #this is the dict of available actions the repeater can take
        print('create a list of things to process. (mouse over + enter on things to process)')
        print('press "q" to finish')
        print('press "r" for each time you want the repetition to occur')

    tracker(DFLTOUTERPROC)

    if not readyto_('run'):
        return
    commands = {el.keyword:el.run_process for el in tracker_commands.values()}

    if default_delay != '':
        outer_repeater = Repeater(
                            commands, PROCESSESFILE\
                            ,DFLTOUTERPROC, sleepTime = int(default_delay))
    else:
        outer_repeater = Repeater(commands, PROCESSESFILE, DFLTOUTERPROC)

@verbose
def app_process_repeater(*args:List[str], process:str)->None:
    process_repeater(*args,process = process, prompts = False)

@verbose
def process_repeater(
            *args:List[str],
            process:str = None,
            prompts:bool = True)->None:
    processes = None
    with open(PROCESSESFILE, 'r') as file:
        processes = json.load(file)
    if prompts:
        print('what manually defined process would you like to repeat')
        for idx, item in enumerate(processes['public'].keys()):
            if item not in (DFLTOUTERPROC):
                print(f'\t-{idx-1}:{item}')
        process = input()
        try:
            process = int(process)
        except ValueError:
            pass
        if isinstance(process,int):
            process = list(processes['public'].keys())[process+1]
            
    commands = {el.keyword:el.run_process for el in tracker_commands.values()}

    if prompts:
        while process not in processes['public'].keys() and process != 'q':
            if process == 'default':
                if not readyto_('run'):
                    return False
                Repeater(commands, PROCESSESFILE, DFLTOUTERPROC)
                return
            process = input('that was not a valid public process try again')
            try:
                process = int(process)
            except ValueError:
                pass
            if isinstance(process,int):
                process = list(processes['public'].keys())[process+1]


        if not readyto_('run'):
            return
    print(f'specific proces = {processes["public"][process]}')
    print(f'process = {process}')
    Repeater(commands, PROCESSESFILE, process)

@verbose
def tracker(
            processName:str = None, second_var:str = None,
            commands:dict = tracker_commands)->None:
    if processName in ('del', 'delete'):
        processDB = None
        with open(PROCESSESFILE, 'r') as file:
            processDB = json.load(file)
        try:
            second_var = int(second_var)
            second_var = list(processDB['public'].keys())[second_var+1]
        except ValueError:
            pass
        try:
            
            print(f"delete '{second_var}'")
            if not readyto_():
                return
                
            del(processDB['public'][second_var])

            with open(PROCESSESFILE, 'w') as file:
                json.dump(processDB,file)
                file.truncate()
            print(f'deleted {second_var} from public processes')
            return
        except(KeyError):
            print(f"public process '{second_var}' doesn't exist")
            return
    elif processName in ('list','-l'):
        with open(PROCESSESFILE, 'r+') as file:
            processDB = json.load(file)
        list_dict_vals(processDB)
        return

    private_keywords =('private','priv','p','-p') 
    if second_var in private_keywords\
       or processName in private_keywords:
        tracker = PrivateTracker(commands,PROCESSESFILE)
    else:
        tracker = Tracker(commands,PROCESSESFILE)
    if processName and processName not in private_keywords:
        tracker.start(processName)
    else:
        tracker.start()        

@verbose
def openwebteams()->None:
    if isrunning(teams_web):
        clickon(teams_web)
    else:
        openViaStart(teams_web.host_prog)
    time.sleep(.5)
    gui.hotkey('ctrl','t')
    time.sleep(.5)
    gui.write(teams_web.address)
    gui.press('enter')

def to_home_screen()->None:
    clickon(LOC['page'])
    for _ in range(6):
        gui.hotkey('shift','tab')
    gui.press('enter')

@verbose
def main_to_mgr(mgr:str)->None:
    pageNo = getpageno()
    to_home_screen()
    pageNo += 1
    time.sleep(5)
    gui.write(mgr)
    waitforpagetoload(gui.press,'enter', store_number = pageNo)
    time.sleep(5)
    clickon(LOC['page'])

#cant pickle with decorator
def innerjiggle(T:int, sched:bool)->None:
    try:
        if sched:
            Jiggler.scheduleFile = MJSCHED
            
        j = Jiggler.getinstance(T = T)
        j.mousejiggle()
        
    except(AssertionError):
        pass

@verbose
def mousejiggleon(*schedule:Union[str,List[str]], T:int = JIGGLEFREQ)->None:
    print('jiggleon confirmed', end = '')
    if not schedule or schedule[0] in ['sched', 'schedule', 'True', True]:
        print(' with schedule')
        sched = MJSCHED
    else:
        sched = None
        print('')
    glob.mouse_proc = multiprocessing.Process(
                        target = innerjiggle,
                        kwargs = {'T':T, 'sched' : sched})
    glob.mouse_proc.daemon = True
    glob.mouse_proc.start()
    
@verbose
def mousejiggleoff()->None:
    try:
        glob.mouse_proc.terminate()
        glob.mouse_proc.join()
        glob.mouse_proc = None
        print('jiggleoff confirmed')
    except (AttributeError, AssertionError):
        pass
    

@verbose
def openprog(prog_name:str, *db:List[str], came_from:str = None)->None:
    #check that a good name was passed
    if prog_name == 'sql' and db[0] is not None:
        prog_name = prog_name + '_' + db[0]

    try:
        prog = PROGS[prog_name]
    except KeyError:
        print('bad program or env name try again')
        return

    #prevent access to otp
    if prog.name == 'otp':
        input('cannot access otp programatically')
        return False

    elif prog.host_prog in ('chrome','ie','edge'):        
        if prog.name in ['otd','fcr']:
            openharness(prog)
        if not isrunning(prog):
            clickon(prog)
            time.sleep(2)
            while not isrunning(prog):
                time.sleep(1)
            gui.hotkey('alt','tab')
            time.sleep(5)
        if checkifopen(prog):
            return False
        if geturl() != ' ':
            gui.hotkey('ctrl','t')
            time.sleep(1)
            gui.hotkey('ctrl','l')
            gui.press('backspace')
            time.sleep(.1)
        gui.write(prog.address)
        gui.press('enter') 

    elif prog.host_prog is 'sql':
        was_running = isrunning(prog)
        clickon(prog)
        if not was_running:
            time.sleep(5)
            while not isrunning(prog):
                time.sleep(1)
            time.sleep(20)
            clickon(prog)
            #issue here
            gui.moveRel(95,-75)
            gui.click()
            time.sleep(1)
            gui.write(prog.address)
            gui.press('enter')
            time.sleep(10)

        gui.hotkey('ctrl','shift','alt','o')
        time.sleep(2)
        gui.hotkey('ctrl','l')
        gui.write(SQR_FOLDER)
        gui.press('enter')
        time.sleep(1)
        gui.press('enter')
        time.sleep(5)
        if was_running:
            clickon(150,40)
            time.sleep(1)
            clickon(330,60)
            time.sleep(1)
            clickon(620,130)
            time.sleep(1)
            gui.write(prog.address)
            gui.press('enter')
            time.sleep(5)
        gui.hotkey('ctrl','u')
        time.sleep(5)
        gui.write(prog.name[-3:]+'_GTAPP')
        gui.press('enter')
        
    else:
        if not isrunning(prog):
            clickon(prog)
            time.sleep(2)
            while not isrunning(prog):
                time.sleep(1)
        else:
            gui.hotkey('win','d')
            clickon(prog)

    if came_from == 'menu':
        gui.hotkey('alt','tab')
    return False

@verbose
def copyslice(user:str, sliceFrom:str, sliceTo:str):
    openProg('ot2')
    input('enter ot2 and click new manager then click here and hit enter')
    gui.hotkey('alt','tab')
    time.sleep(1)
    gui.scroll(500)
    gui.write('copy')
    gui.press('enter')
    time.sleep(3)
    #check if page loaded

    if not key:
        print('opening letters tab')
        return False
    
    for _ in range(4):
        gui.hotkey('shift','tab')
    #problem with writing query to query slice for user and number
    gui.write(user)
    gui.press('enter')
    time.sleep(3)
    #check if page loaded

    return False

@verbose
def openharness(prog:Program)->None:
    if not isrunning(prog):
        clickon(prog.harness_loc)
        input("press enter to continue once you've entered your password")
        
@verbose
def openreport(key:str = None, from_main:bool = True)->None:
    return openreport_or_letter('report', from_main=from_main)

@verbose
def openlettertype(key=None, from_main = True)->None:
    out = openreport_or_letter('mail', key = key)
    for _ in range(4):
        gui.press('tab')
    pageNo = getPageNo()
    gui.press('enter')
    time.sleep(1)
    waitforpagetoload(store_number = pageNo)
    for _ in range(21):
        gui.press('tab')
    gui.press('enter')
    time.sleep(1)
    gui.hotkey('alt','tab')
    return out

@verbose
def openreport_or_letter(
                        toOpen:str, key:str = None,
                        from_main:bool = False)->None:
    openprog('otd')
    if not checkifopen(PROGS['otd'], click = False):
        input("press enter once you're logged in")
        
    main_to_mgr(toOpen)
    
    if not key:
        print(f'opened {toOpen} tab')
        #gui.hotkey('alt','tab')
        return False

    for _ in range(14):
        gui.press('tab')
    gui.write(key)
    gui.press('enter')
    time.sleep(2)
    for _ in range(8):
        gui.press('tab')
    gui.press('enter')
    
    if from_main:
        gui.hotkey('alt','tab')

    return


@verbose
def lettercheck(key:str = None)->None:
    print(f'checking letter {key}')
    with open("", r) as f:
        config_data = json.load(f)

@verbose
def opensqr(key:str = None)->None:
    print(f'open_sqr: {key}')

@verbose
def openemail(toFCR:str = False)->None:
    if isrunning('outlook'):
        clickon(LOC['outlook'])
    else:
        openviastart('outlook')

@verbose
def openproject(proj:str)->None:
    openFCR()
    gui.write('fcr')
    gui.press('enter')
    time.sleep(1)
    gui.write(proj)
    gui.press('enter')

@verbose
def startday():
    #reimplement
    pass



