from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=df[df['Contact']==selected_user] #separate users dataframe
    num_message=df.shape[0]                 #number of messages

    words=[]
    for m in df['Message']:
        words.extend(m.split())             #number of words
    
    num_media=df[df['Message']=='<Media omitted>'].shape[0]  #number of media shared
    
    extractor=URLExtract()
    urls=[]
    for m in df['Message']:
        urls.extend(extractor.find_urls(m))    #number of urls
    
    return num_message,len(words),num_media,len(urls)


def fetch_most_busy_users(df):
    x=df['Contact'].value_counts().head()
    df_most_busy=round((df['Contact'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'Contact':'Name','count':'Percent'})
    return x,df_most_busy

def create_word_cloud(selected_user,df):
 
    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]    #separate users dataframe

    temp = df[df['Contact'] != 'group_notfication']
    temp = temp[temp['Message'] != '<Media omitted>']

    def remove_stopwords(text):
        l=[]
        for word in text.lower().split():
            if word not in stop_words:
                l.append(word)
        return " ".join(l)
    
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message']=temp['Message'].apply(remove_stopwords)
    df_wc = wc.generate(temp['Message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    temp = df[df['Contact'] != 'group_notfication']
    temp = temp[temp['Message'] != '<Media omitted>']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Count'])

    return emoji_df



def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    timeline = df.groupby(['Year','Month_num','Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['Message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['Contact'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='Message',aggfunc='count').fillna(0)

    return user_heatmap