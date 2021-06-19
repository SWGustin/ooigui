#from constants import *
#commands options

from funcs import *

COMMANDS = {'e': endprogram,                #done
            'end':endprogram,               #done
            'email_check' : openemail,      #DONE
            'ec' : openemail,               #todo
            'h': gethelp,                   #TEST
            'hfuncs': gethelpFuncs,         #test
            'funcs':gethelpFuncs,           #test
            'help': gethelp,
            'jiggleon': mousejiggleon,      #DONE
            'jiggleoff': mousejiggleoff,    #DONE
            #'lc':letterCheck,               #not done
            #'letter_check':letterCheck,     #not done
            'm':openlettertype,             #DONE
            'mail':openlettertype,          #DONE
            'open': openprog,               #DONE
            #'open_project': openProject,    #waiting on openFCR
            #'prj': openProject,             #waiting on openFCR
            'q':endprogram,                 #done
            'quit':endprogram,              #done
            'rep': oneoffrepeater,          #DONE
            'repeat': oneoffrepeater,       #DONE
            'rpt':openreport,               #partial
            'report':openreport,            #partial
            'run':process_repeater,
            's': startday,                  #redo
            'start': startday,              #redo
            #'sql' : openprog,               #not done
            #'sqr':openSqr,                 #not done
            'teams_web': openwebteams,      #DONE
            'tw': openwebteams,             #DONE
            'track': tracker,               #done
            'verbose' : toggle_verbose,
            'v':toggle_verbose
            }

#description of commands
COMMAND_DESCRIPTIONS = {
    endprogram:'ends this program',
    gethelp: 'opens the notes document',
    gethelpFuncs: 'opens the functions document',
    lettercheck:'check letter config',
    mousejiggleon:'turn on jiggler [with scheduler]',
    mousejiggleoff:'turn off jiggler',
    oneoffrepeater: 'this triggers the repeater process',
    openemail:'open first email, check for sqr and option to go there',
    #openenv:'opens an environment ...',
    openprog:'opens an environment ...',
    openlettertype:'open a letter (otd must be open)',
    openproject:'open a project from ontario fcr ...',
    openreport:'open a report',
    opensqr:'open sqr number ...',
    #opensqlserver:'open sql server to [OTD, OS2, OTS, RPT]',
    openwebteams:'open via teams',
    process_repeater:'this repeats prior defined processes',
    startday:'opens relevant programs',
    tracker:'opens mouse tracker utility',
    toggle_verbose:'turns logging on and off'
}
