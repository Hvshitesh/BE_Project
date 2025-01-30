import re
import pandas as pd
def preprocess(data):
    pattern='\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{1,2}\s?(?:am|pm)\s-\s'
    messages=re.split(pattern, data)[1:]
    dates=re.findall(pattern,data)
    date = [s.replace('\u202f', ' ') for s in dates]
    date_col=[]
    time_col=[]
    for item in date:
        parts = item.strip().split(', ')
        if len(parts) == 2:
            date_str = parts[0]
            time_str=parts[1].strip(' - ')
            date_col.append(date_str)
            time_col.append(time_str)
    messages = [s.replace('\n', '') for s in messages]
    df = pd.DataFrame({'Message':messages,'Date':date_col,'Time':time_col})
    df['Date']=pd.to_datetime(df['Date'], format='%d/%m/%y')

    #separate users and messages
    users=[]
    messages=[]
    for message in df['Message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]: #user_name
                users.append(entry[1])
                messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['Contact']=users
    df['Message']=messages
    df['Time'] = pd.to_datetime(df['Time']).dt.time
    df['Day']=df['Date'].dt.day
    df['Month']=df['Date'].dt.month_name()
    df['Month_num'] = df['Date'].dt.month
    df['Year']=df['Date'].dt.year
    df['hour'] = df['Time'].apply(lambda x: x.hour)
    df['Minute'] = df['Time'].apply(lambda x: x.minute)
    df['only_date'] = df['Date'].dt.date
    df['day_name'] = df['Date'].dt.day_name()

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period


    return df