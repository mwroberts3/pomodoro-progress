# Pomo Progress!

## Purpose

Started as final project for CS50 and turned into a tool I'll probably keep using and building for the foreseeable future. It is a way to track data regarding advancement towards a goal, short or long term. It's based on the Pomodoro Technique&trade;, but could really apply to any type of task that requires repetition.

Compared to other versions of Pomodoro trackers on the internet, Pomo Progress! is more concerned and aimed at helping individuals achieve longer term goals.

## Current Version Information

**Version:** 1.3.0<br>
**Creator:** mwroberts3<br>
**Server-Side:** Flask<br>
**Database:** Sqlite, exists as a sole .db file<br>
**Host:** http://pomoprogress.pythonanywhere.com/<br>
**Web Launch Date:** July 5, 2020<br>
**Current Version Launch Date:** February 1, 2021<br>

## Usage

1. ### Users create a new table on the first page of website
   1. asks users to pick a table name (basically username) and a password.
   2. asks users to define the goal they're trying to achieve<br>
      eg. _weight loss_
   3. asks users how many hours it will take to achieve this goal
   4. asks users to choose a deadline by which they want to achieve this goal
   5. final input asks users to set the amount of time for each rep (based on the Pomodoro Technique&trade;)
2. ### Users are asked to input their first entry
   1. each row in the table takes four values, **date**, **pomodoro count**, **task(s)**, and **notes**
      - users provide **pomodoro count**, **task(s)**, and **notes**
      - **notes** are not required, **task** is only required on the first entry, and the pomodoro count can be 0
   2. users are shown a table display. The table displays info for every day's activity (or lack of), since the table was created. **The table is updated when a new entry is added.**
   3. new entries can be added by using the inputs at the top of the page, underneath the banner. **Multiple entries can be added in a single day**
      1. since there is no built-in timer, users can time themselves by any external means, such as the <a href="https://www.google.com/search?q=timer&oq=timer&aqs=chrome.0.69i59j0l5j69i61j69i60.995j0j7&sourceid=chrome&ie=UTF-8">Google timer</a>
   4. basic information about the table is shown in the left-hand column and more detailed stats are shown in the right-hand column.
3. ### More features
   1. users can view a graph of their overall progress since inception of table (beta)
   2. more features to be added in future versions

## Support

If your a user with questions or a fellow github user with tech questions, please send a message to the email address below.
<br>
**email:** mwroberts89@gmail.com

## Version History

#### Version 1.3 - February 1, 2021

- added cookies for smoother use between multiple users. Table IDs are encrypted so other user's cannot be edited by anyone

**Graph** - added a basic graph feature, which I intead to bolster in future versions that shows a chart of total progress

**Journal** - removed the journal feature, as I never used it myself and seemed redundant with the notes functionality

#### Version 1.2 - August 7, 2020

**Notes** - javascript alert notes have been replaced by a simple popup, which should cut down on any glitches or bugs, plus it looks cleaner, and the experience is more seamless.

**Timezone Accuracy** - an entry's input date is now taken from the user's browser with some javascript, rather than previously being dictated by the settings in its wsgi.py file. Rather than integrate this functionality into the journal feature, I've removed the timestamp from the journal and am leaning towards removing the journal altogether. It seems a little redundant in addition to the notes feature.

**Color-Coded Pomo Count Feedback** - pomo count of date that is >= to daily average is yellow, pomo count of date that is >= double the daily average is green, pomo count of date that is <= daily average / 3 is red.

**UI Tweaks** - some minor UI tweaks that I feel make the site look better, but not really worth mentioning here.

## Roadmap

### Version 1.4

- add graphing and graph page
  https://www.geeksforgeeks.org/graph-plotting-in-python-set-1/
  https://mpld3.github.io/quickstart.html
  **Projected Release Date:** Fall 2020

### Version 1.5 - 1.9

- allow users to delete their table
- continued ui tweaks for better aesthetics and responsiveness
- rewrite _howtouse.html_ page and make more comprehensive
- make mention of journal in "Other Features" section of _howtouse.html_ a link to the journal. But if there is no login info, need to alert user that they have to login first
- the table of contents in _howtouse.html_ isn't totally usable because the page isn't long enough for the later links to jump to the top of the page
- optimize _howtouse.html_ for smaller screens
- not sure how to get favicon.ico working, need to do more research. Just using a .png image for now
- some kind of custom styling if a day's pomo count is higher than the necessary average
- have results load up to 10 weeks and then have a link to show more

### Beyond version 1.x

- add way for users to download their tables
- embedded timer
- a way to search table parameters and display charts, eg. days over x amount of tomatoes, rank days from least to most, maybe call it 'reports' or something and add the link to the navbar on the home page

### License

As of June 28, 2020, not sure what license I will be using, but I want it to be open source and allow for contributions.

### Contributing

If you're a beginner web developer interested in contributing and collaborating, send me an email to discuss.
