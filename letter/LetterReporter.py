from LetterVetter import LetterVetter
import os
import mdutils

class LetterReporter:

    def __init__(self, vetting_file, output_dir, report_format_file):
        self.output_dir = output_dir
        self.vetting_file = vetting_file
        self.data = LetterVetter.getInstance(vetting_file).configDict
        self.report_format_file = report_format_file

    def report(self):
        i = 1
        self.data['letter type'] = 'test type'
        file_name = self.output_dir+self.data['letter type']
        if os.path.isfile(file_name+'.txt'):
            while os.path.isfile(file_name+f'({i}))'):
                i+=1
            file_name = file_name+f'({i})'

        file_name = file_name + '.txt'

            
        with open(file_name, 'w+') as f:
            f.write('test')

        with open(self.report_format_file, 'r') as f:
            print(f.readline())




if __name__ == '__main__':

    v_file = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\Letter\\letter_config.json'
    out_dir = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\Reports\\'
    format_file = 'C:\\Users\\GustinSa\\OneDrive - Government of Ontario\\Documents\\SQRS\\script\\Letter\\report_format.txt'
    
    test = LetterReporter(v_file,out_dir,format_file)
    test.report()
            
