import sys

clean =   { 'prompt'      :'Hello World!',
            'buttons'     :(0, 1, 2) ,
            'title'       :'HW!',
            'helpfile'    :'demo.chm', 
            'context'     :1,
            'immediately' :True}

dirt = {1:(TypeError, 'prompt', 0),
        2:(TypeError, 'buttons', 'Hello World!'),
        3:(TypeError, 'title', 0),
        4:(FileNotFoundError, 'helpfile', 'demo.html', ),
        5:(TypeError, 'context', '1')}

def __test(step, D):
    first  = True
    string = '' 
    
    for k,v in D.items():
        if step == 0: break
        else:         step -= 1
        
        if isinstance(v, str): string += "{}='{}'".format(k, v)
        else:                  string += '{}={}'.format(k, v)
        
        if step != 0: string += ', '
    
    return exec('MessageBox({})'.format(string))
    
def test(iExcept, D):   
    
    for i in range(1, 7):
        try: __test(i, D)
        except iExcept: print('except: %s' % iExcept)
    
    return 'Fine'

def _error_test(c, d):

    for k, v in d.items():
        iClean = c.copy()
        if v[1] in c:
            iClean[v[1]] = v[2]
            try: __test(k, iClean)
            except v[0]: print('except: %s' % v[0])

try:
    sys.path.insert(0, '../bin') 
    from pyMessageBox import *
except:
    sys.path.insert(0, 'bin')
    from pyMessageBox import *

clean_test = test(KeyError, clean)
dirt_test  = _error_test(clean, dirt)