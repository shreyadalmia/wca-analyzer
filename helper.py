#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from urlextract import URLExtract                                      # import urlextract for extracting links from data
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_sender,df):
    if selected_sender != "Overall analysis":                           # analysis for a single user
        df =  df[df['sender'] == selected_sender]
    # overall analysis of the group
    total_msg = df.shape[0]                                             # total number of messages
    num_words = 0                                                       # num_words -> total number of words
    for msg in df['messages']:
        num_words = num_words + len(msg.split())
    num_media = df[df['messages'] == '<Media omitted>\n'].shape[0]      # number of media messages used
    lk =[]
    for msg in df['messages']:
        lk.extend(extract.find_urls(msg))
    num_links = len(lk)                                                 # number of links shared
    return total_msg, num_words,num_media,num_links

def most_active_users(df):
    x = df['sender'].value_counts().head()
    y = round((df['sender'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'User Name', 'sender': 'Percentage'})
    return x,y

def create_wordcloud(selected_sender,df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    if selected_sender != "Overall analysis":
        df = df[df['sender'] == selected_sender]
    temp = df[df['sender'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    def remove_sw(messages):
        y1=[]
        for word in messages.lower().split():
            if word not in stop_words:
                y1.append(word)
        return " ".join(y1)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_sw)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_used_words(selected_sender, df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    if selected_sender != "Overall analysis":
        df = df[df['sender'] == selected_sender]
    temp = df[df['sender'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words = []
    for messages in temp['messages']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)
    most_uw = pd.DataFrame(Counter(words).most_common(20))
    return most_uw

def mu_emojis(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    emojis= []
    for messages in df['messages']:
        emojis.extend([c for c in messages if c in emoji.UNICODE_EMOJI['en']])
    emojis_mu = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emojis_mu

def monthly_ana(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time']= time
    return timeline

def daily_ana(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    return daily_timeline

def active_day(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    return df['day_name'].value_counts()

def active_month(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    return df['month'].value_counts()

def active_hours(selected_sender,df):
    if selected_sender != 'Overall analysis':
        df = df[df['sender'] == selected_sender]
    user_active_hours = df.pivot_table(index='day_name',columns='period',values='messages',aggfunc='count').fillna(0)
    return user_active_hours

