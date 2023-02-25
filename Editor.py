import zipfile
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk  
import fileinput
import re
import os

root =tk.Tk()
root.title('Conquest Unit Editor')
root.geometry('350x400')
root.resizable(0,0)
save_path = '1'

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx()+30
        y = y + cy + self.widget.winfo_rooty()+30
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text,justify=tk.LEFT,
                      background="white", relief=tk.SOLID, borderwidth=1,
                      font=("Arial","10","normal"))
        label.pack(side=tk.BOTTOM)
    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

def OpenSave():
    global save_path
    print(save_path)
    save_path = filedialog.askopenfilename(filetypes=[('save files','*.sav')])
    name = os.path.basename(str(save_path))
    save_file = save_path
    print(save_path)
    save_file = zipfile.ZipFile(save_path, 'r')
    save_file.extractall('')
    save_file_name['text'] = name    
    squad_cbox['value'] = GetSquadName()
    squad_cbox.current(0)
    ShowSquadMember(squad_cbox.current())
    Target_Squad_List['value'] = GetTargetSquad()
    Target_Squad_List.current(0)
    Target_Squad_ID = Target_Squad_List.current() + 1
    if (Target_Squad_ID == squad_cbox.current()):
        Target_Squad_ID = Target_Squad_ID + 1
    ShowTargetUnit(Target_Squad_ID)
    
def GetSquadName():
    squad_string = 'CampaignSquads'
    squad_name = []
    with open(campaign_file,'r') as file:
        test_flag = True
        while test_flag:
            line = file.readline()
            result = re.search('{CampaignSquads',line)
            if result is not None:
                while True:
                    text2 = file.readline()
                    squad = re.search('"(.*)" "(.*)"( 0x[0-9|a-f|A-f]{4})*',text2)
                    if squad is not None:
                        squad_info = squad.group(0).split()
                        squad_name.append(squad_info[0])
                    else:
                        test_flag = False
                        break
    return squad_name

def GetSquadMember(Squad_id):
    scan_times = 0
    squad_menber = []
    with open(campaign_file,'r') as file:
        test_flag = True
        while test_flag:
            line = file.readline()
            result = re.search('{CampaignSquads',line)
            if result is not None:
                while True:
                    text2 = file.readline()
                    scan_times = scan_times + 1
                    if (scan_times  == Squad_id + 1):
                        squad = re.search('"(.*)" "(.*)"( 0x[0-9|a-f|A-f]{4})*',text2)
                        squad_info = squad.group(0).split()
                        for i in range(2, len(squad_info)):
                            squad_menber.append(squad_info[i])
                        return squad_menber
    
def ShowSquadMember(squad_id):
    name = GetSquadMember(squad_id)

    squad_member_cbox['value'] = name
    squad_member_cbox.current(0)
    Unit_ID = name[0]
    ShowUnitInfo(Unit_ID)
    
def ShowUnitInfo(Unit_Id):
    Unit_Id = '(?:Human|Entity) "(.*)" ' + Unit_Id
    with open(campaign_file,'r') as file:
        line = file.read()
        Unit = re.search(Unit_Id,line)
        Unit_info = Unit.group(0).split()
        Unit_Type['text'] = Unit_info[0]
        Unit_Name.config(state='normal')
        Unit_Name.delete("1.0","end")
        Unit_Name.insert("insert", Unit_info[1])
        Unit_Name.config(state='disabled')
    
def SquadSelected(event):
    squad_id = squad_cbox.current()
    ShowSquadMember(squad_id)
    Target_Squad_List['value'] = GetTargetSquad()
    Target_Squad_List.current(0)
    Target_Squad_Id = Target_Squad_List.current()
    if (Target_Squad_Id >= squad_cbox.current()):
        Target_Squad_Id = Target_Squad_Id + 1
    ShowTargetUnit(Target_Squad_Id)

def UnitSelected(event):
    Unit_Id = squad_member_cbox.get()
    ShowUnitInfo(Unit_Id)
    
def TargetSquadSelected(event):
    Target_Squad_Id = Target_Squad_List.current()
    if (Target_Squad_Id >= squad_cbox.current()):
        Target_Squad_Id = Target_Squad_Id + 1
    ShowTargetUnit(Target_Squad_Id)
    
