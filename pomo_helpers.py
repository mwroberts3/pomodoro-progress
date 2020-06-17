from datetime import date, datetime, timedelta

def statistics(user_data, session):
    total_tomatoes = 0
    stats = {}
    day_count = 0
    days_in_a_row = 0
    one_day_high = 0

    for row in user_data:
        total_tomatoes += row['tomato_count']
        day_count += 1
        if row['tomato_count'] > 0:
            days_in_a_row += 1
        else:
            days_in_a_row = 0
        if row['tomato_count'] > one_day_high:
            one_day_high = row['tomato_count']

    stats['one_day_high'] = one_day_high
    stats['total_tomatoes'] = total_tomatoes
    stats['daily_average'] = round(total_tomatoes/day_count, 2)
    stats['days_in_a_row'] = days_in_a_row

    # to find pomodoros_left
    if not session['hours_goal'] or not session['tomato_rate']:
        stats['pace'] = {'on_pace' : 'NA'}
        stats['pace'] = {'rate' : 0}
        return(stats)

    total_pomos = int((session['hours_goal'] * 60)/session['tomato_rate'])
    stats['pomos_left'] = total_pomos - stats['total_tomatoes']

    # to find completion % of goal
    stats['completion_percentage'] = round(((stats['total_tomatoes'] / total_pomos) * 100), 1)

    # to find pace
    on_pace_average = total_pomos / session['days_until_deadline']

    if stats['daily_average'] >= on_pace_average:
        stats['pace'] = {'on_pace' : 'on pace'}
    else:
        stats['pace'] = {'on_pace' : 'off'}
    
    stats['pace']['rate'] = round((stats['daily_average'] / on_pace_average) * 100) 
    
    # DEBUG stats['test'] = int(total_days)
    
    return (stats)

def deadline_conversion(deadline, start_date):
    #TODO need to skip this if user inputs incompatable or no date
    if deadline is None:
        deadline = datetime.today()
    else:    
        deadline = datetime.strptime(deadline, '%m/%d/%y')
    # start_date defaults to current date in sqlite table when creating new
    start_date = datetime.strptime(start_date, '%Y-%m-%d')

    # calculates the number of days between current date and previous entries day
    date_diff = ((deadline - start_date).days)

    return(date_diff)
