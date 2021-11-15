"""
Benjamin Chen
WebScraping, Serialization, and Databasing File
"""
import requests
from bs4 import BeautifulSoup 
import re
import json
import sqlite3

class Movie:
    def __init__(self, name="", url = "", director = "", actor = None, month = ""):
        """
        constructor method for movie object
        input: name - name of movie, url - url of rotten tomato website, director - director of movie, actor - list of actors, month - month movie is released in
        output: none
        creates a movie object that stores parameters desired
        """
        if not actor: actor = []
        self.name = name
        self.url = url
        self.director = director
        self.actor = actor
        self.month = month
    
    def getMovieTitle(self):
        return self.name
    def getURL(self):
        return self.url
    def getDirector(self):
        return self.director
    def getActor(self):
        return self.actor
    def getMonth(self):
        return self.month
    def setDirector(self, director):
        self.director = director
    
    def setActor(self, actor):
        self.actor = actor
    def setURL(self,url):
        self.url = url
    def setMonth(self, month):
        self.month = month
    def __str__(self):
        return "Movie Name: %s \nURL: %s \nDirector: %s\nActor: %s\nRelease Month: %s" %(self.name, self.url, self.director, self.actor, self.month)
"""
page = requests.get("https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/")
soup = BeautifulSoup(page.content, "lxml")
data = soup.find('div', class_ = 'articleContentBody') 

tag = data.find_all('p')
movieList = []
counter = 0
movieTitle = ""
movieDirector = ""
movieActor = []
movieMonth = ""
for t in tag:
    if re.search('Directed by:\s*([^\n\r]*)',t.text) and re.search('Starring:\s*([^\n\r]*)',t.text) and re.search('Opening on:\s*([^\n\r]*)', t.text):
        temp = t.text.split('\n')[0]
        temp = re.sub('[0-9][0-9]%','',str(temp))
        movieTitle = temp
        temp = re.search('Directed by:\s*([^\n\r]*)', str(t.text)).group()
        movieDirector = ((temp[13:]))
        temp = re.search('Starring:\s*([^\n\r]*)',str(t.text)).group()
        movieActor = temp[10:].split(", ")
        temp = re.search('Opening on:\s*([^\n\r]*)', str(t.text)).group()
        movieMonth = temp[12:].split()[0]
        m = Movie(movieTitle, "No URL", movieDirector, movieActor, movieMonth)
        movieList.append(m)
url = data.select('p strong a')
for ele in url:
    if re.search('https', ele['href']):
        for x in movieList:
            if ele.text in x.getMovieTitle():
                x.setURL(ele['href'])

jsonableList = []
for ele in movieList:
    jsonableList.append({"Name": ele.getMovieTitle(), "URL": str(ele.getURL()), "Director": ele.getDirector(), "Actors": ele.getActor(), "Month": ele.getMonth()})
    #because movie object cannot be seralized, but elements in a list of dictionaries and then serialize
with open('data.json', 'w') as js:
        json.dump(jsonableList, js, indent = 3)

"""
with open('data.json', 'r') as js:
    data = json.load(js)

conn = sqlite3.connect('movie.db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS MovieDB")      
cur.execute('''CREATE TABLE MovieDB(             
                   key INTEGER NOT NULL PRIMARY KEY,
                   name TEXT,
                   URL TEXT,
                   director TEXT,
                   month TEXT)''')

cur.execute('DROP TABLE IF EXISTS MonthDB')
cur.execute('''CREATE TABLE MonthDB(
                key INTEGER NOT NULL PRIMARY KEY,
                month TEXT
                )''')

cur.execute('''INSERT INTO MonthDB (key, month) VALUES
            (1, 'January'),
            (2, 'February'),
            (3, 'March'),
            (4, 'April'),
            (5, 'May'),
            (6, 'June'),
            (7, 'July'),
            (8, 'August'),
            (9, 'September'),
            (10,'October'),
            (11,'November'),
            (12,'December'),
            (13,'TBD'),
            (14,'2021')''')


counter = 0
for ele in data:
    cur.execute('Select key FROM MonthDB WHERE month = ?', (ele['Month'],)) #get the key of months from monthdb and then get that as the attribute in moviedb
    month_id = cur.fetchone()[0]
    cur.execute("INSERT INTO MovieDB (key, name, url, director, month) VALUES (?, ?, ?, ?, ?)", (counter, ele['Name'], ele['URL'], ele['Director'], month_id))
    counter +=1

max = 0
for actors in data:
    if max < len(actors['Actors']):
        max = len(actors['Actors'])
for i in range(max):
    cur.execute('''ALTER TABLE MovieDB ADD COLUMN {} TEXT''' .format('actor'+str(i))) #creates columns for each individual actor

for counter in range(len(data)): #each element in the DB
    for i in range(len(data[counter]['Actors'])): #each element in list of actors
        cur.execute('UPDATE MovieDB SET {} = ? where key = ?'.format('actor'+str(i)),(data[counter]['Actors'][i],counter)) #populates actor columns with frields from data
conn.commit()
"""
cur.execute('''SELECT MovieDB.key FROM MovieDB JOIN MonthDB ON MovieDB.month = MonthDB.key and MonthDB.key = ?''' ,(3,))
for x in cur.fetchall():
    print(x[0])
"""
cur.execute('''SELECT MovieDB.key FROM MovieDB''')
for x in cur.fetchall():
    print(x[0])