def GetTargetSquad():
    Base_Squad =  squad_cbox.current()
    Squad_list = GetSquadName()
    Squad_list.pop(Base_Squad)
    return(Squad_list)

def ShowTargetUnit(squad_id):
    name = GetSquadMember(squad_id)
    Target_squad_member_cbox['value'] = name
    Target_squad_member_cbox.current(0)
    Unit_ID = name[0]
    ShowTargetUnitInfo(Unit_ID)

    
def TargetUnitSelected(event):
    Target_Unit_Id = Target_squad_member_cbox.get()
    ShowTargetUnitInfo(Target_Unit_Id)

def ShowTargetUnitInfo(Unit_Id):
    Unit_Id = '(?:Human|Entity) "(.*)" ' + Unit_Id
    with open(campaign_file,'r') as file:
        line = file.read()
        Unit = re.search(Unit_Id,line)
        Unit_info = Unit.group(0).split()
        Target_Unit_type['text'] = Unit_info[0]
        Target_Unit_Name.config(state='normal')
        Target_Unit_Name.delete("1.0","end")
        Target_Unit_Name.insert("insert", Unit_info[1])
        Target_Unit_Name.config(state='disabled')

def Move2Squad():
    Unit_Id = squad_member_cbox.get()
    test_flag = False
    Target_Squad_Id = Target_Squad_List.current() + 1
    Base_Squad_Id = squad_cbox.current() + 1
    scan_times = 0
    if (Target_Squad_Id >= Base_Squad_Id):
        Target_Squad_Id = Target_Squad_Id + 1
    with fileinput.input(campaign_file, inplace= True) as file:
        for line in file:
            line = line.rstrip()
            result = re.search('{CampaignSquads',line)
            if result is not None:
                test_flag = True
            text = re.search('"(.*)" "(.*)"( 0x[0-9|a-f|A-f]{4})*',line)
            if test_flag:
                if (scan_times == Base_Squad_Id):
                    line = re.sub(' ' + Unit_Id,'', line)
                if (scan_times == Target_Squad_Id):
                    line = line.rstrip('}')
                    line = line +' ' + Unit_Id + "}"
                scan_times = scan_times + 1
            print(line)
    ShowSquadMember(squad_cbox.current())

def ExchangeUnit():
    Base_Unit_Id = squad_member_cbox.get()
    Target_Unit_Id = Target_squad_member_cbox.get()
    test_flag = False
    Target_Squad_Id = Target_Squad_List.current() + 1
    Base_Squad_Id = squad_cbox.current() + 1
    scan_times = 0
    if (Target_Squad_Id >= Base_Squad_Id):
        Target_Squad_Id = Target_Squad_Id + 1
    with fileinput.input(campaign_file , inplace= 1) as file:
        for line in file:
            line = line.rstrip()
            result = re.search('{CampaignSquads',line)
            if result is not None:
                test_flag = True
            text = re.search('"(.*)" "(.*)"( 0x[0-9|a-f|A-f]{4})*',line)
            if test_flag:
                if (scan_times == Base_Squad_Id):
                    line=re.sub(Base_Unit_Id,Target_Unit_Id,line)
                if (scan_times == Target_Squad_Id):
                    line=re.sub(Target_Unit_Id,Base_Unit_Id,line)
                scan_times = scan_times + 1
            print(line)
    ShowSquadMember(Base_Squad_Id-1)
    ShowTargetUnit(Target_Squad_Id-1)
    
def SaveFile():
    with zipfile.ZipFile(str(save_path), 'w') as SaveFile:
        SaveFile.write(campaign_file)
    
campaign_file = './campaign.scn'

root.grid_columnconfigure((0, 1), weight=1)

LoadSave = tk.Button(root,text='Select Save File', command=OpenSave)
LoadSave.grid(row = 0, column= 0, sticky='n', padx = 10 ,pady = 2)
CreateToolTip(LoadSave, text = 'Load conquest save file to edit.\nIt should be in Documents\my games\gates of hell\profiles\\numbers\campaign')

save_file_name = tk.Label(root, width= 20)
save_file_name.grid(row = 0, column= 1, sticky='e', padx = 10, pady = 2)

squads_name = tk.Label(root,text = 'Squad Name',  width= 20)
squads_name.grid(row = 1, column= 0,sticky='e', padx = 10, pady = 2)

