from flask import Flask, render_template, redirect, request, abort, flash
from flask_session import Session
from tempfile import mkdtemp
from cs50 import SQL
from datetime import date, datetime, timedelta
import csv
from pomo_helpers import statistics, deadline_conversion, current_date_diff

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


@app.route("/", methods=["GET", "POST"])
def load():
    if request.method == "POST":

        # opens the app's database and converts to usable dictionary
        db = SQL("sqlite:///pomodoro.db")

        # if user wants to load existing table
        if request.form.get("load"):
            saved_tables = db.execute(
                "SELECT * FROM tables WHERE table_name=:table_name AND table_password=:table_password",
                table_name=request.form.get("table_name"),
                table_password=request.form.get("password"),
            )

            # check to see if user input table name exists in database
            # if there is not exactly one list returned, then display error message
            if len(saved_tables) != 1:
                flash(
                    "table name and/or password is incorrect, please check spelling and try again"
                )
                return render_template("load.html")

            else:
                session["table_id"] = saved_tables[0]["id"]
                session["table_name"] = saved_tables[0]["table_name"]
                session["purpose"] = saved_tables[0]["purpose"]
                session["hours_goal"] = saved_tables[0]["hours_goal"]
                session["time_frame"] = saved_tables[0]["time_frame"]
                session["start_date"] = saved_tables[0]["start_date"]
                session["tomato_rate"] = saved_tables[0]["tomato_rate"]

                # converts the time_frame string into individual years, months and days elements
                session["days_until_deadline"] = deadline_conversion(
                    session["time_frame"], session["start_date"]
                )

                # finds the current number of days until you reach deadline
                session["current_days_until_deadline"] = current_date_diff(
                    session["time_frame"]
                )

                # converts the date formats in right column to something more easy to digest visually
                session["time_frame"] = datetime.strptime(
                    session["time_frame"], "%Y-%m-%d"
                )
                session["time_frame"] = session["time_frame"].strftime("%b %d, %Y")
                session["start_date"] = datetime.strptime(
                    session["start_date"], "%Y-%m-%d"
                )
                session["start_date"] = session["start_date"].strftime("%b %d, %Y")

                # DEBUG-CODE: return render_template("test.html", session=session, saved_tables=saved_tables)

                return redirect("/home")

        # if user wants to create a new table
        if request.form.get("create"):

            saved_tables = db.execute(
                "SELECT id FROM tables WHERE table_name=:table_name",
                table_name=request.form.get("new_table_name"),
            )

            # checks to see if table with that name already exists in database
            if len(saved_tables) == 1:
                flash("a table with that name already exists, please choose another")
                return render_template("load.html")

            if request.form.get("new_password") != request.form.get("confirm_password"):
                flash("passwords do not match, please try again")
                return render_template("load.html")

            else:
                # inserts new table name, with automatic id into tables table
                db.execute(
                    "INSERT INTO tables (table_name, table_password, purpose, hours_goal, time_frame, start_date, tomato_rate) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    request.form.get("new_table_name"),
                    request.form.get("new_password"),
                    request.form.get("purpose"),
                    request.form.get("hours_goal"),
                    request.form.get("time_frame"),
                    request.form.get("date"),
                    request.form.get("tomato_setting"),
                )

                # pull up newly created table's ID and save to session list
                saved_tables = db.execute(
                    "SELECT * FROM tables WHERE table_name=:table_name",
                    table_name=request.form.get("new_table_name"),
                )
                session["table_id"] = saved_tables[0]["id"]
                session["table_name"] = saved_tables[0]["table_name"]
                session["purpose"] = saved_tables[0]["purpose"]
                session["hours_goal"] = saved_tables[0]["hours_goal"]
                session["time_frame"] = saved_tables[0]["time_frame"]
                session["start_date"] = saved_tables[0]["start_date"]
                session["tomato_rate"] = saved_tables[0]["tomato_rate"]

                # calculates the amount of days until deadline is reached
                session["days_until_deadline"] = deadline_conversion(
                    session["time_frame"], session["start_date"]
                )

                # finds the current number of days until you reach deadline
                session["current_days_until_deadline"] = current_date_diff(
                    session["time_frame"]
                )

                # converts the date formats in right column to something more easy to digest visually
                # first makes sure the user provided deadline (session['time_frame']) is in the correct format
                if not session["time_frame"]:
                    session["time_frame"] = datetime.today()
                    time_frame_insert = session["time_frame"].strftime("%m/%d/%y")
                    db.execute(
                        "UPDATE tables SET time_frame =:time_frame WHERE id=:id",
                        time_frame=time_frame_insert,
                        id=session["table_id"],
                    )
                else:
                    session["time_frame"] = datetime.strptime(
                        session["time_frame"], "%Y-%m-%d"
                    )

                session["time_frame"] = session["time_frame"].strftime("%b %d, %Y")
                session["start_date"] = datetime.strptime(
                    session["start_date"], "%Y-%m-%d"
                )
                session["start_date"] = session["start_date"].strftime("%b %d, %Y")

                return redirect("/home")
    else:
        return render_template("load.html")


