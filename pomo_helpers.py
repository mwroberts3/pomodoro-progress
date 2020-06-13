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

    #to find pomodoros_left
    if session['hours_goal'] == None or session['tomato_rate'] == None:
        stats['pace'] = {'on_pace' : 'NA'}
        stats['pace'] = {'rate' : 0}
        return(stats)

    total_pomos = int((session['hours_goal'] * 60)/session['tomato_rate'])
    stats['pomos_left'] = total_pomos - stats['total_tomatoes']
    
    #to find pace
    total_days = session['years'] * 365
    total_days += session['months'] * 30.42
    total_days += session['days']

    on_pace_average = total_pomos / total_days

    if stats['daily_average'] >= on_pace_average:
        stats['pace'] = {'on_pace' : 'on pace'}
    else:
        stats['pace'] = {'on_pace' : 'off'}
    
    stats['pace']['rate'] = round((stats['daily_average'] / on_pace_average) * 100) 
    
    # DEBUG stats['test'] = int(total_days)
    
    return (stats)

def time_frame_conversion(session):
    session['years'] =""
    session['months'] =""
    session['days'] =""
    
    # breakdown time_frame into separate elements for year, month, and day
    if session['time_frame'] == None:
        return (session)
    else:
        i = 0
        for ele in session['time_frame']:
            if ele == '/':
                i += 1
                continue
            if i == 0:
                session['years'] += ele
            if i == 1:
                session['months'] += ele
            if i == 2:
                session['days'] += ele

        session['years'] = int(session['years'])
        session['months'] = int(session['months'])
        session['days'] = int(session['days'])  

        return(session)
