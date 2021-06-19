from menuoptions import *
import _globals as glob

gui.FAILSAFE = True
gui.PAUSE = PAUSE

def show_menu():
    print('\t\t\tMenu')
    print('\t------------------------------')
    commands = dict(sorted(COMMANDS.items(), key = lambda x:x[1].__name__))
    lastfunc = None
    coms = []
    for com, func in commands.items():
        if lastfunc == func:
            coms.append(com)
        elif coms != []:
            coms.sort(key = lambda x: len(x))
            apnd = '\n\t\t'
            if lastfunc.__name__ == 'openEnv':
                apnd += ', '.join([*ENVS.keys()])
            else:
                apnd= ''
            print(f'\t{", ".join(coms)} : {COMMAND_DESCRIPTIONS[lastfunc]} {apnd}')
            lastfunc = func
            coms = [com]
        else:
            coms =[com]
            lastfunc = func
    print(f'\t{", ".join(coms)} : {COMMAND_DESCRIPTIONS[lastfunc]} {apnd}')
    print('\t------------------------------')
    
def process_commands(command):
    if command and command[0] not in COMMANDS.keys():
        print('bad code')
        return False
    func = COMMANDS[command[0]]
    
    if len(command)>1:
        return func(*command[1:])
    else:
        return func()

def close_prog():
    try:
        glob.mouse_proc.terminate()
        glob.mouse_proc.join()
    except (AttributeError,AssertionError):
        pass

    exit()

if __name__ == '__main__':
    end = False
    while not end:
        time.sleep(0.5)
        show_menu()
        command = None
        while not command:
            command = input().lower().strip().split()
        end = process_commands(command)
        
    close_prog()