@app.route("/home", methods=["GET", "POST"])
def home():

    if request.method == "POST":
        db = SQL("sqlite:///pomodoro.db")

        date_check = db.execute(
            "SELECT date FROM daily_history WHERE table_id=:table_id ORDER BY date DESC LIMIT 1",
            table_id=session["table_id"],
        )

        # find date of previous entry to table
        previous_date = None
        for row in date_check:
            previous_date = row["date"]

        # convert date string from table into python date type
        previous_date = datetime.strptime(previous_date, "%Y-%m-%d")

        # get current date
        current_date = datetime.strptime(request.form.get("date"), "%Y-%m-%d")

        # calculates the number of days between current date and previous entries day
        date_diff = (current_date - previous_date).days

        # for same date addition purposes
        current_date_same = request.form.get("date")

        # if no days have been skipped, 0 tomato entries do not have to be added, and user can go straight to home page, otherwise entries with '0' tomato counts need to be added for each day missed
        if date_diff == 0:
            date_previous_data = db.execute(
                "SELECT tomato_count, task, notes FROM daily_history WHERE table_id=:table_id AND date=:date",
                table_id=session["table_id"],
                date=current_date_same,
            )

            # the next ~20 lines make it so tasks and notes added in separate entry for same day have correct grammer
            if date_previous_data[0]["task"] == None:
                date_previous_data[0]["task"] = ""

            if date_previous_data[0]["notes"] == None:
                date_previous_data[0]["notes"] = ""

            task_space = ""
            notes_space = ""

            if not date_previous_data[0]["task"] or not request.form.get("task"):
                task_space = ""
            else:
                task_space = ", "

            if not date_previous_data[0]["notes"] or not request.form.get("notes"):
                notes_space = ""
            else:
                notes_space = " || "

            db.execute(
                "UPDATE daily_history SET tomato_count=:tomato_count, task=:task, notes=:notes WHERE table_id=:table_id AND date=:date",
                tomato_count=date_previous_data[0]["tomato_count"]
                + int(request.form.get("tomatoes")),
                task=date_previous_data[0]["task"]
                + task_space
                + request.form.get("task"),
                notes=date_previous_data[0]["notes"]
                + notes_space
                + request.form.get("notes"),
                table_id=session["table_id"],
                date=current_date_same,
            )

            return redirect("/home")
        else:
            date_diff -= 1
            while date_diff > 0:
                db.execute(
                    "INSERT INTO daily_history (table_id, date, tomato_count) VALUES (?, ?, 0)",
                    session["table_id"],
                    current_date - timedelta(days=date_diff),
                )

                strft_days = current_date - timedelta(days=date_diff)

                db.execute(
                    "UPDATE daily_history SET display_date=:display_date WHERE table_id=:table_id AND date=:date",
                    display_date=strft_days.strftime("%m-%d"),
                    table_id=session["table_id"],
                    date=current_date - timedelta(days=date_diff),
                )

                date_diff -= 1

            db.execute(
                "INSERT INTO daily_history (table_id, date, display_date, tomato_count, task, notes) VALUES(?, ?, ?, ?, ?, ?)",
                session["table_id"],
                request.form.get("date"),
                request.form.get("date-displayed"),
                request.form.get("tomatoes"),
                request.form.get("task"),
                request.form.get("notes"),
            )
            return redirect("/home")

        # DEBUG-CODE return render_template("test.html", previous_date=previous_date, current_date=current_date, date_diff=date_diff)

    else:
        db = SQL("sqlite:///pomodoro.db")
        user_daily_history = db.execute(
            "SELECT * FROM daily_history WHERE table_id=:table_id",
            table_id=session["table_id"],
        )

        # checks to see if user has any previous data, if they don't have any entries, send them to firstentry.html template
        if len(user_daily_history) < 1:
            return redirect("/firstentry")

        # counts the number of entries in table for given user
        count = 0
        user_data = []
        for row in user_daily_history:
            user_data.append(row)
            count += 1

        # determines the total number of weeks
        total_weeks = int(count / 7)

        # sets up a 2D array--a different list for every 7 day count
        weeks = [[] for j in range(total_weeks + 1)]

        # adds data to weeks hashtable in groups of seven
        day_count = 0
        week_count = 0
        tomato_total = 0
        tomato_count_from_full_weeks = 0
        for row in user_data:
            day_count += 1
            tomato_total += int(row["tomato_count"])
            weeks[week_count].append(row)

            # deteremines if seven days has been counted
            if day_count % 7 == 0:
                week_count += 1
                day_count = 0
                # seems like I can make a temporary dictionary with same names as week's keys, so this can be displayed in the home.html template
                end_of_week_stats = {
                    "date": week_count,
                    "tomato_count": tomato_total,
                    "task": round(tomato_total / 7, 2),
                }
                total_weeks -= 1
                weeks[week_count].append(end_of_week_stats)
                tomato_count_from_full_weeks += end_of_week_stats["tomato_count"]
                tomato_total = 0

            # copy table exactly, so it can be displayed in reverse on webpage
            full_chart = []
            for week in weeks:
                for day in week:
                    full_chart.append(day)

            # send user_data to statistics function in stat_helpers to generate stats
            stats = statistics(user_data, session)

            # calculate weekly average...NOT ABLE TO divide tomato_count_from_full_weeks by week_count in python for some reason, so had to do it in jinja
            stats["weekly_average"] = tomato_count_from_full_weeks

            # DEBUG-CODE
            # return render_template("test.html", stats=stats)

        return render_template(
            "home.html",
            full_chart=full_chart,
            week_count=week_count,
            tomato_total=tomato_total,
            day_count=day_count,
            stats=stats,
            session=session,
        )


