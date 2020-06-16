from flask import Flask, render_template, redirect, request, abort, flash
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from datetime import date, datetime, timedelta
import csv
from pomo_helpers import statistics, time_frame_conversion

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
# really not sure what this does, but just copied from CS50 finance python file
    # looks like there's some more info here https://www.reddit.com/r/cs50/comments/bc4x9t/help_understanding_session_config_with/
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# dictionary used to store the table id that user wants to use.
session = {}


@app.route('/', methods=["GET", "POST"])
def load():
    if request.method == "POST":
        
        # opens the app's database and converts to usable dictionary
        db = SQL("sqlite:///pomodoro.db")

        # if user wants to load existing table
        if request.form.get("load"):
            saved_tables = db.execute("SELECT * FROM tables WHERE table_name=:table_name", table_name=request.form.get("table_name"))
            
            # check to see if user input table name exists in database
            # if there is not exactly one list returned, then display error message
            if len(saved_tables) != 1:
                flash('That table name does not exist, please check spelling')
                return render_template("load.html")
                   
            else:
                session['table_id'] = saved_tables[0]['id']
                session['table_name'] = saved_tables[0]['table_name']
                session['purpose'] = saved_tables[0]['purpose']
                session['hours_goal'] = saved_tables[0]['hours_goal']
                session['time_frame'] = saved_tables[0]['time_frame']
                session['tomato_rate'] = saved_tables[0]['tomato_rate']
                
                # converts the time_frame string into individual years, months and days elements
                # TODO take deadline input from user and determine the amount of days between now and then
                session.update(time_frame_conversion(session))            
            
                # DEBUG-CODE: return render_template("test.html", session=session, saved_tables=saved_tables)

                return redirect('/home')
                
        
        # if user wants to create a new table
        if request.form.get("create"):

            saved_tables = db.execute("SELECT id FROM tables WHERE table_name=:table_name", table_name=request.form.get("new_table_name"))

            # checks to see if table with that name already exists in database
            if len(saved_tables) == 1:
                flash('A table with that name already exists, please choose another')
                return render_template("load.html")

            else:    
                # inserts new table name, with automatic id into tables table
                db.execute("INSERT INTO tables (table_name, purpose, hours_goal, time_frame, tomato_rate) VALUES (?, ?, ?, ?, ?)", request.form.get("new_table_name"), request.form.get("purpose"), request.form.get("hours_goal"), request.form.get("time_frame"), request.form.get("tomato_setting"))

                # pull up newly created table's ID and save to session list
                saved_tables = db.execute("SELECT * FROM tables WHERE table_name=:table_name", table_name=request.form.get("new_table_name"))
                session['table_id'] = saved_tables[0]['id']
                session['table_name'] = saved_tables[0]['table_name']
                session['purpose'] = saved_tables[0]['purpose']
                session['hours_goal'] = saved_tables[0]['hours_goal']
                session['time_frame'] = saved_tables[0]['time_frame']
                session['tomato_rate'] = saved_tables[0]['tomato_rate']

                # converts the time_frame string into individual years, months and days elements
                session.update(time_frame_conversion(session))                 

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
                      
            # the next ~20 lines make it so tasks and notes added in separate entry for same day have correct grammer
            if date_previous_data[0]['task'] == None:
                date_previous_data[0]['task'] = ""

            if date_previous_data[0]['notes'] == None:
                date_previous_data[0]['notes'] = ""

            task_space = ""
            notes_space = ""

            if not date_previous_data[0]['task'] or not request.form.get("task"):
                task_space =""
            else:
                task_space = ", "
            
            if not date_previous_data[0]['notes'] or not request.form.get("notes"):
                notes_space = ""
            else:
                notes_space = ", "          
            
            db.execute("UPDATE daily_history SET tomato_count=:tomato_count, task=:task, notes=:notes WHERE table_id=:table_id AND date=:date", tomato_count = date_previous_data[0]['tomato_count'] + int(request.form.get("tomatoes")), task = date_previous_data[0]['task'] + task_space + request.form.get("task"), notes = date_previous_data[0]['notes'] + notes_space + request.form.get("notes"), table_id=session['table_id'], date=current_date)

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

            # send user_data to statistics function in stat_helpers to generate stats
            stats = statistics(user_data, session)

            # DEBUG-CODE 
            # return render_template("test.html", stats=stats)

        return render_template('home.html', full_chart = full_chart, week_count = week_count, tomato_total = tomato_total, day_count = day_count, stats=stats, session=session)
    
    
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

@app.route('/notes')
def notes():
    return render_template('notes.html')