import pandas as pd
import re

def preprocess(dataset):
    pattern1 = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s\D{2}\s-\s'
    processed_messages = re.split(pattern1, dataset)[1:]

    regular_exp_date = '(\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s)(AM|PM)\s-\s'
    date = re.findall(regular_exp_date, dataset)
    df = pd.DataFrame({'chats': processed_messages, 'date': date})
    # df['date'] = pd.to_datetime(df['date'])
    df['date'] = df['date'].apply(lambda x: pd.to_datetime(x[0]))

    sender = []
    messages = []
    for message in df['chats']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            sender.append(entry[1])
            messages.append(entry[2])
        else:
            sender.append('group_notification')
            messages.append(entry[0])
    df['sender'] = sender
    df['messages'] = messages

    df['only_date'] = df['date'].dt.date                   # date
    df['year'] = df['date'].dt.year                        # year
    df['month_num'] = df['date'].dt.month                  # month number
    df['day'] = df['date'].dt.day                          # day
    df['day_name'] = df['date'].dt.day_name()              # day name
    df['month'] = df['date'].dt.month_name()               # month name
    df['hour'] = df['date'].dt.hour                        # hour
    df['minute'] = df['date'].dt.minute                    # minutes

    # for period of time
    period = []
    for hour in df[['day_name','hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str(00) + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df