@app.route("/firstentry", methods=["GET", "POST"])
def firstentry():
    if request.method == "POST":
        db = SQL("sqlite:///pomodoro.db")
        db.execute(
            "INSERT INTO daily_history (table_id, date, display_date, tomato_count, task, notes) VALUES(?, ?, ?, ?, ?, ?)",
            session["table_id"],
            request.form.get("date"),
            request.form.get("date-displayed"),
            request.form.get("tomatoes"),
            request.form.get("task"),
            request.form.get("notes"),
        )
        return redirect("/home")

    else:
        return render_template("firstentry.html")


@app.route("/howtouse")
def howtouse():
    return render_template("howtouse.html")


@app.route("/journal", methods=["GET", "POST"])
def journal():
    db = SQL("sqlite:///pomodoro.db")
    if request.method == "POST":
        date = datetime.today()
        date_date = date.strftime("%b %d, %Y")
        date_time = date.strftime("%I:%M%p")

        # checks to see if there's already a journal entry for current date
        previous_entries = db.execute(
            "SELECT date FROM journal WHERE date=:date AND table_id=:table_id",
            date=date_date,
            table_id=session["table_id"],
        )
        if len(previous_entries) == 1 or len(previous_entries) > 1:
            session["journal_same_date"] = False
        else:
            session["journal_same_date"] = True

        if session["journal_same_date"] == True:
            db.execute(
                "INSERT INTO journal (table_id, entry, date, time) VALUES (?, ?, ?, ?)",
                session["table_id"],
                request.form.get("entry"),
                date_date,
                date_time,
            )
        else:
            db.execute(
                "INSERT INTO journal (table_id, entry, date, time) VALUES (?, ?, '', ?)",
                session["table_id"],
                request.form.get("entry"),
                date_time,
            )

        return redirect("/journal")
    else:
        journal_data = db.execute(
            "SELECT * FROM journal WHERE table_id=:table_id ORDER BY datetime DESC, time_exact ASC",
            table_id=session["table_id"],
        )
        return render_template(
            "journal.html", session=session, journal_data=journal_data
        )

