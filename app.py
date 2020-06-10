from flask import Flask, render_template, redirect, request, abort, flash
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from datetime import date, datetime, timedelta
import csv

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
# really not sure what this does, but just copied from CS50 finance python file
    # looks like there's some more info here https://www.reddit.com/r/cs50/comments/bc4x9t/help_understanding_session_config_with/
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# dictionary used to store the table id that user wants to use.
session = {"table_id" : "user input"}


@app.route('/', methods=["GET", "POST"])
def load():
    if request.method == "POST":
        
        # opens the app's database and converts to usable dictionary
        db = SQL("sqlite:///pomodoro.db")

        # if user wants to load existing table
        if request.form.get("load"):
            saved_tables = db.execute("SELECT id FROM tables WHERE table_name=:table_name", table_name=request.form.get("table_name"))
            
            # check to see if user input table name exists in database
            # if there is not exactly one list returned, then display error message
            if len(saved_tables) != 1:
                flash('That table name does not exist, please check spelling')
                return render_template("load.html")
                   
            else:
                session['table_id'] = saved_tables[0]['id']
                return redirect('/home')
                # DEBUG-CODE: return render_template("test.html", saved_tables=saved_tables, session_id = session['table_id'])
        
        # if user wants to create a new table
        if request.form.get("create"):

            saved_tables = db.execute("SELECT id FROM tables WHERE table_name=:table_name", table_name=request.form.get("table_name"))

            # checks to see if table with that name already exists in database
            if len(saved_tables) == 1:
                flash('A table with that name already exists, please choose another')
                return render_template("load.html")

            else:    
                # inserts new table name, with automatic id into tables table
                db.execute("INSERT INTO tables (table_name) VALUES (?)", request.form.get("table_name"))

                # pull up newly created table's ID and save to session list
                saved_tables = db.execute("SELECT id FROM tables WHERE table_name=:table_name", table_name=request.form.get("table_name"))
                session['table_id'] = saved_tables[0]['id']

                return redirect('/home')
    else:
        return render_template("load.html")

@app.route('/home', methods=["GET","POST"])
def home():
    
    if request.method == "POST":
        db = SQL("sqlite:///pomodoro.db")

        date_check = db.execute("SELECT date FROM daily_history WHERE table_id=:table_id ORDER BY date DESC LIMIT 1", table_id = session['table_id']) 

        # find date of previous entry to table
        previous_date = None
        for row in date_check:
            previous_date = row['date']

        # convert date string from table into python date type
        previous_date = datetime.strptime(previous_date, '%Y-%m-%d')
        
        # get current date
        current_date = datetime.today()

        # calculates the number of days between current date and previous entries day
        date_diff = ((current_date - previous_date).days)

        # convert current_date back to date format for GUI purposes
        current_date = date.today()

        # if no days have been skipped, 0 tomato entries do not have to be added, and user can go straight to home page, otherwise entries with '0' tomato counts need to be added for each day missed
        if date_diff == 0:
            date_previous_data = db.execute("SELECT tomato_count, task, notes FROM daily_history WHERE table_id=:table_id AND date=:date", table_id=session['table_id'], date=current_date)

            previous_tomato_count = date_previous_data[0]['tomato_count']
            previous_task = date_previous_data[0]['task']
            previous_notes = date_previous_data[0]['notes']

            db.execute("UPDATE daily_history SET tomato_count=:tomato_count, task=:task, notes=:notes WHERE date=:date", tomato_count = previous_tomato_count + int(request.form.get("tomatoes")), task = previous_task + ", " +request.form.get("task"), notes = previous_notes + "| " +request.form.get("notes"), date=current_date)

            return redirect('/home')
        else:
            date_diff -= 1
            while date_diff > 0:
                db.execute("INSERT INTO daily_history (table_id, date, tomato_count) VALUES (?, ?, 0)", session['table_id'], current_date - timedelta(days=date_diff))
                date_diff -= 1

            db.execute("INSERT INTO daily_history (table_id, date, tomato_count, task, notes) VALUES(?, date('now','localtime'), ?, ?, ?)", session['table_id'], request.form.get('tomatoes'), request.form.get('task'), request.form.get('notes'))
            return redirect('/home')


        # DEBUG-CODE return render_template("test.html", previous_date=previous_date, current_date=current_date, date_diff=date_diff)

    else:    
        db = SQL("sqlite:///pomodoro.db")
        user_daily_history = db.execute("SELECT * FROM daily_history WHERE table_id=:table_id", table_id = session['table_id'])

        # checks to see if user has any previous data, if they don't have any entries, send them to firstentry.html template
        if len(user_daily_history) < 1:
            return redirect('/firstentry')

        # counts the number of entries in table for given user
        count = 0
        user_data = []
        for row in user_daily_history:
            user_data.append(row)
            count += 1
        
        # determines the total number of weeks
        total_weeks = int(count/7)

        # sets up a 2D array--a different list for every 7 day count
        weeks = [[] for j in range(total_weeks + 1)]

        # adds data to weeks hashtable in groups of seven
        day_count = 0
        week_count = 0
        tomato_total = 0
        for row in user_data:
            day_count += 1
            tomato_total += int(row['tomato_count'])
            weeks[week_count].append(row)

            # deteremines if seven days has been counted
            if day_count % 7 == 0:
                week_count += 1
                day_count = 0
                # seems like I can make a temporary dictionary with same names as week's keys, so this can be displayed in the home.html template
                end_of_week_stats = {'date' : week_count, 'tomato_count' : tomato_total, 'task' : round(tomato_total/7, 2)}
                total_weeks -= 1
                weeks[week_count].append(end_of_week_stats)
                tomato_total = 0

            # copy table exactly, so it can be displayed in reverse on webpage
            full_chart = []
            for week in weeks:
                for day in week:
                    full_chart.append(day)

        return render_template('home.html', full_chart = full_chart, week_count = week_count, tomato_total = tomato_total, day_count = day_count)
    # DEBUG-CODE return render_template("test.html", user_data = user_data, session_id = session['table_id'])
    
@app.route('/firstentry', methods=["GET","POST"])
def firstentry():
    if request.method == "POST":
        db = SQL("sqlite:///pomodoro.db")
        db.execute("INSERT INTO daily_history (table_id, date, tomato_count, task, notes) VALUES(?, date('now','localtime'), ?, ?, ?)", session['table_id'], request.form.get('tomatoes'), request.form.get('task'), request.form.get('notes'))
        return redirect('/home')

    else:
        return render_template('firstentry.html')

@app.route('/howtouse')
def howtouse():
    return render_template('howtouse.html')