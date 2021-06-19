from mousejiggler.mouseJiggler import Jiggler
from funcs import *
import _globals as glob
gui.PAUSE = .5
gui.FAILSAFE = True


def listProcesses(look_for= None):
    show_at_end = []
    for proc in psutil.process_iter():  
            try:
                print(proc.name())
                if look_for and look_for in proc.name():
                    show_at_end.append(proc.name()) 
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    if look_for:
        print(f'the processes matching the query are: {show_at_end}')
    return False

def jigglewrapper(T:int, sched:bool)->None:
    try:
        if sched:
            Jiggler.scheduleFile = MJSCHED
            
        j = Jiggler.getinstance(T = T)
        j.mousejiggle()
        
    except(AssertionError):
        pass


def workspace(*schedule, T = None):
    print('jiggleon confirmed', end = '')
    if schedule or schedule[0] in ['sched', 'schedule', 'True']:
        print(' with schedule')
        sched = MJSCHED
    else:
        sched = None
        print('')
    glob.mouse_proc = multiprocessing.Process(
                        target = jigglewrapper,
                        kwargs = {'T':T, 'sched' : sched})
    glob.mouse_proc.daemon = True
    glob.mouse_proc.start()
    return False


def to_test(func, *args, **kwargs):
    print(f'testing "{func.__name__}" with args {args} and kwargs {kwargs}')
    if func(*args, **kwargs):
        print('true')
    else:
        print('false')
    print(f'testing done')


if __name__ == '__main__':
    j = to_test(workspace, True, T = 15)
    while True:
        pass
