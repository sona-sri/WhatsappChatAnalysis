import re
import pandas as pd

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2} -'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    #creating dataframes
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = df['date'].str.rstrip(' -')
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %H:%M')
    df['date'] = df['date'].dt.strftime('%d/%m/%y %H:%M:%S')

    # Initialize lists 
    users = []
    messages = []

    # Process each message
    for message in df['user_message']:
        entry = re.split(r'(?<=\S):\s', message, maxsplit=1)
        if len(entry) == 2:
            users.append(entry[0])
            messages.append(entry[1].strip())
        else:
            users.append('group_notification')
            messages.append(entry[0].strip())
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # converting into date format
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y %H:%M:%S')
    #df['date'] = pd.to_datetime(df['date_column'], format='%Y-%m-%d %H:%M:%S'

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
