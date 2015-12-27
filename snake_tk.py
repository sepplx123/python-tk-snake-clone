# !/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from random import randint
from datetime import datetime

# Fix for Python 2.x/3.x
try:
    import Tkinter as tk
    import tkMessageBox as msgbox    
    import ScrolledText as tkst
    
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
        self.strv_cycletime.set('00:00:00')

        # festlegen der sonstigen Optionen wie Titel, Geometry, etc.
        self.master.configure(background='black')
        #self.master.title("Snake Game V0.1")
        #self.master.geometry('600x600')

        # FRAMES
        self.fr1 = tk.Frame(self.master, width=0, height=20, background='grey')
        self.fr2 = tk.Frame(self.master,width=200, height=200, background='yellow')
        self.fr3 = tk.Frame(self.master, width=0, height=20, background='grey')
        self.fr1.pack(expand=1,fill='both')
        self.fr2.pack(fill='none',expand=0, side='top',anchor='center')
        self.fr3.pack(expand=1,fill='both')        

        # Canvas
        self.canvas = tk.Canvas(self.fr2, width=500, height=500,
                                highlightthickness=1, background='white')
        self.canvas.grid(row=2,column=2,sticky='nesw')

        # BUTTONS
        bQuit = tk.Button(self.fr3, text="Quit", width=8, height=1, command=self.closeWindow)        # Button Quit/Exit
        bCreateWorld = tk.Button(self.fr3, text="load new Level",width=0, height=1, command=None)    # Button Create World
        bCreateSnake = tk.Button(self.fr3, text="restart",width=0, height=1, command=None)           # Button paint Snake        
        #bCreateWorld.pack(side="left", padx=10, pady=1,anchor='s')
        #bCreateSnake.pack(side="left", padx=10, pady=1,anchor='s')       
        #bQuit.pack(side="right", padx=10, pady=1, anchor='s')        

        #Scrolled Textbox
        self.scroll_text = tkst.ScrolledText( self.fr3, width=0, height=10, wrap="word", fg='blue',)
        self.scroll_text.pack(fill='both',expand=1, side='bottom',anchor='s')
        #mytext = 'TESTTTTTT \n'
        #self.scroll_text.insert('insert', mytext)

        # Labels
        self.label_uhrzeit = tk.Label(self.fr1, textvariable=self.strv_zeitangabe,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 20))
        self.label_uhrzeit.pack(side="left", padx=10, pady=1,anchor='n')    
        self.label_cycletime = tk.Label(self.fr1, textvariable=self.strv_cycletime,
                                      bg='black', fg='#00bfff', width=0, height=0, font=("Arial", 20))
        self.label_cycletime.pack(side="right", padx=10, pady=1,anchor='n')  



        # Class calls
        self.snake = Snake(self.spielfeld_rows,self.spielfeld_columns,self.scroll_text)
        self.spielfeld = Spielfeld(self.canvas,self.snake,self.spielfeld_rows,self.spielfeld_columns,
                                   self.spielfeld_itemwidth,self.spielfeld_itemheight,scrollbox=self.scroll_text)
        self.spielsteuerung = Spielsteuerung(self.snake,self.spielfeld,canvas=self.canvas,scrollbox=self.scroll_text)
        self.leveleditor = Leveleditor(spielfeld=self.spielfeld,snake=self.snake,spielsteuerung=self.spielsteuerung,canvas=self.canvas,scrollbox=self.scroll_text)

        self.create_keybindings()       # Funktion Keybindsings aufrufen


        # Menubar "Datei"-Menue
        self.menubar = tk.Menu(self.master)
        
        # "File"-Menue
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Game", menu=self.filemenu)
        self.filemenu.add_command(label="new game",
                                  command=self.spielsteuerung.new_game)       
        self.filemenu.add_command(label="reset",
                                  command=self.spielsteuerung.reset)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Game exit",
                                  command=self.closeWindow)
        
        # "Leveleditor"-Menue
        self.l_editor = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Level Editor", menu=self.l_editor) 
        self.l_editor.add_command(label="create level", command=self.leveleditor.create_level)
        self.l_editor.add_command(label="edit level", command=self.leveleditor.edit_level)
        self.l_editor.add_command(label="save level", command=self.leveleditor.save_level)
        self.l_editor.add_command(label="load level", command=self.leveleditor.load_level)       

        # "Hilfe"-Menue
        self.infomenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Info", menu=self.infomenu)        
        self.infomenu.add_command(label="About", command=self.showInfo)
        
        self.master.config(menu=self.menubar)

        
        self.main_loop()                # start mainloop
        #print(self.act_time, 'init class GUI done')
        
        self.show_text('init class GUI done')
        #################               Init class GUI beendet
    


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
        
        # Step: call game handler game_loop
        if time_delta >= 500:
            self.strv_cycletime.set(str(int(time_delta))+' ms')
            self.time_last_cycle = self.act_time
            
            self.spielsteuerung.game_loop()
            

        # Step5: start the loop again
        self.master.after(self.cycle_time, self.main_loop)  # mainloop



        # KEY-BINDINGS / EVENTS
    def create_keybindings(self):
        self.master.bind("<Left>", self.keyfunctions)
        self.master.bind("<Right>", self.keyfunctions)        
        self.master.bind("<Up>", self.keyfunctions)
        self.master.bind("<Down>", self.keyfunctions)
        self.master.bind("<p>", self.keyfunctions)
        self.master.bind("<Escape>", self.closeWindow)
        self.show_text('keybindings created')

        # Funktionsauswertung der Tastendrücke
    def keyfunctions(self,event):
        self.event = event
        #print(self.act_time, "Tastendruck =", self.event.keysym)
        self.spielsteuerung.keyevent(self.event.keysym)

               
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
class Leveleditor():
    """ Create and edite levels and save/load it to a file
    """
    def __init__(self,spielfeld,snake,spielsteuerung,canvas,scrollbox):
        self.spielfeld = spielfeld
        self.snake = snake
        self.spielsteuerung = spielsteuerung
        self.canvas = canvas
        self.scrollbox = scrollbox


        
        self.show_text('init class Leveleditor done')

    def reset_all(self):
        self.spielsteuerung.reset()
        #self.spielfeld.reset()
        #self.snake.reset()

    def create_level(self):
        print('create_level')

        
       
    def edit_level(self):
         print('edit_level')

         
       
    
    def save_level(self):
        liste = []
        for i in range(self.spielfeld.rows):
            liste.append("")

        for x in range(self.spielfeld.columns):                     # column Schleife ==>> X-Koordinate
            for y in range(self.spielfeld.rows):                    # row Schleife    ==>> Y-Koordinate
                coords = x,y
                #self.spielfeld.spielfeld_db[coords]
                liste[y] += (self.spielfeld.spielfeld_db[coords])

        fobj_out = open("snake_level.txt", "w")
        print('------------')
        for line in liste:
            out_line = "{0:s}\n".format(line)
            fobj_out.write(out_line)
            print('|'+line+'|')
            #print(out_line)
        fobj_out.close()
        print('------------')
        print('level saved! filename: snake_level.txt')

    def load_level(self):       
        self.reset_all()

        snake_head = False
        fobj_in = open("snake_level.txt", "r")
        liste = fobj_in.read().splitlines()
        fobj_in.close()
        print('------------')
        for i in range(len(liste)):
            print('|'+str(liste[i])+'|')
        print('------------')
            

        for y in range(len(liste)):                 # row schleife     ==>> Y-Koordinate
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
                else:
                    self.canvas.itemconfigure(str(x)+'_'+str(y), fill='black',tags=(str(x)+'_'+str(y),'empty'))
                    self.spielfeld.empty_fields.append(coords)

                
        #print('snake head:',self.spielfeld.snake_headposition ,'snake body:',self.spielfeld.snake_positions)
        #print('Class snake positions:',self.snake.positions)
        #print('walls:',self.spielfeld.wall_positions)
        #print('apples:',self.spielfeld.apple_positions)
        #print('exit:', self.spielfeld.exit_position)
        print('level loaded from file: snake_level.txt')

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
    def __init__(self,snake,spielfeld,canvas,scrollbox):
        self.snake = snake
        self.spielfeld = spielfeld
        self.canvas = canvas
        self.scrollbox = scrollbox
        
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
        
        
          
    def game_loop(self):
        
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
                self.snakedirection = (newx, newy)
                break

        
        
        #Step 1: check if game not over           
        if not self.game_end:    
            if self.snakedirection != (0, 0) and not self.game_start:
                self.game_start = True
                #print('==> game starts...')
                self.show_text('==> game starts...')

            if  self.game_start and self.snakedirection != (0, 0) and not self.game_paused :
                self.game_running = True
            elif self.game_start and self.snakedirection != (0, 0) and self.game_paused:
                self.game_running = True
                self.game_paused = False
                self.show_text('==> game continues...')
                #print('==> game continues')

        #Step 2: check if game running or paused
        if self.game_running:
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
            # 4.4 exit found ==> game win!               
            elif self.game_status == self.pass_exit:
                    self.game_win()
            #print(datetime.now().time(),'Loop_End' ,'direction=',self.snakedirection,'commands=', self.commands)
            
    def collision_detection(self):
        if self.new_snake_headposition in self.spielfeld.snake_positions:
            print('snake body:',self.spielfeld.snake_positions)
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
        self.reset()                            # create a new game and DB
        self.spielfeld.create_world()
        self.new_snake_headposition = self.snake.headposition
        self.game_status = self.no_collision
        print(datetime.now().time(),'create new_world:')
    
    def game_over(self):
        self.game_running = False
        self.game_start = False
        self.game_end = True
        self.commands = []
        self.show_text('==> Game Over!')
        self.spielfeld.show_game_over_reason(self.new_snake_headposition)
        #self.spielfeld.show_status()

    def game_win(self):
        self.game_running = False
        self.game_start = False
        self.game_end = True
        self.commands = []
        self.show_text('==> You win!')
        #self.spielfeld.show_status()


    def reset(self):
        self.snakedirection = (0, 0)
        self.no_collision = 1
        self.game_status = self.no_collision
        self.game_start = False
        self.game_running = False
        self.game_end = False
        
        self.snake.reset()
        self.spielfeld.reset()
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

        self.apples_amount = 15
        self.walls_amount = 5

        self.spielfeld_db = {}         
        self.empty_fields = []
        self.apple_positions = []
        self.exit_position = []
        self.wall_positions = []
        self.snake_positions = []
        self.snake_headposition = []
        self.new_empty_field = []

        self.create_playground()
        self.show_text('init class Spielfeld done')

    def create_playground(self):
        # create an empty playground                                X,Y-Koordinanten-Paare erzeugen und in dem dict fuers Spielfeld als leere Felder anlegen 
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

        self.show_text('init class Spielfeld done')

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

    def create_exit(self):
        self.empty_fields = []
        for item in self.spielfeld_db:                               # gehe jedes Item der Spielfeld-DB durch
            if self.spielfeld_db[item] == " ":                       # pruefe auf leere Felder
                self.empty_fields.append(item)                       # Erstelle eine Liste mit Koordinatenpaare der leeren Felder
        """       
        temp = []        
        print('self.empty_fields:',self.empty_fields)
        for element in self.spielfeld_db:
            if self.spielfeld_db[element] == 'S':
                temp.append(element)
        print('____Snake:',len(temp),temp )
        print('snake_positions:',len(self.snake_positions),self.snake_positions)
        """
        item = randint(0, len(self.empty_fields)-1)                 # Picke random ein element aus den leeren Spielfeldern heraus 
        self.exit_position.append(self.empty_fields[item])          # füge dieses Element zur Liste der Exit-Positionen hinzu
        del self.empty_fields[item]                                 # Lösche das Element aus der Liste der freien Felder
        self.spielfeld_db[self.exit_position[0]] = "E"              # Eintrag in die DB als Exit
        x,y = self.exit_position[0]      
        self.canvas.itemconfigure(str(x)+'_'+str(y), fill='blue',tags=(str(x)+'_'+str(y),'exit')) #change the color according to the defined
        """
        print('_______',datetime.now().time(),' create exit at: ', self.exit_position[0])
        
        if self.exit_position[0] in temp:
            print(temp.index(self.exit_position[0]))
        else:
            print('exit not in ____Snake:')
        if self.exit_position[0] in self.snake_positions:
            print(self.snake_positions.index(self.exit_position[0]))
        else:
            print('exit not in snake_positions:')            
            
        #print('Exit:',self.exit_position[0])
        """
        
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


    def show_game_over_reason(self,item_position):
        print('reason for game over ==> field',item_position,'item_type:',self.spielfeld_db[item_position])

    def load_next_level(self):
        pass
        
    def reset(self):
        self.spielfeld_db = {}         
        self.empty_fields = []
        self.apple_positions = []
        self.exit_position = []
        self.wall_positions = []
        self.snake_positions = []
        self.snake_headposition = []
        self.new_empty_field = []

        self.create_playground()
        
        #self.create_world()
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
