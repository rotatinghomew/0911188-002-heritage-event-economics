def lookup(events, key):
    event = next((row for row in events if row['id'] == key), None)
    if event is None:
        raise ValueError('没有该活动')
    return event


def billable(event):
    return event['state'] == 'held'
