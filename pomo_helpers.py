def statistics(user_data):
    total_tomatoes = 0
    stats = {}
    day_count = 0
    days_in_a_row = 0

    for row in user_data:
        total_tomatoes += row['tomato_count']
        day_count += 1
        if row['tomato_count'] > 0:
            days_in_a_row += 1
        else:
            days_in_a_row = 0

    stats['total_tomatoes'] = total_tomatoes
    stats['daily_average'] = round(total_tomatoes/day_count, 2)
    stats['days_in_a_row'] = days_in_a_row

    return (stats)