var1 = tk.StringVar()
squad_cbox = ttk.Combobox(root, textvariable= var1)
squad_cbox.grid(row = 1, column= 1,sticky='w', padx = 10, pady = 2)

squad_cbox.bind('<<ComboboxSelected>>', SquadSelected)

Unit_ID = tk.Label(root,text = 'Unit ID',  width= 20)
Unit_ID.grid(row = 2, column= 0,sticky='e', padx = 10, pady = 2)

var2 = tk.StringVar()
squad_member_cbox = ttk.Combobox(root, textvariable= var2)
squad_member_cbox.grid(row = 2, column= 1 , sticky='w', padx = 10, pady = 2)

squad_member_cbox.bind('<<ComboboxSelected>>', UnitSelected)

Unit_type = tk.Label(root,text = 'Unit type',  width= 20)
Unit_type.grid(row = 3, column= 0,sticky='w', padx = 10, pady = 2)

Unit_Type = tk.Label(root, width= 20)
Unit_Type.grid(row = 3, column= 1,sticky='e', padx = 10, pady = 2)

Unit_name = tk.Label(root,text = 'Unit name',  width= 20)
Unit_name.grid(row = 4, column= 0,sticky='w', padx = 10, pady = 2)

Unit_Name = tk.Text(root, height = 1.5, width= 23)
Unit_Name.grid(row = 4, column= 1,sticky='e', padx = 10, pady = 2)

Unit_Transfer = tk.Label(root,text = 'Unit Squad Transfer', height= 2, width= 20)
Unit_Transfer.grid(row = 5, columnspan = 2, column= 0 ,sticky='n', padx = 10, pady = 2)

Target_Squad = tk.Label(root, text= 'Target Squad', width= 20)
Target_Squad.grid(row = 6, column= 0,sticky='w', padx = 10, pady = 2)

var3 = tk.StringVar()
Target_Squad_List = ttk.Combobox(root, textvariable= var3)
Target_Squad_List.grid(row = 6, column= 1,sticky='e', padx = 10, pady = 2)

Target_Squad_List.bind('<<ComboboxSelected>>', TargetSquadSelected)

Target_Unit_ID = tk.Label(root,text = 'Target Unit ID',  width= 20)
Target_Unit_ID.grid(row = 7, column= 0,sticky='e', padx = 10, pady = 2)

var4 = tk.StringVar()
Target_squad_member_cbox = ttk.Combobox(root, textvariable= var4)
Target_squad_member_cbox.grid(row = 7, column= 1 , sticky='w', padx = 10, pady = 2)

Target_squad_member_cbox.bind('<<ComboboxSelected>>', TargetUnitSelected)

Target_Unit_type = tk.Label(root,text = 'Target Unit type',  width= 20)
Target_Unit_type.grid(row = 8, column= 0,sticky='w', padx = 10, pady = 2)

Target_Unit_Type = tk.Label(root, width= 20)
Target_Unit_Type.grid(row = 8, column= 1,sticky='e', padx = 10, pady = 2)

Target_Unit_name = tk.Label(root,text = 'Target Unit name',  width= 20)
Target_Unit_name.grid(row = 9, column= 0,sticky='w', padx = 10, pady = 2)

Target_Unit_Name = tk.Text(root, height = 1.5, width= 23)
Target_Unit_Name.grid(row = 9, column= 1,sticky='e', padx = 10, pady = 2)

Transfer_Unit = tk.Button(root, text = 'Transfer Unit', command= Move2Squad)
Transfer_Unit.grid(row = 10, column= 0,sticky='n', padx = 10, pady = 2)
CreateToolTip(Transfer_Unit, text= 'Transfer unit to target squad')

Exchange_Unit = tk.Button(root, text = 'Exchange Unit', command= ExchangeUnit)
Exchange_Unit.grid(row = 10, column= 1,sticky='n', padx = 10, pady = 2)
CreateToolTip(Exchange_Unit, text= 'Exchange two units in different squad')

saveButton=tk.Button(root,text='Save changes',command=SaveFile)
saveButton.grid(row = 11, columnspan= 2,column= 0,sticky='n', padx = 10, pady = 10)
CreateToolTip(saveButton, text= 'Save changes to conquest save file')

root.mainloop()
