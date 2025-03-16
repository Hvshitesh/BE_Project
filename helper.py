import pandas as pd
import calendar
from collections import Counter
import emoji

def preprocess_data(df):
    # Preprocess the DataFrame as needed
    df['Message'] = df['Message'].str.replace('\n', ' ')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Ensure Date is in datetime format
    return df

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    num_messages = df.shape[0]
    num_words = df['Message'].str.split().str.len().sum()
    num_media = df[df['Message'] == '<Media omitted>'].shape[0]
    num_urls = df['Message'].str.contains('http').sum()
    
    return num_messages, num_words, num_media, num_urls

def fetch_most_busy_users(df):
    user_activity = df['Contact'].value_counts()  # Count messages per user
    most_busy_users = user_activity.head()  # Get the top users
    return most_busy_users  # Return the Series directly

def create_word_cloud(selected_user, df):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]

    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'].tolist())
    
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_messages)

    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # Hide the axes
    plt.show()
    return wordcloud

def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    df['Month_num'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    timeline = df.groupby(['Year', 'Month_num']).count()['Message'].reset_index()
    timeline['Month'] = timeline['Month_num'].apply(lambda x: calendar.month_name[x])
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    df['Date'] = df['Date'].dt.date
    daily_timeline = df.groupby('Date').count()['Message'].reset_index()
    daily_timeline.columns = ['only_date', 'Message']
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Ensure Date is in datetime format
    df['Weekday'] = df['Date'].dt.day_name()  # Get the name of the weekday

    week_activity = df.groupby(['Weekday']).count()['Message'].reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    return week_activity

def month_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    df['Month'] = df['Date'].dt.month_name()  # Get the name of the month
    month_activity = df.groupby('Month').count()['Message'].reindex(calendar.month_name[1:])  # Reindex to ensure all months are included
    return month_activity

def activity_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    df['Hour'] = df['Date'].dt.hour  # Extract hour from Date
    df['Day'] = df['Date'].dt.day_name()  # Extract day name from Date
    heatmap_data = df.groupby(['Day', 'Hour']).count()['Message'].unstack(fill_value=0)  # Create heatmap data
    return heatmap_data

def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'].tolist())
    
    # Split the messages into words and count occurrences
    words = all_messages.split()
    most_common = Counter(words).most_common(10)  # Get the 10 most common words
    
    # Separate words and counts for plotting
    common_words, counts = zip(*most_common)
    return list(common_words), list(counts)

def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['Contact'] == selected_user]
    
    # Combine all messages into a single string
    all_messages = ' '.join(df['Message'].tolist())
    
    # Count emojis in the messages
    emoji_count = Counter(c for c in all_messages if c in emoji.UNICODE_EMOJI['en'])
    
    # Convert the Counter to a DataFrame for easier plotting
    emoji_df = pd.DataFrame(emoji_count.items(), columns=['Emoji', 'Count'])
    return emoji_df
