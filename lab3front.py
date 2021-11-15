"""
Benjamin Chen
GUI Class
"""
import tkinter as tk
import webbrowser
import sqlite3
import tkinter.messagebox as tkmb

class DisplayWin(tk.Toplevel):
    """
    Display Window object
    """
    def __init__(self, master, information):
        """
        Constructor for Display window object
        input - master - main window, information - list of information to be displayed in display window
        output - none
        """
        super().__init__()
        box = tk.Listbox(self, height = 10, width = 60)
        for info in information:
            box.insert('end', info['name'])
            box.insert('end', info['director'])
            for x in info['actors']:
                box.insert('end', x)
        box.pack()

class DialogWin(tk.Toplevel):
    def __init__(self, master, x):
        """
        constructor for dialog window object
        input - x - integer representing 3 buttons is pressed
        output - none
        """
        super().__init__()
        self.movies = []
        self.URL = ""
        self.actor = ''
        box = tk.Listbox(self, height = 12, width = 60, selectmode = "multiple")
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()
        if x == 0:
            tk.Label(self, text = "Click on a movie to select").pack()
            for movie in cur.execute('SELECT name from MovieDB'):
                self.movies.append(movie)
            self.movies.sort()

            for movie in self.movies:
                box.insert('end', str(movie)[2:-3])
            box.bind('<<ListboxSelect>>', self.getSelection)
            box.pack(side="left", fill="both", expand=True)

        if x == 1:
            tk.Label(self, text = "Click on a actor to select").pack()
            self.actors = []
            for actor in cur.execute('SELECT actor0 from MovieDB'):
                self.actors.append(actor)
            self.actors.sort()

            for actor in self.actors:
                box.insert('end', str(actor)[2:-3])
            
            box.bind('<<ListboxSelect>>',self.commandActor)
            box.pack(side = "left", fill = 'both', expand = True)
        
        if x == 2:
            tk.Label(self, text = "Click on a month to select").pack()
            self.actor = []
            for month in cur.execute('Select month from MonthDB'):
                self.actor.append(month)
            for x in self.actor:
                box.insert('end', str(x)[2:-3])
            box.bind('<<ListboxSelect>>', self.commandActor)
            box.pack(side = "left", fill = 'both', expand = True)
        S = tk.Scrollbar(self, orient="vertical")
        S.config(command = box.yview)
        S.pack(side = 'right', fill = 'y')
        box.config(yscrollcommand = S.set)

    def commandActor(self, event):
        """
        command method when user clicks in listbox
        input - event, saves what the user clicks in self.actor and then destroys window
        """
        widget = event.widget
        selection = widget.curselection()
        choice = widget.get(selection[0])
        self.actor = choice
        self.destroy()
    
    def getActor(self):
        return self.actor

    def getSelection(self, event):
        """
        command method when user clicks in listbox
        input - event, saves what the user clicks in self.URL and then destroys window
        """
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()
        widget = event.widget
        selection = widget.curselection()
        choice = widget.get(selection[0])
        cur.execute('Select URL from MovieDB WHERE name = ?', (choice,))
        URL = cur.fetchone()[0]
        if URL == "No URL":
            tkmb.showinfo(title = "No URL", message = "The Movie you chose has no URL")
            self.destroy()
        else:
            self.URL = URL
            self.destroy()
    
    def getURL(self):
        return self.URL

class MainWin(tk.Tk):
    def __init__(self):
        """
        Constructor for Main Window
        input - none
        output - none
        creates mainwin object with three buttons
        """
        self.x = 1
        super().__init__()
        self.title("Movies")
        tk.Label(self, text = self.x).grid(row = 0, column = 2)
        """
        tk.Label(self, text = "Search:").grid(row = 3, column = 0, sticky = 'w',padx = 5, pady = 10)
        tk.Button(self, text = "Webpage", fg = 'blue', command = self.movieWebpage).grid(row = 3, column = 1, sticky = 's', padx = 5, pady = 10)
        tk.Button(self, text = "Main Actor", fg = 'blue', command = self.actors).grid(row = 3, column = 2, padx = 5)
        tk.Button(self, text = "Month", fg = 'blue', command = self.months).grid(row = 3, column = 3, padx = 5)
        """
        tk.Button(self, text = 'test', command =  self.ree).grid()

    def ree(self):
        self.x +=1
        print('hi')
    def movieWebpage(self):
        """
        method call after user presses webpage button:
        gets url from dialogwin (after user is done making selection) and opens a webbrowser based on user selection
        input - none
        output - none
        """
        top = DialogWin(self,0)
        self.wait_window(top)
        if top.getURL() != "":
            webbrowser.open(top.getURL())

    def actors(self):
        """
        method call after user presses main actor button:
        gets topActor from dialogwin and saves it in actor name, then gets list of all the movie names, directors, and actors that are from that actor and sends that information to display win,
        that information is then displayed to user
        input - none
        output - none
        """
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()

        top = DialogWin(self, 1)
        self.wait_window(top)
        actorName = top.getActor()


        movieName = ""
        director = ""
        actorList = []
        actorList.append("Starring:\n")
        info = []
        if actorName:
            for x in cur.execute('Select key from MovieDB where actor0 = ?', (actorName,)):
                cur.execute('Select name from MovieDB where key = ?', (x[0],))
                movieName = cur.fetchone()[0]
                cur.execute('Select director from MovieDB where key = ?',(x[0],))
                director = cur.fetchone()[0]
                i = 0
                while not cur.execute('Select {} from MovieDB where key = ?'.format('actor'+str(i)), (x[0],)).fetchone()[0] == None:
                    actorList.append(cur.execute('Select {} from MovieDB where key = ?'.format('actor'+str(i)), (x[0],)).fetchone()[0] + '\n')
                    i+=1
                info.append({'name': 'Movie: '+movieName, 'director': 'Director: ' + director, 'actors': actorList})
        d = DisplayWin(self, info)
    
    def months(self):
        """
        method call after user presses month button
        gets user selected month (from dialogue window) and gets a list of all the movie names, directors, actors that are released in that month
        list is sent to display win to be displayed to user.
        """
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()
        top = DialogWin(self,2)
        self.wait_window(top)
        month = top.getActor() #month of user choice
        movieName = ""
        director = ""
        actorList = []
        actorList.append("Starring:\n")
        info = {}
        movieList = []
        for x in cur.execute('Select MovieDB.key from MovieDB JOIN MonthDB ON MovieDB.month = MonthDB.key and MonthDB.month = ?', (month,)).fetchall():
            cur.execute('Select name from MovieDB where key = ?', (x[0],))
            movieName = cur.fetchone()[0]
            cur.execute('Select director from MovieDB where key = ?',(x[0],))
            director = cur.fetchone()[0]
            i = 0
            while (not cur.execute('Select {} from MovieDB where key = ?'.format('actor'+str(i)), (x[0],)).fetchone()[0] == None):
                actorList.append(cur.execute('Select {} from MovieDB where key = ?'.format('actor'+str(i)), (x[0],)).fetchone()[0] + '\n')
                i+=1
                if i == 11:
                    break
            info = {'name': 'Movie: '+movieName, 'director': 'Director: ' + director, 'actors': actorList}
            movieList.append(info)
        d = DisplayWin(self, movieList)
app = MainWin()
app.mainloop()
