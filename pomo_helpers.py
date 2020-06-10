def statistics(user_data):
    total_tomatoes = 0
    stats = {}
    day_count = 0
    for row in user_data:
        total_tomatoes += row['tomato_count']
        day_count += 1

    stats['total_tomatoes'] = total_tomatoes
    stats['daily_average'] = round(total_tomatoes/day_count, 2)

    return (stats)
