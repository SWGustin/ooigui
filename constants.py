from dataclasses import dataclass

#pause between gui actions
PAUSE = 0.1

#duration of mouse moves
MOVEDURATION = 0.1

#time in seconds between jiggles
JIGGLEFREQ = 90

#my primary username
USERNAME = 'sgustin'

#file on help notes
HELPFILE = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\notes.docx'

#robs help file
GENTAXFUNCSFILE = '\\\\cacdqpvsdvap009\\OntTax Common\\Drop-In\\sgustin\\GenTax Functions.txt'

#folder for holding all sqr info
SQR_FOLDER='C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS'

#mouse jiggler Schedule
MJSCHED = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\MouseJiggler\\mj_sched.json'

#processes file
PROCESSESFILE = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\Tracker\\processes.json'

#default inner process file
DFLTOUTERPROC = "defaultOuterProcess"

#processes
PROC = { 'chrome' : 'chrome.exe',
         'otd' : 'gtgen.exe',
         'teams': 'teams.exe',
         'ie': 'iexplore.exe',
         'edge':'msedge.exe',
         'fcr':'gtGen.exe',
         'outlook':'OUTLOOK.EXE',
         'sql':'Ssms.exe',
         'file_explorer':'explorer.exe'
    }

#button locations
LOC = {'otd':(320,750),
       'fcr':(280,750),
       'fcrNewMgr':(70,180),
       'ie':(950,750),
       'edge':(70,750),
       'chrome':(115,750),
       'sqr':(0,750),
       'outlook':(165,750),
       'visual_studio':(660,750),
       'teams':(710,750),
       'notepad':(815,755),
       'sql':(625,750),
       'page':(10,90),
       'file_explorer':(225,750)
    }

@dataclass
class Program:
    name: str = None
    exe: str = None
    button_loc: tuple = None
    host_prog: str = None
    address: str = None
    harness_loc: tuple = None

#friendly program structures
PROGS= {
'otd':Program(
    'otd', PROC['otd'], LOC['chrome'],
    'chrome', 'http://on34c03065363:8080/OTD/Web.Gentax/',
    (315,750)),
'ot2':Program(
    'ot2', PROC['edge'], LOC['edge'], 'edge',
    'http://intra.test.ot2.onttax.fin.gov.on.ca/OT2/Gentax/'),   
'ott':Program(
    'ott', PROC['edge'], LOC['edge'], 'edge',
    'http://intra.test.ott.onttax.fin.gov.on.ca/OTT/Gentax/'), 
'os2':Program(
    'os2', PROC['edge'], LOC['edge'],'edge',
    'https://intra.stage.uat.os2.onttax.fin.gov.on.ca/OS2/Gentax/'),    
'ots':Program(
    'ots', PROC['edge'], LOC['edge'], 'edge',
    'https://intra.stage.ppe.ots.onttax.fin.gov.on.ca/OTS/Gentax/'),    
'links': Program(
    'links', PROC['edge'], LOC['edge'], 'edge',
    'https://intra.fcr.onttax.fin.gov.on.ca/links/'),
'fcr':Program(
    'fcr', PROC['fcr'], LOC['chrome'], 'chrome',
    'http://on34c03065363.cihs.ad.gov.on.ca:8080/FCR/GenTax/',
    (280,750)),
'outlook': Program('outlook_loc', PROC['outlook'], LOC['outlook'],'outlook'),
'outlook_web': Program(
    'outlook_web', PROC['chrome'], LOC['chrome'], 'chrome',
    'outlook.office.com'),
'teams': Program('teams_loc', PROC['teams'], LOC['teams'], 'teams'),
'teams_web': Program(
    'teams_web', PROC['chrome'],LOC['chrome'], 'chrome',
    'https://teams.microsoft.com/go#'),
'planview': Program(
    'planview', PROC['chrome'],LOC['chrome'], 'chrome',
    'https://ontario.pvcloud.com/planview/Track/Time/'),
'sharepoint':Program(
    'sharepoint', PROC['chrome'],LOC['chrome'],'chrome',
    'https://fastenterprises-my.sharepoint.com/personal/apickett_gentax_com/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fapickett%5Fgentax%5Fcom%2FDocuments%2FShared%20with%20Everyone%2FTimesheets&FolderCTID=0x012000CAE6BB948AAC32428D9A21CF8E084F24'),
'sql_otd': Program(
    'sql_otd', PROC['sql'], LOC['sql'],
    'sql', 'cacdqpvsdvap004'),
'sql_ot2': Program(
    'sql_ot2', PROC['sql'], LOC['sql'],
    'sql', 'cacdqpvsdvap004'),
'sql_os2': Program(
    'sql_os2', PROC['sql'], LOC['sql'], 'sql',
    'cactigdcdbcls05.mgmt.cihs.gov.on.ca\\OS2MSSQL'),
'sql_ots': Program(
    'sql_ots', PROC['sql'], LOC['sql'], 'sql',
    'cactigdcdbcls05.mgmt.cihs.gov.on.ca\\OTSMSSQL'),
'sql_rep': Program(
    'sql_rep', PROC['sql'], LOC['sql'], 'sql',
    'cactigdcdbcls05.mgmt.cihs.gov.on.ca\\REPMSSQL'),
'file_explorer':Program(
    'file explorer', PROC['file_explorer'], LOC['file_explorer'])
}
            
