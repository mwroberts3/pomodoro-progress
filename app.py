from flask import Flask, render_template, redirect, request, abort
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
import csv

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
# really not sure what this does, but just copied from CS50 finance python file
    # looks like there's some more info here https://www.reddit.com/r/cs50/comments/bc4x9t/help_understanding_session_config_with/
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# opens the app's database
db = SQL("sqlite:///pomodoro.db")

# dictionary used to store the table id that user wants to use.
session = {"table_id" : "user input"}


@app.route('/', methods=["GET", "POST"])
def load():
    if request.method == "POST":
        # TODO want users to have the option to load table or create one
        return redirect('/home')
    else:
        return render_template("load.html")

@app.route('/home')
def home():
    with open('pptest.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')

        # counts the number of entries in imported csv and creates hashtable of dictionaries
        count = 0
        raw_data = []
        for row in csv_reader:
            raw_data.append(row)
            count += 1
        
        # determines number of total weeks in csv file
        total_weeks = int(count/7)

        # sets up a 2D array a different list for every week of the csv provided
        weeks = [[] for j in range(total_weeks + 1)]

        
        # adds data to weeks hashtable in groups of seven
        day_count = 0
        week_count = 0
        tomato_count = 0
        for row in raw_data:
            day_count += 1
            tomato_count += int(row['tomatoes'])
            weeks[week_count].append(row)
            
            # determines if seven days has been counted
            if day_count % 7 == 0:
                week_count += 1
                day_count = 0
                # seems like I can make a temporary dictionary with same names as week's keys, so this can be displayed in the home.html template
                end_of_week_stats = {'date' : week_count, 'tomatoes' : tomato_count, 'task' : round(tomato_count/7, 2)}
                total_weeks -= 1
                weeks[week_count].append(end_of_week_stats)
                tomato_count = 0

            # copy table exactly, so it can be displayed in reverse on webpage
            full_chart = []
            for week in weeks:
                for day in week:
                    full_chart.append(day)

        
        # print(weeks)
            

        return render_template('home.html', full_chart = full_chart, week_count = week_count, tomato_count = tomato_count, day_count = day_count)

# print('test')