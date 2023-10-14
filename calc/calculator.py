import tkinter as tk
from tkinter.constants import NORMAL
from tkinter.messagebox import showinfo
from jsonHandler import SettingsJSONHandler

class CalculatorGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculator App or something")

        self.jsonhandler = SettingsJSONHandler()
        self.prop = self.jsonhandler.getProperty('preferences', 'colorscheme')

        self.menubar = tk.Menu()
        self.config(menu=self.menubar)

        self.settingsMenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Settings", menu=self.settingsMenu)
        self.settingsMenu.add_command(label="Preferences...", command=self.create_settings_window)

        self.fontName = "Segoe UI"
        self.fontSize = 20

        self.FONTSTYLE = (self.fontName, self.fontSize, NORMAL)

        self.screen = tk.Text(self, height=5, width=20)
        self.screen.grid(columnspan=5, sticky='W')
        self.screen.configure(font=self.FONTSTYLE, state=tk.DISABLED)

        self.numberButtons = []

        self.xpad = 20
        self.ypad = 10

        for x in range(1,4):
            for y in range(0,3):
                self.button = tk.Button(self, padx=self.xpad, pady=self.ypad)
                self.button.grid(row=x, column=y)
                self.numberButtons.append(self.button)
        
        for i, v in enumerate(self.numberButtons):
            v['text'] = str(i+1)
            v['command'] = lambda i=i: self.appendToScreen(i+1)

        self.operations = ['+', '-', '×', '÷']

        self.operationButtons = []

        for i, v in enumerate(self.operations):
            self.button = tk.Button(self,
                                    padx=self.xpad, 
                                    pady=self.ypad, 
                                    command=lambda v=v: self.appendToScreen(v)
                                    )
            self.button.grid(row=i+1, column=4)
            self.button['text'] = v
            self.operationButtons.append(self.button)
            
        self.equalsButton = tk.Button(self, 
                                    padx=60, 
                                    pady=self.ypad, 
                                    command=self.calculate, 
                                    bg='#4287f5', 
                                    fg='white'
                                    )

        self.equalsButton['text'] = '='
        self.equalsButton.grid(row=5, column=0, columnspan=2)
        self.equalsButton.configure(font=self.FONTSTYLE, relief='solid', bd=0)
        
        self.clearButton = tk.Button(self, 
                                    padx=self.xpad+3, 
                                    pady=self.ypad, 
                                    command=self.clear, 
                                    bg='#db2e2e', 
                                    fg='white'
                                    )

        self.clearButton['text'] = 'C'
        self.clearButton.grid(row=5, column=2)
        self.clearButton.configure(font=self.FONTSTYLE, relief='solid', bd=0)

        for a, i in enumerate(['.', 0]):
            self.button = tk.Button(self, padx=self.xpad, pady=self.ypad, command=lambda i=i: self.appendToScreen(i))
            self.button['text'] = i
            self.button.grid(row=4, column=a)
            self.button.configure(font=self.FONTSTYLE, relief='solid', bd=0)
            self.numberButtons.append(self.button)
        
        self.sqrtButton = tk.Button(self, 
                                    padx=self.xpad-10, 
                                    pady=self.ypad, 
                                    command=lambda: self.appendToScreen('^')
                                    )
                                    
        self.sqrtButton['text'] = 'xⁿ'
        self.sqrtButton.grid(row=4, column=2)
        self.sqrtButton.configure(font=self.FONTSTYLE, relief='solid', bd=0)
        self.operationButtons.append(self.sqrtButton)

        for button in self.numberButtons:
            button.configure(font=self.FONTSTYLE, relief='solid', bd=0)
        
        for buttons in self.operationButtons:
            buttons.configure(font=self.FONTSTYLE, relief='solid', bd=0)

        self.bind('<Key>', self._keypressed)

        self.settings = SettingsHandler(self)
        self.settings.changeScheme(self.prop)


    def create_settings_window(self):
        SettingsWindow(self)

    #Decorator Function
    def disableAfter(foo):
        def wrapper(self, *arg):
            self.screen.configure(state=tk.NORMAL)
            foo(self, *arg)
            self.screen.configure(state=tk.DISABLED)
        return wrapper

    @disableAfter
    def appendToScreen(self, arg):
        if type(arg) == 'str':
            arg = " " + arg + " "
        self.screen.insert(tk.END, str(arg))

    @disableAfter
    def clear(self):
        self.screen.delete(1.0, tk.END)

    @disableAfter
    def calculate(self):
        sd = self.getInput()
        calculation = ""
        for i in range(len(sd)):
            if sd[i] == '×':
                calculation += '*'
            elif sd[i] == '÷':
                calculation += '/'
            elif sd[i] == '^':
                calculation += "**"
            elif sd[i] == ',':
                calculation += '_'
            else:
                calculation += sd[i]
        try:
            result = f'{eval(calculation):,}'
            self.screen.insert(tk.END, result)
        except:
            self.screen.insert(tk.END, 'ERROR')
      
    def getInput(self):
        screendata = self.screen.get('1.0', 'end-1c')
        self.screen.delete(1.0, tk.END)
        return screendata

    def _keypressed(self, event):
        if event.char in "0123456789+-":
            self.appendToScreen(event.char)
        elif event.char == '*':
            self.appendToScreen('×')
        elif event.char == '/':
            self.appendToScreen('÷')
        elif event.char == 'y' or event.char == '^':
            self.appendToScreen('^')
        elif event.keysym == 'Return':
            self.calculate()
        elif event.keysym == 'Escape':
            self.clear()
    
class SettingsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master=master)
        
        self.title('Settings')

        self.colorText = tk.Label(self, text='Color Scheme: ')
        self.colorText.grid(row=0, column=0)

        self.colorSchemeList = ['Light', 'Dark']

        self.selectedColorScheme = SettingsJSONHandler().getProperty('preferences', 'colorscheme')
        self.colorScheme = tk.StringVar(self, self.selectedColorScheme)

        self.colorSchemeOption = tk.OptionMenu(self, self.colorScheme, *self.colorSchemeList)
        self.colorSchemeOption.grid(row=0, column=1, padx=10, pady=50)

        self.saveButton = tk.Button(self, text='Save', command=self.applySettings)
        self.saveButton.grid(row=1, column=1)
    

    def applySettings(self):
        colorscheme = self.colorScheme.get()

        print(colorscheme)

        jsonhandler = SettingsJSONHandler()
        jsonhandler.setProperty('preferences', 'colorscheme', colorscheme)

        showinfo(title="Restart", message="Restart the app to notice the changes")
        print(colorscheme)
    
class SettingsHandler():

    def __init__(self, master):
        self.master = master

    def changeScheme(self, scheme):
        color = ""
        fontColor = ""

        if scheme == 'Light':
            color = '#fcfcfc'
            fontColor = 'black'
            self.master.screen.configure(bg='white', fg=fontColor)

        elif scheme == 'Dark':
            color = '#2e2e2e'
            fontColor = 'white'
            self.master.screen.configure(bg='black', fg=fontColor)
        
        self.master.configure(bg=color)
        for i in self.master.operationButtons:
            i.configure(bg=color, fg=fontColor)
        for i in self.master.numberButtons:
            i.configure(bg=color, fg=fontColor)


if __name__ == "__main__":
    app = CalculatorGUI()
    app.mainloop()