class test():
    def __init__(self, repeate, val1= None, val2 = None):
        self.val1 = val1
        self.val2 = val2
        print('before')
        print('------------------------------------')
        print(f'self.val1 = {self.val1}')
        print(f'self.val2 = {self.val2}')
        print('------------------------------------')
        if repeate:
            testval = test(False, self.val2)

        print('after')
        print('------------------------------------')
        print(f'self.val1 = {self.val1}')
        print(f'self.val2 = {self.val2}')
        print('------------------------------------')


if __name__ =='__main__':
    testr = test(True, 'value 1', 'value 2')
