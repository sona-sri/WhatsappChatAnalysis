# helper.py
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
from urlextract import URLExtract
import emoji
from emoji_utils import get_emoji_data  # or import emoji directly

extract = URLExtract()


def show_stats(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media = df[df['message'] == '<Media omitted>'].shape[0]
    links = []
    for msg in df['message']:
        links.extend(extract.find_urls(msg))

    return num_messages, len(words), num_media, len(links)


def busy_users(df):
    x = df['user'].value_counts().head(6)
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x, df


def create_word_cloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=300, height=300, background_color='white', min_font_size=10)
    temp['message'] = temp['message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'All Users':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.extend(message.split())

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


