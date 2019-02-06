from os import name as platform

class MessageBox(object):
    buttons = {
         0:'vbOKOnly',
         1:'vbOKCancel',
         2:'vbAbortRetryIgnore',
         3:'vbYesNoCancel',
         4:'vbYesNo',
         5:'vbRetryCancel',
         6:'vbCritical',
         7:'vbQuestion',
         8:'vbExclamation',
         9:'vbInformation',
         # 1,2,3,4 ...button will use, if user won't make change.
         10:'vbDefaultButton1',
         11:'vbDefaultButton2', 
         12:'vbDefaultButton3',
         13:'vbDefaultButton4',
         # Modal win for main application.
         14:'vbApplicationModal',
         # Modal win for all system.
         15:'vbSystemModal',
         16:'vbMsgBoxHelpButton',
         # Win on Foreground.
         17:'vbMsgBoxSetForeground',
         # Prompt right side.
         18:'vbMsgBoxRight',
         # For Hebrew or Arabian language.
         19:'vbMsgBoxRtlReading'}
         
    errors  = { 
        0: ('TypeError', 'Buttons must be int(0-19) or tuple with int.'),
        1: ('ValueError', "Button key: '{}' not found."),
        2: ('TypeError', "{} must be {}, but type is '{}'."),
        3: ('FileNotFoundError', "HelpFile on directory - '{}', not found."),
        4: ('KeyError', "If helpfile != None need set attribute context."),
        5: ('TypeError', "Can't use: {} for help file, please use '*.chm'."),
        6: ('TypeError', "Attribute helpfile must be path of chm file, not: {}.")}   
    
    value  = 'Here will be the return value (from MessageBox).'
    
    def __init__(self, prompt, buttons     = 0, 
                               title       = None, 
                               helpfile    = None, 
                               context     = None,
                               immediately = False):
    
        ''' Method __init__ class MessageBox.
            Required:
            prompt   - String expression displayed as 
                       the message in the dialog box. 
                       The maximum length of prompt is 
                       approximately 1024 characters, 
                       depending on the width of the characters used. 
                       If prompt consists of more than one line,
                       you can separate the lines using a carriage 
                       return character (Chr(13)), a linefeed character 
                       (Chr(10)), or carriage return – linefeed 
                       character combination (Chr(13) & Chr(10)) 
                       between each line.
            Optional:
            buttons  - tuple that is the 
                       sum of values specifying the 
                       number and type of buttons to display, 
                       the icon style to use, the identity 
                       of the default button, and the modality 
                       of the message box. If omitted, 
                       the default value for buttons is 0.

            title    - String expression displayed in 
                       the title bar of the dialog box. 
                       If you omit title, the application name 
                       is placed in the title bar.

            helpfile - String expression 
                       that identifies the Help file 
                       to use to provide context-sensitive 
                       Help for the dialog box. If helpfile 
                       is provided, context must also be provided.
            context  - Numeric expression that is 
                       the Help context number assigned to 
                       the appropriate Help topic by the Help 
                       author. If context is provided, helpfile 
                       must also be provided.
            immediately - show box after create. 

        '''
        
        self.prompt   = self.__isinstance(prompt, name='Prompt')
        self.buttons  = self.__buttons(buttons)
        self.title    = self.__isinstance(title, name='Title')
        self.helpfile = self.__isinstance(helpfile, name='Helpfile', path=True)
        self.context  = self.__isinstance(context, int, name='Context', context=True)
        self.file     = '{}\\__pyMessageBox.vbs'.format(getenv('temp'))
        
        if immediately: self.show()

    def __buttons(self, tup):
        ## Check values in tuple and if correct append to self.buttons.
        valstr = ''
        first  = True
        
        if isinstance(tup, int):
            if tup in self.buttons:  return self.buttons[tup]  
            else:                    return self.__error(1, tup)  
        elif isinstance(tup, tuple): pass       
        else:                        return self.__error(0)
        
        for i in tup: 
            if i in self.buttons: 
                if first: 
                    valstr += '{}'.format(self.buttons[i])
                    first   = False
                else:     valstr += ' + {}'.format(self.buttons[i])
                
            else: return self.__error(1, i)
        
        return valstr
    
    def __isinstance(self, val, iType=str, name='NoneType', path=False, context=False):
        if context and val == None:
            if self.helpfile != None: self.__error(4)
           
        if val == None: return val
        
        if isinstance(val, iType): 
                if path: 
                    if exists(r'%s' % val): 
                        try: 
                            form = val.split('.') 
                            form = form[len(form) - 1]
                        except: self.__error(6, val)
                        
                        if form != 'chm': self.__error(5, form)
                        else:             return abspath(val)
                    else: self.__error(3, val)
                else: return val
        else: self.__error(2, (name, iType, type(val)))

    def __error(self, key, val=None):
        # Return special script errors.
        key   = self.errors[key]
        line  = '\n{}\n'.format('--' * len(key[1]))
        txt  = line
        
        if val != None: 
            if isinstance(val, tuple) and len(val) >= 3: 
                txt += key[1].format(val[0], val[1], val[2])
            if isinstance(val, str): 
                txt += key[1].format(val)
        else: txt += key[1]
        txt += line

        exec("raise {}('''{}''')".format(key[0], txt))

    def show(self):
        ''' Method show class MessageBox.
            Method show MessageBox use early created MessageBox and return values.
                          Return Values:
            -------------------------------------------
            |   Button    |    Value    | Description |
            -------------------------------------------
            |   vbOK      |      1      |   OK        |
            -------------------------------------------
            |   vbCancel  |      2      |   Cancel    |
            -------------------------------------------
            |   vbAbort   |      3      |   Abort     |
            -------------------------------------------
            |   vbRetry   |      4      |   Retry     |
            -------------------------------------------
            |   vbIgnore  |      5      |   Ignore    |
            -------------------------------------------
            |   vbYes     |      6      |   Yes       |
            -------------------------------------------
            |   vbNo      |      7      |   No        |
            -------------------------------------------
            
        '''
        
        command = '('
        
        first   = True
        
        for k, v in self.__dict__.items():
            if v != None and k != 'immediately' and k != 'file': 
                if k != 'buttons' and k != 'context': 
                    if first: 
                        command += '"{}"'.format(v)
                        first    = False
                    else: command += ', "{}"'.format(v)  
                else:  command += ', {}'.format(v)
            else: break
        
        
        command += ')'
        sys_command  = 'Set obj = WScript.StdOut'.format(command)
        sys_command  += '\ncur = MsgBox{}'.format(command)
        sys_command  += '\nobj.write(cur)'
        
        with open(self.file, 'w') as file:
            file.write(sys_command)
        
        pip = Popen('WScript %s' % self.file, stdout=PIPE)
        
        while pip.poll():
            pass
        
        self.value = int(str(pip.stdout.readline()).split("'")[1])
        return self.value
            
    def __call__(self):
        return self.show()
    
    def __str__(self):
        return str(self.value)

                
if platform != 'nt': raise SystemExit("Script will close.\nАvailable only for os windows")
if __name__ == '__main__':
    from subprocess import Popen, PIPE
    from os import getenv
    from os.path import exists, abspath

else:
    temp = {'Popen("explorer.exe",  stdout=PIPE)': ('subprocess', 'Popen, PIPE'),
            "getenv('temp')": ('os', 'getenv'),
            "exists('..\\'); abspath('.\\')": ('os.path', 'exists, abspath')}
    
    for key in temp.keys():
        try: eval(key);
        except: exec('from {} import {}'.format(temp[key][0], temp[key][1]))
    
    del temp
