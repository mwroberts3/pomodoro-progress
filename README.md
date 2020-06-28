# Pomo Progress!
## Purpose 
Started as final project for CS50 and turned into a tool I'll probably keep using and building for the forseeable future. It is a way to track data regarding advancement towards a goal. It's based on the Pomodoro Technique&trade;, but could really apply to anytype of task that requires repetition. 

Compared to other versions of Pomodoro trackers on the internet, Pomo Progress! is more concerned and aimed at helping individuals acheive longer term goals. 

## Current Version Information ##
**Version:** 1.0<br>
**Completion Date:** July 1, 2020<br>
**Creator:** mwroberts3<br>
**Backend:** Flask<br>
**Database:** Sqlite, exists as a sole .db file<br>
**Host:** http://pomoprogress.pythonanywhere.com/<br>
**Web Launch Date:** July 5, 2020

## Usage ##
1. ### Users create a new table on the first page of website
    1. asks users to pick a table name (basically username) and a password.
    2. asks users to define the goal they're trying to acheive<br>
        eg. _weight loss_
    3. asks users how many hours it will take to acheive this goal
    4. asks users to choose a deadline by which they want to acheive this goal
    5. final input asks users to set the amount of time for each rep (based on the Pomodoro Technique&trade;)
2. ### Users are asked to input their first entry
    1. each row in the table takes four values, **date**, **pomodoro count**, **task(s)**, and **notes**
        * users provide **pomodoro count**, **task(s)**, and **notes**
        * **notes** are not required, **task** is only required on the first entry, and the pomodoro count can be 0
    2. users are shown a table display. The table displays info for every day's activity (or lack of), since the table was created. **The table is updated when a new entry is added.**
    3. new entries can be added by using the inputs at the top of the page, underneath the banner. **Multiple entries can be added in a single day**
        1. since there is no built-in timer, users can time themselves by any external means, such as the <a href="https://www.google.com/search?q=timer&oq=timer&aqs=chrome.0.69i59j0l5j69i61j69i60.995j0j7&sourceid=chrome&ie=UTF-8">Google timer</a>
    4. basic information about the table is shown in the left-hand column and more detailed stats are shown in the right-hand column. 
3. ### More features ###
    1. users can user the journal feature to add long-form thoughts and ideas about their journey
    2. more funtions to be added in future versions
## Support ##
If your a user with questions or a fellow github user with tech questions, please message the email address below. 
<br>
**email:** mwroberts89@gmail.com

## Roadmap ##
### Version 1.1 ###
* allow users to delete their table
* continued ui tweeks for better aesthetics and responsiveness
* rewrite _howtouse.html_ page and make more comprehensive
* make mention of journal in "Other Features" section of *howtouse.html* a link to the journal. But if there is no login info, need to alert user that they have to login first
* the table of contents in *howtouse.html* isn't totally usable because the page isn't long enough for the later links to jump to the top of the page
### Beyond 1.1 ###
* add way for users to download their tables
* embedded timer
* have results load up to 10 weeks and then have a link to show more
* add way to view a chart that shows a user's progress
* some kind of custom styling if a day's pomo count is higher than the necessary average
* a way to search table parameters and display charts, eg. days over x amount of tomatoes, rank days from least to most
### License ###
As of June 28, 2020, not sure what license I will be using, but I want to be open source and allow for contributions.
### Contributing ###
If you're a web development interested in contributing to Pomo Progress! Send me an email to discuss.