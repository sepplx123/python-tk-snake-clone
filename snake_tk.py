# !/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from random import randint
from datetime import datetime
from copy import deepcopy

# Fix for Python 2.x/3.x
try:
    import Tkinter as tk
    import tkMessageBox as msgbox    
    import ScrolledText as tkst
    import tkFileDialog as fdialog
except ImportError:
    import tkinter as tk
    import tkinter.messagebox as msgbox    
    import tkinter.scrolledtext as tkst


class GUI():
    def __init__(self, master):
        self.master = master

        self.spielfeld_rows = 10        
        self.spielfeld_columns = 10
        self.spielfeld_itemwidth = 50
        self.spielfeld_itemheight = 50

        self.speed_index = tk.StringVar()
        self.speed_index.set("")
        
        self.speed_selector = { "" : 900,
                                "speed_index_slow" : 500 ,
                                "speed_index_medium" : 350 ,
                                "speed_index_fast" : 250 ,
                                "speed_index_ultra" : 50
                               }

        self.topwindow_active = False

        self.cycle_time = 1                             # time in ms to wait for start next cycle
        self.time_last_cycle = datetime.now().time()
        self.cycle_counter = 0

        # clock variables
        self.act_time = datetime.now().time()
        self.hours = 0
        self.minutes = 0
        self.seconds = 0
        self.micros = 0
        self.strv_zeitangabe = tk.StringVar()           # actual time shown above
        self.strv_zeitangabe.set('00:00:00')
        self.strv_cycletime = tk.StringVar()            # cycletime
        self.strv_cycletime.set('000ms')

        # festlegen der sonstigen Optionen wie Titel, Geometry, etc.
        self.master.configure(background='black')
        #self.master.title("Snake Game V0.1")
        #self.master.geometry('600x600')

        # FRAMES
        self.fr1 = tk.Frame(self.master, width=0, height=20, background='grey')
        self.fr2 = tk.Frame(self.master,width=200, height=200, background='yellow')
        self.fr3 = tk.Frame(self.master, width=0, height=20, background='grey')
        self.fr1.pack(expand=1,fill='y',anchor='center')
        self.fr2.pack(fill='none',expand=0, side='top',anchor='center')
        self.fr3.pack(expand=1,fill='both',anchor='center')        

        self.fr_scoreboard = tk.Frame(self.fr1,width=0, height=0, background='black')
        self.fr_scoreboard.grid(row=0,column=1,ipadx=0,padx=5,pady=5,rowspan=1,columnspan=1,sticky="nesw")

        
        # Canvas
        self.canvas = tk.Canvas(self.fr2, width=500, height=500,
                                highlightthickness=1, background='white')
        self.canvas["background"]='red'
        self.canvas.grid(row=2,column=2,sticky='nesw')

        # BUTTONS
        #bQuit = tk.Button(self.fr3, text="Quit", width=8, height=1, command=self.closeWindow)        # Button Quit/Exit
        #bCreateWorld = tk.Button(self.fr3, text="load new Level",width=0, height=1, command=None)    # Button Create World
        #bCreateSnake = tk.Button(self.fr3, text="restart",width=0, height=1, command=None)           # Button paint Snake        
        #bCreateWorld.pack(side="left", padx=10, pady=1,anchor='s')
        #bCreateSnake.pack(side="left", padx=10, pady=1,anchor='s')       
        #bQuit.pack(side="right", padx=10, pady=1, anchor='s')        

        #Scrolled Textbox
        self.scroll_text = tkst.ScrolledText( self.fr3, width=0, height=10, wrap="word", fg='blue',)
        self.scroll_text.pack(fill='both',expand=1, side='bottom',anchor='s')
        #mytext = 'TESTTTTTT \n'
        #self.scroll_text.insert('insert', mytext)



        # Scoreboard variables
        self.strv_player_name = tk.StringVar()
        self.strv_player_name.set("")
        self.strv_act_level = tk.StringVar()
        self.strv_act_level.set("")
        self.strv_act_points = tk.StringVar()
        self.strv_act_points.set("")
        self.strv_time_passed = tk.StringVar()
        self.strv_time_passed.set("")

        # Class calls
        self.snake = Snake(self.spielfeld_rows,self.spielfeld_columns,self.scroll_text)
        self.spielfeld = Spielfeld(self.canvas,self.snake,self.spielfeld_rows,self.spielfeld_columns,
                                   self.spielfeld_itemwidth,self.spielfeld_itemheight,scrollbox=self.scroll_text)
        self.leveleditor = Leveleditor(spielfeld=self.spielfeld,snake=self.snake,
                                       canvas=self.canvas,scrollbox=self.scroll_text)
        self.scoreboard = Scoreboard(spielfeld=self.spielfeld,snake=self.snake,
                                     canvas=self.canvas,scrollbox=self.scroll_text,player_name=self.strv_player_name.get())
        self.spielsteuerung = Spielsteuerung(self.snake,self.spielfeld,self.leveleditor,self.scoreboard,
                                             canvas=self.canvas,scrollbox=self.scroll_text,speed_index=self.speed_index)
        ############################################################################################
    

        # Labels
        self.label_uhrzeit = tk.Label(self.fr1, textvariable=self.strv_zeitangabe,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 14))
        #self.label_uhrzeit.pack(side="left", padx=10, pady=1,anchor='n')
        self.label_uhrzeit.grid(row=0,column=0,ipadx=5,padx=5,pady=5,rowspan=1,columnspan=1,sticky="nw")
        
        self.label_cycletime = tk.Label(self.fr1, textvariable=self.strv_cycletime,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 14))
        #self.label_cycletime.pack(side="right", padx=10, pady=1,anchor='n')  
        self.label_cycletime.grid(row=0,column=2,ipadx=5,padx=5,pady=5,rowspan=1,columnspan=1,sticky="ne")


        self.label_player = tk.Label(self.fr_scoreboard, text="player:",
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_player.grid(row=0,column=1,padx=5,pady=5,rowspan=1,columnspan=1,sticky="e")
        self.label_player_name = tk.Label(self.fr_scoreboard, textvariable=self.strv_player_name,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_player_name.grid(row=0,column=2,ipadx=0,padx=0,pady=5,rowspan=1,columnspan=1,sticky="e")
        self.label_time = tk.Label(self.fr_scoreboard, text="time passed:",
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_time.grid(row=1,column=1,padx=5,pady=5,rowspan=1,columnspan=1,sticky="e")
        self.label_time_passed = tk.Label(self.fr_scoreboard, textvariable=self.strv_time_passed,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_time_passed.grid(row=1,column=2,ipadx=0,padx=0,pady=5,rowspan=1,columnspan=1,sticky="e")
        
        # separator
        self.label_seperator = tk.Label(self.fr_scoreboard, text="",
                                      bg='black', fg='#00bfff', width=5, height=0, font=("Arial", 10))
        self.label_seperator.grid(row=0,column=3,ipadx=5,padx=5,pady=5,rowspan=2,columnspan=1,sticky="nesw")
        ###########
        
        self.label_level = tk.Label(self.fr_scoreboard,  text="level:",
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_level.grid(row=0,column=4,padx=0,pady=5,rowspan=1,columnspan=1,sticky="e")
        self.label_act_level = tk.Label(self.fr_scoreboard, textvariable=self.strv_act_level,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_act_level.grid(row=0,column=5,ipadx=0,padx=5,pady=5,rowspan=1,columnspan=1,sticky="w")        
        self.label_points = tk.Label(self.fr_scoreboard, text="points:",
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_points.grid(row=1,column=4,padx=0,pady=5,rowspan=1,columnspan=1,sticky="e")       
        self.label_act_points = tk.Label(self.fr_scoreboard, textvariable=self.strv_act_points,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 10))
        self.label_act_points.grid(row=1,column=5,ipadx=0,padx=5,pady=5,rowspan=1,columnspan=1,sticky="w")
   

        # Menubar "Datei"-Menue
        self.menubar = tk.Menu(self.master)
        
        # "File"-Menue
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Game", menu=self.filemenu)
        self.filemenu.add_command(label="new game",
                                  command=self.new_game)
        self.filemenu.add_command(label="restart level",
                                  command=self.spielsteuerung.restart_level)       
        self.filemenu.add_command(label="reset",
                                  command=self.spielsteuerung.reset)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Game exit",
                                  command=self.closeWindow)
        
        # "Leveleditor"-Menue
        self.l_editor = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Level Editor", menu=self.l_editor) 
        self.l_editor.add_command(label="create level", command=lambda: self.start_leveleditor("create_level"))
        self.l_editor.add_command(label="edit level", command=lambda: self.start_leveleditor("edit_level"))
        self.l_editor.add_command(label="save level", command=lambda: self.start_leveleditor("save_level"))
        self.l_editor.add_command(label="load level", command=lambda: self.start_leveleditor("load_level"))      

        # "Hilfe"-Menue
        self.infomenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Info", menu=self.infomenu)        
        self.infomenu.add_command(label="About", command=self.showInfo)
        
        self.master.config(menu=self.menubar)



        self.create_keybindings()       # Funktion Keybindsings aufrufen        
        self.main_loop()                # start mainloop
        #print(self.act_time, 'init class GUI done')
        
        self.show_text('init class GUI done')
        #################               Init class GUI beendet

    def new_game(self):
        if self.strv_player_name.get():
            self.spielsteuerung.new_game()
        else:
            self.topwindow_open_newgame()
            
    def topwindow_open_newgame(self):
        """ creates a toplevel window to enter the players name """
        self.topwindow_active = True
        
        self.top = tk.Toplevel(bg='black')
        self.top.title("Snake - configure game settings")

        self.strv_name = tk.StringVar()
        self.strv_name.set("")
     
        L1 = tk.Label(self.top, text="enter player name:")
        L1.grid(row=0,column=0,ipadx= 5,padx=10,pady=5,sticky="e")
        E1 = tk.Entry(self.top, bd =5, fg="blue",textvariable=self.strv_name)
        E1.grid(row=0,column=1,columnspan=5,padx=10,pady=5,sticky="w")
        L2 = tk.Label(self.top, text="select difficulty:")
        L2.grid(row=1,column=0,ipadx= 15,padx=10,pady=5,sticky="w")

        rb1 = tk.Radiobutton(self.top, width=7, text="slow")
        rb2 = tk.Radiobutton(self.top, width=7, text="medium")
        rb3 = tk.Radiobutton(self.top, width=7, text="fast")
        rb4 = tk.Radiobutton(self.top, width=7, text="ultra")
        
        rb1.grid(row=1,column=1,padx=10,pady=5,sticky="e")
        rb2.grid(row=1,column=2,padx=10,pady=5,sticky="e")
        rb3.grid(row=1,column=3,padx=10,pady=5,sticky="e")
        rb4.grid(row=1,column=4,padx=10,pady=5,sticky="e")

        rb1.config(variable=self.speed_index,value="speed_index_slow",indicatoron=0,fg="blue",activeforeground="blue",activebackground="green",selectcolor="green")
        rb2.config(variable=self.speed_index,value="speed_index_medium",indicatoron=0,fg="blue",activeforeground="blue",activebackground="green",selectcolor="green")
        rb3.config(variable=self.speed_index,value="speed_index_fast",indicatoron=0,fg="blue",activeforeground="blue",activebackground="green",selectcolor="green")
        rb4.config(variable=self.speed_index,value="speed_index_ultra",indicatoron=0,fg="blue",activeforeground="blue",activebackground="green",selectcolor="green")

        rb1.select()
        rb2.deselect()
        rb3.deselect()
        rb4.deselect()
        
        button = tk.Button(self.top, text="OK", width=10,command=self.topwindow_close_newgame)
        button.grid(row=5,column=0,columnspan=1,padx=10,pady=5,sticky="sew")

    def topwindow_close_newgame(self):
        """ close the toplevel window and displayes the name on the game window """
        self.scoreboard.player_name = self.strv_name.get()
        if self.strv_name.get():
            self.spielsteuerung.new_game()
            self.top.destroy()
            self.topwindow_active = False
        else:
            self.top.destroy()
            self.topwindow_active = False
            self.topwindow_open()
        #print('self.scoreboard.player_name',self.scoreboard.player_name)


    def game_end_continue(self):
        if self.spielsteuerung.game_end and not self.topwindow_active:
            self.topwindow_open_game_end_continue()


    def topwindow_open_game_end_continue(self):
        self.topwindow_active = True
        
        self.top = tk.Toplevel(bg='black')
        self.top.title("Snake - Level finished")

        L0 = tk.Label(self.top, fg="blue",text="<<<<<   Congratulations! You win!!!   >>>>>")
        L0.grid(row=0,column=0,ipadx=20,padx=10,pady=5,columnspan=10,sticky="nesw")
        
        L1 = tk.Label(self.top, fg="blue",text="levels passed:")
        L1.grid(row=1,column=0,ipadx=0,padx=5,pady=5,sticky="e")
        L1_value = tk.Label(self.top, fg="blue",text="{0:>03d}".format(self.scoreboard.act_level))
        L1_value.grid(row=1,column=1,ipadx=0,padx=0,pady=5,sticky="w")
        
        L2 = tk.Label(self.top, fg="blue",text="time played:")
        L2.grid(row=2,column=0,ipadx=0,padx=5,pady=5,sticky="e")
        L2_value = tk.Label(self.top, fg="blue",text="{0:>07.3f}s".format(self.scoreboard.time_passed))
        L2_value.grid(row=2,column=1,ipadx=0,padx=0,pady=5,sticky="w")
        
        L3 = tk.Label(self.top, fg="blue",text="points this level:")
        L3.grid(row=3,column=0,ipadx=0,padx=5,pady=5,sticky="e")
        L3_value = tk.Label(self.top, fg="blue",text="{0:>08d}".format(int(self.scoreboard.act_points)))
        L3_value.grid(row=3,column=1,ipadx=0,padx=0,pady=5,sticky="w")
        
        L4 = tk.Label(self.top, fg="blue",text="total points:")
        L4.grid(row=4,column=0,ipadx=0,padx=5,pady=5,sticky="e")
        L4_value = tk.Label(self.top, fg="blue",text="{0:>08d}".format(int(self.scoreboard.total_points)))
        L4_value.grid(row=4,column=1,ipadx=0,padx=0,pady=5,sticky="w")
        
        L5 = tk.Label(self.top, fg="blue",text="Do you want to load next level?")
        L5.grid(row=5,column=0,ipadx=20,padx=10,pady=5,columnspan=10,sticky="nesw")


        b_save = tk.Button(self.top, fg="blue",text="save", width=8,command=None)
        b_save.grid(row=6,column=3,columnspan=1,ipadx=2,padx=2,pady=5,sticky="e")        
        b_continue = tk.Button(self.top, fg="blue",text="continue", width=8,command=None)
        b_continue.grid(row=6,column=4,columnspan=1,ipadx=2,padx=2,pady=5,sticky="e")
        b_end = tk.Button(self.top, fg="blue",text="end", width=8,command=self.topwindow_close_game_end_continue)
        b_end.grid(row=6,column=5,columnspan=1,ipadx=2,padx=2,pady=5,sticky="e")

        
        if self.spielsteuerung.level_passed:
            # Buttons continue or end or maybe save!
            pass
        else:
            pass
            # Hide button continue and make end to OK  

        
    def topwindow_close_game_end_continue(self):
        self.top.destroy()
        self.topwindow_active = False
        



    def main_loop(self):
        """ Updates the actual time and represents the mainloop.
        This function is called as fast as possible. """
        # Step1: get the actual time
        self.act_time = self.get_act_time()

        # Step2: Forward the variables to update the actual time shown on top of the window
        self.strv_zeitangabe.set('{0:02d}:{1:02d}:{2:02d}'.format
                (self.act_time.hour, self.act_time.minute, self.act_time.second))


        # Step3: create the cycle time and update the game_ui and game_settings
        time_delta = ((self.act_time.hour - self.time_last_cycle.hour)*3600*1000) + (
                     (self.act_time.minute - self.time_last_cycle.minute)*60*1000) + (
                     (self.act_time.second - self.time_last_cycle.second)*1000) + (
                     (self.act_time.microsecond - self.time_last_cycle.microsecond)/1000)
        
        # Step4: call game handler game_loop
        if time_delta >= self.speed_selector[self.speed_index.get()]:
            self.strv_cycletime.set("{0:>03d}ms".format(int(time_delta)))
            self.time_last_cycle = self.act_time
            
            self.spielsteuerung.do_game_start_stop()
 
            
        # Step5: Scoreboard variables values
        self.update_scoreboard_values()

        # Step6 game end or game win and continue
        self.game_end_continue()


        # Step7: start the loop again
        self.master.after(self.cycle_time, self.main_loop)  # mainloop



        # KEY-BINDINGS / EVENTS
    def create_keybindings(self):
        self.master.bind("<Left>", self.keyfunctions)
        self.master.bind("<Right>", self.keyfunctions)        
        self.master.bind("<Up>", self.keyfunctions)
        self.master.bind("<Down>", self.keyfunctions)
        self.master.bind("<p>", self.keyfunctions)
        self.master.bind("<Escape>", self.closeWindow)
        self.canvas.bind("<Button-1>", self.mousefunctions)
        self.canvas.bind("<Button-3>", self.mousefunctions)
        self.show_text('keybindings created')

        # Funktionsauswertung der Tastendrücke
    def keyfunctions(self,event):
        self.event = event
        #print(self.act_time, "Tastendruck =", self.event.keysym)
        self.spielsteuerung.keyevent(self.event.keysym)

    def mousefunctions(self,event):
        next_item_mode = 0
        self.event = event
        self.canvas.focus_set()

        if self.event.num == 1:
            next_item_mode = +1
        if self.event.num == 3:
            next_item_mode = -1
        if self.leveleditor.edit_mode:
            coords = (self.event.x, self.event.y)
            self.spielfeld.edit_mode(coords,next_item_mode)            

    def update_scoreboard_values(self):
        act_time = datetime.now().time()
        
        self.strv_player_name.set("{0:>}".format(self.scoreboard.player_name))
        self.strv_act_level.set("{0:>03d}".format(self.scoreboard.act_level))
        self.strv_act_points.set("{0:>08d}".format(int(self.scoreboard.act_points)))
        self.strv_time_passed.set("{0:>07.3f}s".format(self.scoreboard.time_passed))

        if self.spielsteuerung.game_start:
            time = self.scoreboard.calc_time_passed(self.scoreboard.time_level_start,act_time)
            self.strv_time_passed.set("{0:>07.3f}s".format(time))
            
    def start_leveleditor(self,command):
        #self.spielsteuerung.reset()

        if command == 'create_level':
            self.leveleditor.create_level()
        if command == 'edit_level':
            self.leveleditor.edit_level()
        if command == 'save_level':
            self.leveleditor.save_level()
        if command == 'load_level':
            self.leveleditor.load_level()

    def closeWindow(self,*event):
        self.event = event
        if self.event:
            print(self.act_time, "Tastendruck = Escape")
            print(self.act_time,'Program exit! window will be closed')
        self.master.destroy()
 
    def myquit(self):
        """ Messagebox Ask ok to cancel """
        if msgbox.askokcancel("Quit", "Do you really want to quit?"):
            self.closeWindow()

    def showInfo(self):
        """ Shows an Info box """
        msgbox.showinfo(
                "Info",
                "Snake clone \n"
                "Erstellt von sepplx123 \n\n"
        )

    def get_act_time(self):
        """  Returns the values of the actual time """
        return datetime.now().time()
    

    def show_text(self, text):
        mytext = '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(self.act_time.hour, self.act_time.minute, self.act_time.second,int(self.act_time.microsecond/1000)) + ' ' + text +'\n'
        self.scroll_text.insert('insert', mytext)
##############################################################################################################
##############################################################################################################
##############################################################################################################  
class Scoreboard():
    """ Create a scroeboard and saves the values in file.
        Also shows actual score information in the game window.
            points for  actions:
            level_solved = 100000
            eat_apple    = 1000
            command_sent = 100
            speed_index  = (slow=1, medium=10, fast=100, ultra=1000)
            1s passed    = 1 x speed_index
    """
    def __init__(self,spielfeld,snake,canvas,scrollbox,player_name):
        self.spielfeld = spielfeld
        self.snake = snake
        self.canvas = canvas
        self.scrollbox = scrollbox

        # total data for player saved in the db
        self.levels_solved = 0
        self.apples_eaten = 0
        self.commands_sent = 0
        self.total_time_passed = 0
        self.total_points = 0

        # data for actual level shown in the game window
        self.player_name = player_name
        self.act_level = 0
        self.time_passed = 0
        self.act_points = 0

        # other variables
        self.time_level_start = 0
        self.time_level_end = 0

        
        # database
        self.point_db = { 'level_solved': 100000,
                          'eat_apple': 1000,
                          'command_sent' : 100,
                          'speed_index_slow' : 1,
                          'speed_index_medium' : 10,
                          'speed_index_fast' : 100,
                          'speed_index_ultra' : 1000,
                         }
        
        self.scoreboard_db = {self.player_name : [self.levels_solved, self.apples_eaten, self.commands_sent,
                                                  self.total_time_passed, self.total_points]
                             }


        self.load_db_file()

        #for item in self.scoreboard_db:
        #    print('scoreboard_db:','player:',item,'stats:',self.scoreboard_db[item] )
        #print('init class Scoreboard done')


    def load_db_file(self):
        try:
            scoreboard_file = open("snake_scoreboard.txt", "r")
            liste = scoreboard_file.read().splitlines()
            scoreboard_file.close()
            if liste:
                #print('liste:', liste)
                for item in liste:
                    temp = item.split(" ")
                    #print('temp =',temp)
                    self.scoreboard_db[temp[0]] = [temp[1],temp[2],temp[3],temp[4],temp[5]]
            else:
                self.create_db_file()

        except:
            print('===> no scoreboard file found. It will be created now!')
            self.create_db_file()


    def create_db_file(self):
        #try:
            scoreboard_file = open("snake_scoreboard.txt", "w")
            print('----------------------------')
            for line in self.scoreboard_db:
                temp = self.scoreboard_db[line]
                out_line = "{0:s} {1:d} {2:d} {3:d} {4:d} {5:d}\n".format(line,temp[0],temp[1],temp[2],temp[3],temp[4])
                print("{0:s} {1:d} {2:d} {3:d} {4:d} {5:d}".format(line,temp[0],temp[1],temp[2],temp[3],temp[4]))
                #print(out_line)
                scoreboard_file.write(out_line)
            print('----------------------------')
            scoreboard_file.close()
        #except:        
            #print('===> scoreboard file could not be created!')


    def game_start(self):
        self.act_level = 1

    def next_level(self):
        self.act_level += 1
        self.act_points = 0
        self.total_points = self.total_points

    def level_summary(self):
        print('Level', self.act_level,'passed')
        print('time needed:', self.time_passed)
        print('Total Points:', self.total_points)
        print('------------------------------------------------')

    
    def calc_act_points(self,reason):
        """ reason = level_solved, eat_apple, command_sent """
        self.act_points += self.point_db[reason]        
        return self.act_points   

    def calc_time_passed(self,start,end): 
        """ calculates time in s between a start and an end point """
        self.time_passed = ((end.hour - start.hour)*3600*1000 +
                            (end.minute - start.minute)*60*1000 +
                            (end.second - start.second)*1000 +
                            (end.microsecond - start.microsecond)/1000)/1000
        return self.time_passed

    def output_level_time(self):
         """ calculates the time spent in this level """
         self.calc_time_passed(self.time_level_start, self.time_level_end)
         return self.time_passed
             
    def calc_total_points(self,speed_index):
        """ calculates total points until game over
        'speed_index_slow' : 1
        'speed_index_medium' : 2
        'speed_index_fast' : 5
        'speed_index_ultra' : 10 """
        self.total_points += self.act_points    # adds act_points for actual level
        self.total_points += (self.time_passed * self.point_db[speed_index.get()]) # adds spent time * time_multiplier
        self.act_points = self.total_points
        

    def reset(self):
        # total data for player saved in the db
        self.levels_solved = 0
        self.apples_eaten = 0
        self.commands_sent = 0
        self.total_time_passed = 0
        self.total_points = 0

        # data for actual level shown in the game window
        #self.player_name = 0
        self.act_level = 0
        self.time_passed = 0
        self.act_points = 0

        # other variables
        self.time_level_start = 0
        self.time_level_end = 0
        
        print("reset scoreboard done")
    
##############################################################################################################
##############################################################################################################
##############################################################################################################   
class Leveleditor():
    """ Create and edite levels and save/load it to a file
    """
    def __init__(self,spielfeld,snake,canvas,scrollbox):
        self.spielfeld = spielfeld
        self.snake = snake
        self.canvas = canvas
        self.scrollbox = scrollbox

        self.edit_mode = False
        
        self.show_text('init class Leveleditor done')


    def create_level(self):
        self.edit_mode = True
        self.spielfeld.create_playground()
        print('Leveleditor: Edit-mode activated. Now you can create a new level')
        

        
        

        
       
    def edit_level(self):
        self.edit_mode = True

        
        print('Leveleditor: Edit-mode activated. Now you can edit this level')

         
       
    
    def save_level(self):
        print('start saving level.......')
        print(len(self.spielfeld.spielfeld_db),self.spielfeld.spielfeld_db)
        
        liste = []
        level_name = fdialog.asksaveasfilename(defaultextension=".txt", title="save snake level")
        
        if level_name:
            level_file = open(level_name, "w")

            for i in range(self.spielfeld.rows):
                liste.append("")

            for x in range(self.spielfeld.columns):                     # column Schleife ==>> X-Koordinate
                for y in range(self.spielfeld.rows):                    # row Schleife    ==>> Y-Koordinate
                    coords = x,y
                    #self.spielfeld.spielfeld_db[coords]
                    liste[y] += (self.spielfeld.spielfeld_db[coords])

            print('------------')
            for line in liste:
                out_line = "{0:s}\n".format(line)
                print('|'+line+'|')
                #print(out_line)
                level_file.write(out_line)
            print('------------')
        
            level_file.close()
            self.spielfeld.act_level_data(command='save') # save level information in a new DB [necessary for restart!]
            self.edit_mode = False
            print('level saved to file: '+str(level_name))
        else:
            print('canceled save level!')

    def load_level(self):       
        #print('snake head:',self.spielfeld.snake_headposition ,'snake body:',self.spielfeld.snake_positions)
        #print('Class snake positions:',len(self.snake.positions),self.snake.positions)
        #print('walls:',len(self.spielfeld.wall_positions),self.spielfeld.wall_positions)
        #print('apples:',len(self.spielfeld.apple_positions),self.spielfeld.apple_positions)
        #print('exit:', len(self.spielfeld.exit_position),self.spielfeld.exit_position)
        #print('empty fields:',len(self.spielfeld.empty_fields),self.spielfeld.empty_fields)
        snake_head = False       
        level_name = fdialog.askopenfilename(defaultextension=".txt", title="load snake level")

        if level_name:
            self.spielfeld.reset()
            self.snake.reset()

            
            level_file = open(level_name, "r")
            liste = level_file.read().splitlines()
            level_file.close()
        
            print('------------')
            for y in range(len(liste)):                 # row schleife     ==>> Y-Koordinate
                print('|'+str(liste[y])+'|')
                for x in range(len(liste[y])):          # column schleife  ==>> X-Koordinate
                    coords = x, y
                    item = liste[y]
                    self.spielfeld.spielfeld_db[coords] = str(item[x])
                    #print(coords, str(item[x]))
                    
                    if item[x] == "S":
                        if snake_head == False: # the first snake item is defined as the head. all others are body
                            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='green',tags=(str(x)+'_'+str(y),'snake'))   # snake head
                            snake_head = True
                            self.spielfeld.snake_headposition = coords
                            self.snake.positions.append(coords)
                        else:
                            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='#006400',tags=(str(x)+'_'+str(y),'snake')) # snake body
                            self.spielfeld.snake_positions.append(coords)
                            self.snake.positions.append(coords)
                    elif item[x] == "W":
                        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='grey',tags=(str(x)+'_'+str(y),'wall'))
                        self.spielfeld.wall_positions.append(coords)
                    elif item[x] == "A":
                        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='red',tags=(str(x)+'_'+str(y),'apple'))
                        self.spielfeld.apple_positions.append(coords)
                    elif item[x] == "E":    # no exit allowed! will be calculated later! change back to empty field
                        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty'))
                        self.spielfeld.empty_fields.append(coords)
                        print('Exit field',coords, 'changed back to empty field!')
                    elif item[x] == " ":
                        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty'))
                        self.spielfeld.empty_fields.append(coords)
                        
            print('------------')
            #print('snake head:',self.spielfeld.snake_headposition ,'snake body:',self.spielfeld.snake_positions)
            #print('Class snake positions:',len(self.snake.positions),self.snake.positions)
            #print('walls:',len(self.spielfeld.wall_positions),self.spielfeld.wall_positions)
            #print('apples:',len(self.spielfeld.apple_positions),self.spielfeld.apple_positions)
            #print('exit:', len(self.spielfeld.exit_position),self.spielfeld.exit_position)
            #print('empty fields:',len(self.spielfeld.empty_fields),self.spielfeld.empty_fields)
            #print('level loaded from file:'+str(level_name))

            self.spielfeld.act_level_data(command='save') # save level information in a new DB [necessary for restart!]
            self.edit_mode = False
        else:
            print('canceled load level!')
        

            
    def show_text(self, text):
        self.act_time = datetime.now().time()
        mytext = '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(self.act_time.hour, self.act_time.minute, self.act_time.second,int(self.act_time.microsecond/1000)) + ' ' + text +'\n'
        self.scrollbox.insert('insert', mytext) 
        
##############################################################################################################
##############################################################################################################
##############################################################################################################   
class Spielsteuerung():
    """ Spielablauf und Collisionsauswertung.
    UI ==> spielsteuerung ==> spielfeld ==> Snake
    """
    def __init__(self,snake,spielfeld,leveleditor,scoreboard,canvas,scrollbox,speed_index):
        self.snake = snake
        self.spielfeld = spielfeld
        self.leveleditor =leveleditor
        self.scoreboard = scoreboard
        self.canvas = canvas
        self.scrollbox = scrollbox
        self.speed_index = speed_index
        
        self.snakedirection = (0, 0)
        self.no_collision = 1
        self.collision = -1
        self.eat_apple = -2
        self.pass_exit = -3
        self.empty_field = []

        self.new_snake_headposition = ()
        self.game_status = 0
        self.game_start = False
        self.game_running = False
        self.game_end = False
        self.game_paused = False
        self.commands = []
        self.keysym = ""
        self.level_passed = False
        self.show_text('init class Spielsteuerung done')


    def keyevent(self,keysym):      
        self.keysym = keysym
        #print('key detected:', self.keysym)
        
        value = (0, 0)
        
        if self.keysym == 'p' and self.game_running == True:    # pause the game
            #print('==> game paused')
            self.show_text('==> game paused...')
            self.commands = []                                  # clear the command queue
            self.snakedirection = (0, 0)                        # Stop the snake movement
            self.game_running = False                           # game_running = False
            self.game_paused = True
        
        if self.keysym == 'Left':
            value = (-1, 0)
        elif self.keysym == 'Right':
            value = (+1, 0)          
        elif self.keysym == 'Up':
            value = (0, -1)
        elif self.keysym == 'Down': 
            value = (0, +1)
        
        if value != (0, 0):
            self.commands.append(value) # add commant to the queue
        #print(self.commands)

    def do_game_start_stop(self):
        #print(datetime.now().time(),'|game_end:',self.game_end,'|start:',self.game_start,'|running:',self.game_running,'|paused:',self.game_paused,'|edit_mode:',self.leveleditor.edit_mode)
        #print(datetime.now().time(),'Loop_Start' ,'direction=',self.snakedirection,'commands=', self.commands, 'snake body:',self.spielfeld.snake_positions)

        #Step 1: check if game not over           
        if not self.game_end:
            # command queue for snake directions
            while self.commands:                                
                #print(datetime.now().time(),'Loop_Start' ,'direction=',self.snakedirection,'commands=', self.commands, 'snake body:',self.spielfeld.snake_positions)
                actx, acty = self.snakedirection                # take actual snake direction            
                newx, newy = self.commands.pop(0)               # get the value and delete the item from the list
                if (newx, newy) == self.snakedirection:         # if new direction is the same, pick next item from queue
                    print('_____________________ same direction removed from queue')
                    continue
                elif (actx+newx, acty+newy) == (0, 0):          # lock 180° turns
                    print('_____________________ 180 degree turn blocked')
                    continue
                else:
                    self.snakedirection = (newx, newy)          # command taken from list
                    self.scoreboard.calc_act_points(reason = "command_sent")
                    break

            if self.snakedirection != (0, 0) and not self.game_start:
                self.game_start = True
                self.scoreboard.time_level_start = datetime.now().time()
                #print('==> game starts...')
                self.show_text('==> game starts...')

            if  self.game_start and self.snakedirection != (0, 0) and not self.game_paused :
                self.game_running = True
            elif self.game_start and self.snakedirection != (0, 0) and self.game_paused:
                self.game_running = True
                self.game_paused = False
                self.show_text('==> game continues...')
                #print('==> game continues')
            if self.game_start:                         # reset Leveleditor Edit-mode
                self.leveleditor.edit_mode = False

        #Step 2: check if game running ===> call game_loop
        if self.game_running:
            self.game_loop()
        
          
    def game_loop(self):
        #print(datetime.now().time(),'game_loop start:')
        self.new_snake_headposition = self.snake.move(self.snakedirection)    #get the new headposition       
        #print('snake wants to moves to field:',self.new_snake_headposition)

        #Step3: check collision and create game status       
        self.game_status = self.collision_detection()
        #print('self.game_status', self.game_status)

        #Step4: evaluate the game status and update the playground, database and items
            
        # 4.1 no collision ==> update snake & apples
        if self.game_status == self.no_collision:
            self.empty_field = self.snake.update_position()
            #print('empty field=',self.empty_field,'snake=',self.snake.positions)
            self.spielfeld.update_screen(self.new_snake_headposition, self.empty_field, eat_apple=False) 
                
        # 4.2 collision detected! ==> game over!               
        elif self.game_status == self.collision:
            self.game_over()
            
        # 4.3 eat apple ==> snake grows                
        elif self.game_status == self.eat_apple:
            self.snake.eat_apple()
            self.empty_field = self.snake.update_position()
            #print('empty field=',self.empty_field)
            self.spielfeld.update_screen(self.new_snake_headposition, self.empty_field, eat_apple=True)
            self.game_status = self.no_collision
            self.scoreboard.calc_act_points(reason = "eat_apple")
            
        # 4.4 exit found ==> game win!               
        elif self.game_status == self.pass_exit:
            self.game_win()
        
        #print(datetime.now().time(),'Loop_End' ,'direction=',self.snakedirection,'commands=', self.commands)
            
    def collision_detection(self):
        if self.new_snake_headposition in self.spielfeld.snake_positions:
            #print('snake body:',self.spielfeld.snake_positions)
            #print('_______self collision!!!!!','head:',head_position,'item_index:',self.spielfeld.snake_positions.index(head_position))
            #print('_______snake_body:',self.spielfeld.snake_positions)
            self.show_text('==> self collision! head'+str(self.new_snake_headposition)+' collides with body item_index['+str(self.spielfeld.snake_positions.index(self.new_snake_headposition))+']')
            #self.show_text('snake_body:'+str(self.spielfeld.snake_positions))
            return self.collision
        elif self.new_snake_headposition in self.spielfeld.wall_positions:
            #print('_______wall collision!!!!!','head:',head_position,'item_index:',self.spielfeld.wall_positions.index(head_position))                  
            #print('_______walls:',self.spielfeld.wall_positions)
            self.show_text('==> wall collision!!! head'+str(self.new_snake_headposition)+' collides with wall item_index['+str(self.spielfeld.wall_positions.index(self.new_snake_headposition))+']')
            #self.show_text('walls:'+str(self.spielfeld.wall_positions))
            return self.collision
        elif self.new_snake_headposition in self.spielfeld.apple_positions:
            #print('_______>>>>>>>>> eat apple! Snake grows ['+str(self.snake.apple_grow)+']')
            #self.show_text('==>> eat apple! Snake grows [+'+str(self.snake.apple_grow)+']')
            return self.eat_apple
        elif self.new_snake_headposition in self.spielfeld.exit_position:
            return self.pass_exit
        else:
            return self.no_collision

    def new_game(self):
        self.reset()
        self.spielfeld.load_next_level()        # create a new game and DB
        self.new_snake_headposition = self.snake.headposition
        self.game_status = self.no_collision
        self.scoreboard.reset()
        self.scoreboard.game_start()

    def restart_level(self):
        self.reset()
        self.scoreboard.reset()
        self.spielfeld.restart()                # load game data back from DB and restart from the beginning
        self.new_snake_headposition = self.snake.headposition
        self.game_status = self.no_collision
        
    def game_over(self):
        self.game_running = False
        self.game_start = False
        self.game_end = True
        self.level_passed = False
        self.commands = []
        self.show_text('==> Game Over!')
        self.spielfeld.reason_game_over(self.new_snake_headposition)
        #self.spielfeld.show_status()

        self.scoreboard.time_level_end = datetime.now().time()
        self.scoreboard.output_level_time()
        self.scoreboard.calc_total_points(speed_index=self.speed_index)
        print('self.game_end =',self.game_end,' self.level_passed=',self.level_passed)

    def game_win(self):
        self.game_running = False
        self.game_start = False
        self.game_end = True
        self.level_passed = True
        self.commands = []
        self.show_text('==> You win!')
        #self.spielfeld.show_status()

        self.scoreboard.time_level_end = datetime.now().time()
        self.scoreboard.output_level_time()
        self.scoreboard.calc_act_points(reason = "level_solved")
        self.scoreboard.calc_total_points(speed_index=self.speed_index)


    def reset(self):
        self.snakedirection = (0, 0)
        self.no_collision = 1
        self.game_status = self.no_collision
        self.game_start = False
        self.game_running = False
        self.game_end = False
        self.level_passed = False
        self.commands = []
        
        self.snake.reset()
        self.spielfeld.reset()
        self.spielfeld.create_playground()
        self.scoreboard.reset()
        self.show_text('reset spielsteuerung done')
        print("reset spielsteuerung")

    def show_text(self, text):
        self.act_time = datetime.now().time()
        mytext = '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(self.act_time.hour, self.act_time.minute, self.act_time.second,int(self.act_time.microsecond/1000)) + ' ' + text +'\n'
        self.scrollbox.insert('insert', mytext) 
##############################################################################################################
##############################################################################################################
##############################################################################################################   
class Snake():
    def __init__(self,spielfeld_rows,spielfeld_columns,scrollbox):
        """
        init erstellt die Schlange.
        Zu Begin hat die Schlange eine Länge von 4 Kästchen
        Startpunkt liegt bei x=5, y=48
        Der Kopf ist oben also bei x=5 y=45
        """
        self.spielfeld_rows = spielfeld_rows
        self.spielfeld_columns = spielfeld_columns
        self.scrollbox = scrollbox
        
        self.start_x = 2
        self.start_y = self.spielfeld_columns - 1
        self.length = 4
        self.apple_grow = 4        
        self.direction = []             # Bewegungsrichtung der Schlange in X,Y Koords
        self.headposition = []          # Schlangenkopf in X,Y Koords
        self.positions = []             # Dimension der Schlange in X,Y Koords
        self.growing = 0
        self.growing_size = 0
        self.show_text('init class Snake done')
        

    def create(self):
        self.positions = []
        for i in range(1,self.length+1):
            coords = (self.start_x, self.start_y-(self.length-i))
            self.positions.append(coords)
        self.headposition = self.positions[0]     # Schlangenkopf ist immer das erste Element der Liste(ganz oben)
        #print('snake head:',self.headposition,' body', self.positions[1:])
        return self.headposition, self.positions[1:]

 
    def move(self,direction):
        self.direction = direction
        self.headposition = self.positions[0]

        x, y = self.headposition                            # Alte Kopfposition in temp. Variable speichern
        dx, dy = self.direction                             # Richtung auslesen und in temp. Variable speichern
        newheadx = x + dx                                   # Neue Kopfposition = alte + Richtung
        newheady = y + dy                                   # Neue Kopfposition = alte + Richtung
        
        if newheadx < 0:                                    # Korrektur um von links nach Rechts durch den Rand zu fahren oder oben/unten
            newheadx = self.spielfeld_columns-1      
        if newheadx > self.spielfeld_columns-1:
            newheadx = 0
        if newheady < 0:
            newheady = self.spielfeld_rows-1      
        if newheady > self.spielfeld_rows-1:    
            newheady = 0        

        self.headposition = (newheadx, newheady)                # Neue Kopfposition = alte Position + Richtung
        #print('Snake moves', self.direction, 'Neue Kopfposition =', self.headposition, 'self.positions =',self.positions)
        #return self.positions   # Kopf ist erstes Element der Liste
        return self.headposition   # Return Kopfposition

    def update_position(self):       
        self.positions.insert(0, self.headposition)             # Neue Kopfposition als erstes Element einfügen        
        if not self.growing:
            empty_field = self.positions[-1]                    # Frei gewordenes Element zwischenspeichern
            self.positions.pop()                                # Letztes Element entfernen
        else:
            self.growing -= 1
            empty_field = None

            #print('_________________snake grows_____['+str(self.growing_size-self.growing)+'/'+ str(self.growing_size)+']')
            #self.show_text('snake grows_['+str(self.growing_size-self.growing)+'/'+ str(self.growing_size)+']')
            if self.growing == 0:
                self.growing_size = 0
        return empty_field
        
    def eat_apple(self):
        self.growing_size += self.apple_grow
        self.growing += self.apple_grow

    def tell_position(self):
        return self.positions[1:]   # return only the body without the head

    def show_text(self, text):
        self.act_time = datetime.now().time()
        mytext = '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(self.act_time.hour, self.act_time.minute, self.act_time.second,int(self.act_time.microsecond/1000)) + ' ' + text +'\n'
        self.scrollbox.insert('insert', mytext) 

    def reset(self):
        self.direction = []             # Bewegungsrichtung der Schlange in X,Y Koords
        self.headposition = []          # Schlangenkopf in X,Y Koords
        self.positions = []             # Dimension der Schlange in X,Y Koords
        self.growing = 0
        self.growing_size = 0

        self.show_text('reset Snake done')
        print("reset snake done")

##############################################################################################################
##############################################################################################################
##############################################################################################################

class Spielfeld(): 
    def __init__(self,canvas,snake,spielfeld_rows,spielfeld_columns,spielfeld_itemwidth,spielfeld_itemheight,scrollbox):
        """
        init Spielfeld als schwarze Boxen      
        self.spielfeld0_0 = tk.Canvas(self.mainWindow, width=50, height=50, highlightthickness=1, background="black")
        self.spielfeld0_0.grid(row=0,column=0, sticky='nesw')

        item = self.canvas.create_rectangle(x*self.itemwidth,y*self.itemheight,self.itemwidth*(x+1),self.itemheight*(y+1), fill="black", outline='grey' ,tags=str(x)+'_'+str(y))
        self.canvas.itemconfigure('9_0', fill='blue')
        self.canvas.itemconfigure('0_9', fill='red')          
        """
        self.canvas = canvas
        self.snake = snake
        self.rows = spielfeld_rows        
        self.columns = spielfeld_columns
        self.itemwidth = spielfeld_itemwidth
        self.itemheight = spielfeld_itemheight
        self.scrollbox = scrollbox

        self.apples_amount = 5
        self.walls_amount = 5

        self.spielfeld_db = {}         
        self.empty_fields = []
        self.apple_positions = []
        self.exit_position = []
        self.wall_positions = []
        self.snake_positions = []
        self.snake_headposition = []
        self.new_empty_field = []
        self.act_spielfeld_db = {}


        self.create_playground()
        self.show_text('init class Spielfeld done')

    def create_playground(self):
        # create an empty playground                                X,Y-Koordinanten-Paare erzeugen und in dem dict fuers Spielfeld als leere Felder anlegen 
        self.spielfeld_db = {}
        self.empty_fields = []
        for x in range(self.columns):                               # column Schleife ==>> X-Koordinate
            for y in range(self.rows):                              # row Schleife    ==>> Y-Koordinate
                coords = x,y
                self.spielfeld_db[coords] = " "
                item = self.canvas.create_rectangle(x*self.itemwidth,y*self.itemheight,self.itemwidth*(x+1),self.itemheight*(y+1), fill="black", outline='white' ,tags=(str(x)+'_'+str(y),'empty'))
        #print(self.spielfeld_db)

        for item in self.spielfeld_db:                               # gehe jedes Item der Spielfeld-DB durch
            if self.spielfeld_db[item] == " ":                       # pruefe auf leere Felder
                self.empty_fields.append(item)                       # Erstelle eine Liste mit Koordinatenpaare der leeren Felder
        #print(self.empty_fields)
        #print('____init empty_fields:',len(self.empty_fields))        

    def create_world(self):                  
        #Create snake
        self.snake_headposition, self.snake_positions = self.snake.create()
        del_position = self.empty_fields.index(self.snake_headposition)
        del self.empty_fields[del_position]                     # Lösche das Element aus der Liste der freien Felder 
        self.spielfeld_db[self.snake_headposition] = "S"        # Eintrag in die DB als Snake
        x,y = self.snake_headposition
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='green',tags=(str(x)+'_'+str(y),'snake')) #change the color according to the defined         
            
        for i in range(len(self.snake_positions)):
            #print(self.snake_positions[i], 'position:',self.empty_fields.index(self.snake_positions[i]))
            del_position = self.empty_fields.index(self.snake_positions[i])
            del self.empty_fields[del_position]                     # Lösche das ELement aus der Liste der freien Felder 
            self.spielfeld_db[self.snake_positions[i]] = "S"        # Eintrag in die DB als Snake
            x,y = self.snake_positions[i]
            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='#006400',tags=(str(x)+'_'+str(y),'snake')) #change the color according to the defined   
        #print('snake_positions:',self.snake_positions)
        #print('____create snake:',self.snake_headposition,self.snake_positions,'len empty fields=', len(self.empty_fields)) 
            
        #Create walls
        #print('____create walls:',self.walls_amount,'len empty fields=', len(self.empty_fields))    
        for i in range(self.walls_amount):                           # Generiere die geforderte Anzahl walls
            item = randint(0, len(self.empty_fields)-1)                # Picke random ein element aus den leeren Spielfeldern heraus
            #print('randint=',item,'len empty fields=', len(self.empty_fields))
            self.wall_positions.append(self.empty_fields[item])      # fuege dieses Element zur Liste der walls hinzu
            del self.empty_fields[item]                              # Lösche das ELement aus der Liste der freien Felder 
            self.spielfeld_db[self.wall_positions[i]] = "W"          # Eintrag in die DB als Wall
            x,y = self.wall_positions[i]
            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='grey',tags=(str(x)+'_'+str(y),'wall')) #change the color according to the defined
        #print('wall_positions:',self.wall_positions)
            
        #Create apples
        #print('____create apples:',self.apples_amount,'len empty fields=', len(self.empty_fields))            
        for i in range(self.apples_amount):                          # Generiere die geforderte Anzahl Aepfel
            item = randint(0, len(self.empty_fields)-1)                # Picke random ein element aus den leeren Spielfeldern heraus
            #print('randint=',item,'len empty fields=', len(self.empty_fields))            
            self.apple_positions.append(self.empty_fields[item])     # füge dieses Element zur Liste der Apples hinzu
            del self.empty_fields[item]                              # Lösche das ELement aus der Liste der freien Felder 
            self.spielfeld_db[self.apple_positions[i]] = "A"         # Eintrag in die DB als Apple
            x,y = self.apple_positions[i]
            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='red',tags=(str(x)+'_'+str(y),'apple')) #change the color according to the defined 
        #print('apple_positions:',self.apple_positions)

        self.show_text('world created')

    def update_screen(self,snake_headposition, new_empty_field, eat_apple):
        self.snake_headposition = snake_headposition
        self.new_empty_field = new_empty_field

        if eat_apple == True:                                   # update the apple positions and remove the eaten one
            del_position = self.apple_positions.index(self.snake_headposition)
            del self.apple_positions[del_position]             
            #print('___________apple removed:', self.snake_headposition,'______left apples:',self.apple_positions)
            
        self.snake_positions = self.snake.tell_position()            # update the snake headposition        
        self.spielfeld_db[self.snake_headposition] = "S"        # Eintrag in die DB als Snake
        x,y = self.snake_headposition
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='green',tags=(str(x)+'_'+str(y),'snake')) #change the color according to the defined
        x,y = self.snake_positions[0]
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='#006400',tags=(str(x)+'_'+str(y),'snake')) #change the color of the 2nd snake items
        #print('snake_head:',self.snake_headposition,'body:',self.snake_positions)

        if self.new_empty_field != None:                        # If there is a empty field for color change (Not eat apple or not grow)
            self.spielfeld_db[self.new_empty_field] = " "        # Eintrag in die DB als empty
            x,y = self.new_empty_field
            self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty')) #change the color according to the defined

        if len(self.apple_positions) == 0 and len(self.exit_position) == 0:  #Wenn keine Apples mehr da sind, erstelle den Ausgang nur 1mal
            self.create_exit()

    def update_spielfeld_dict(self,item,snake_head):
        
        if item in self.snake_positions:
            self.spielfeld_db[item] = "S"
            if snake_head:
                self.snake_headposition = item
        if item in self.wall_positions:
            self.spielfeld_db[item] = "W"
        if item in self.apple_positions:
            self.spielfeld_db[item] = "A"
        if item in self.exit_position:
            self.spielfeld_db[item] = "E"
        if item in self.empty_fields:
            self.spielfeld_db[item] = " "
        print('==>>> item:', item, 'changed to item_type:',self.spielfeld_db[item])
            

    def edit_mode(self,coords,next_item_mode):
        snake_head = False
        
        #print('snake head:',self.snake_headposition ,'snake body:',self.snake_positions)
        #print('Class snake positions:',len(self.snake.positions),self.snake.positions)
        #print('walls:',len(self.wall_positions),self.wall_positions)
        #print('apples:',len(self.apple_positions),self.apple_positions)
        #print('exit:', len(self.exit_position),self.exit_position)
        #print('empty fields:',len(self.empty_fields),self.empty_fields)
        
        self.item_rotation = {"S":[self.snake_positions,"self.snake_positions",2,"#006400","snake"],
                              "W":[self.wall_positions,"self.wall_positions",1,"grey","wall"],
                              "A":[self.apple_positions,"self.apple_positions",3,"red","apple"],
                              " ":[self.empty_fields,"self.empty_fields",0,"black","emtpy"],
                              "E":[self.exit_position,"self.exit_position",-1,"blue","exit"]
                              }
        
        x = coords[0] // self.itemwidth
        y = coords[1] // self.itemheight
        item = (x, y)
        
            
        temp = self.item_rotation[self.spielfeld_db[item]]  # selects the item data list
        db = temp[0]
        db_name = temp[1]
        db_index =temp[2]
        color = temp[3]
        tagname = temp[4]        

        try:
            index = db.index(item)
            #print('| field:',item, '| item_type:', self.spielfeld_db[item],'| found in:',db_name,'| item_index:', index, '| color=', color,'|')
            del db[db.index(item)]                          # delete item from specific DB
            #print('| field:',item, '| removed from:', db_name,'| item_index:', index,'|')
        except ValueError:
            pass
            #print('| field:',item, '| item_type:', self.spielfeld_db[item])
            #print('==>>> item has no index! Could not be removed from db')

        next_item = db_index + next_item_mode
        if next_item > 3:
            next_item = 0
        elif next_item < 0:
            next_item = 3
            
        for element in self.item_rotation.values():
            if next_item == element[2]:
                db = element[0]
                db_name = element[1]
                db_index = element[2]
                color = element[3]
                tagname = element[4]
                
        
        if db_index == 2 and len(db) == 0:        # Sneak head will be created, if no other snake item exist on the field.
            snake_head = True
            color = 'green'
            
        db.append(item)                                     # add item to the new DB
        index = db.index(item)
        #print('| field:',item, '| saved in:', db_name,'| item_index:', index,'|')
        
        self.update_spielfeld_dict(item,snake_head)     # also add item to dict

        self.canvas.itemconfigure(str(x)+'_'+str(y), fill=color, tags=(str(x)+'_'+str(y),tagname))

        #print('check if operation was succesful...')
        temp = self.item_rotation[self.spielfeld_db[item]]  # selects the item data list
        db = temp[0]
        index = db.index(item)
        db_name = temp[1]
        db_index =temp[2]
        color = temp[3]
        tagname = temp[4]
        #print('| field:',item,'| item_type:',self.spielfeld_db[item],'| found in:',db_name,'| item_index:',index,'| color=',color,'|')
        #print('self.spielfeld_db:',len(self.spielfeld_db),self.spielfeld_db)

    def create_exit(self):
        self.empty_fields = []
        for item in self.spielfeld_db:                               # gehe jedes Item der Spielfeld-DB durch
            if self.spielfeld_db[item] == " ":                       # pruefe auf leere Felder
                self.empty_fields.append(item)                       # Erstelle eine Liste mit Koordinatenpaare der leeren Felder
        
        item = randint(0, len(self.empty_fields)-1)                 # Picke random ein element aus den leeren Spielfeldern heraus 
        self.exit_position.append(self.empty_fields[item])          # füge dieses Element zur Liste der Exit-Positionen hinzu
        del self.empty_fields[item]                                 # Lösche das Element aus der Liste der freien Felder
        self.spielfeld_db[self.exit_position[0]] = "E"              # Eintrag in die DB als Exit
        x,y = self.exit_position[0]      
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='blue',tags=(str(x)+'_'+str(y),'exit')) #change the color according to the defined


    def show_status(self):
        temp = []  
        for element in self.spielfeld_db:
            if self.spielfeld_db[element] == 'S':
                temp.append(element)
        print('____Snake:',len(temp),temp )
        print('____Snake:',len(self.snake_positions) , self.snake_positions)
        for element in temp:
            if element not in self.snake_positions:
                print('____Differenz_Element:',element)
        temp = []
        for element in self.spielfeld_db:        
            if self.spielfeld_db[element] == 'E':
                temp.append(element)
        print('____Exit:',len(temp),temp )
        print('____Exit:',len(self.exit_position) , self.exit_position)
        temp = []
        for element in self.spielfeld_db:        
            if self.spielfeld_db[element] == 'A':
                temp.append(element)
        print('____Apples:',len(temp),temp )
        print('____Apples:',len(self.apple_positions) , self.apple_positions)
        temp = []                            
        for element in self.spielfeld_db:        
            if self.spielfeld_db[element] == 'W':
                 temp.append(element)
        print('____Walls:',len(temp),temp )
        print('____Walls:',len(self.wall_positions) , self.wall_positions)                      


    def reason_game_over(self,position):
        reason = ""
        if self.spielfeld_db[position] == 'S':
            reason = "snake body"
        elif self.spielfeld_db[position] == 'W':
            reason = "wall"
        elif self.spielfeld_db[position] == 'A':
            reason = "apple"
        elif self.spielfeld_db[position] == 'E':
            reason = "exit"
        elif self.spielfeld_db[position] == ' ':
            reason = "empty field"
        print('reason for game over ==> field:'+str(position)+' | item_type: '+reason)
         
    def act_level_data(self,command):
        if command == "save":
            self.act_spielfeld_db = self.spielfeld_db.copy()
        if command == "load":
            return self.act_spielfeld_db
         
    def load_next_level(self):
        self.create_playground()
        self.create_world()
        self.act_level_data(command='save') # save level information in a new DB

    def fill_itemtype_db(self,database):
        for item in database:
            x,y = item
            if database[item] == "S":  
                    self.snake.positions.append(item)   # snake body
                    self.canvas.itemconfigure(str(x)+'_'+str(y), fill='#006400',tags=(str(x)+'_'+str(y),'snake')) #change the color according to the defined
            elif database[item] == "W":
                self.wall_positions.append(item)
                self.canvas.itemconfigure(str(x)+'_'+str(y), fill='grey',tags=(str(x)+'_'+str(y),'wall')) #change the color according to the defined
            elif database[item] == "A":
                self.apple_positions.append(item)
                self.canvas.itemconfigure(str(x)+'_'+str(y), fill='red',tags=(str(x)+'_'+str(y),'apple')) #change the color according to the defined
            elif database[item] == "E":    # no exit allowed! Exit will be calculated later! change back to empty field
                self.empty_fields.append(item)
                self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty')) #change the color according to the defined
                print('Exit field',item, 'changed back to empty field!')
            elif database[item] == " ":
                self.empty_fields.append(item)
                self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty')) #change the color according to the defined

        #snake head is the first snake item!  all others are body. So sort the list first
        self.snake.positions.sort()
        self.snake_positions = self.snake.positions[:]
        self.snake_headposition = self.snake_positions.pop(0)
        x, y = self.snake_headposition
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='green',tags=(str(x)+'_'+str(y),'snake')) #change the color according to the defined

        #print('snake head:',self.snake_headposition ,'snake body:',self.snake_positions)
        #print('Class snake positions:',len(self.snake.positions),self.snake.positions)
        #print('walls:',len(self.wall_positions),self.wall_positions)
        #print('apples:',len(self.apple_positions),self.apple_positions)
        #print('exit:', len(self.exit_position),self.exit_position)
        #print('empty fields:',len(self.empty_fields),self.empty_fields)


        
    def restart(self):
        self.reset()
        
        #print('load items from db:.....',len(self.act_spielfeld_db),self.act_spielfeld_db)
        self.spielfeld_db = self.act_level_data(command='load').copy()  # load the level information back to the dict
        #print('values loaded:.....',len(self.spielfeld_db),self.spielfeld_db)
        if self.spielfeld_db:
            self.fill_itemtype_db(database=self.spielfeld_db)                        # extract values to specific item_type lists
            #print('spielfeld reload done')
        else:
            print('no data alavailable. You need to start a new game!')

    def reset(self):
        self.exit_position = []
        self.new_empty_field = []
        
        self.spielfeld_db = {}         
        self.empty_fields = []
        self.apple_positions = []
        self.wall_positions = []
        self.snake_positions = []
        self.snake_headposition = []
        print('reset spielfeld done')
    
    def show_text(self, text):
        self.act_time = datetime.now().time()
        mytext = '{0:02d}:{1:02d}:{2:02d}:{3:03d}'.format(self.act_time.hour, self.act_time.minute, self.act_time.second,int(self.act_time.microsecond/1000)) + ' ' + text +'\n'
        self.scrollbox.insert('insert', mytext) 
    
##############################################################################################################
##############################################################################################################
##############################################################################################################
    
def main():
    root = tk.Tk()
    root.title("Snake Game V0.1")
    #root.geometry('800x800')
    gameui = GUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
