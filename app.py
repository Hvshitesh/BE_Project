import streamlit as st
import preprocessor, helper, sentiment
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from streamlit_lottie import st_lottie
import time

st.set_page_config(layout='wide', page_title='Whatsapp Chat Analyzer')
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['Contact'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'Overall')
    selected_user = st.sidebar.selectbox("Analysis With Respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        st.snow()
        num_messages, num_words, num_media, num_urls = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_urls)

        timeline = helper.monthly_timeline(selected_user, df)
        st.title("Monthly TimeLine")
        fig, ax = plt.subplots()
        ax.plot(timeline['Month'], timeline['Message'], color='red')
        plt.title("Monthly Message Timeline")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Messages")

        plt.xticks(rotation="vertical")
        plt.xticks(rotation="horizontal")
        st.pyplot(fig)

        daily_timeline = helper.daily_timeline(selected_user, df)
        st.title("Daily TimeLine")
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['Message'], color='#795548')
        plt.title("Daily Message Timeline")
        ax.set_xlabel("Date")
        ax.set_ylabel("Number of Messages")

        plt.xticks(rotation=45)
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9', '#E57373', '#47D1B5']
            ax.bar(busy_day.index, busy_day.values, color=custom_colors)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color=['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A',
                                                               '#A64AC9', '#E57373', '#42A5F5', '#FF9800',
                                                               '#4CAF50', '#FF5722', '#9C27B0', '#795548'])
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)

        # Check if user_heatmap is empty
        if user_heatmap.empty:
            st.warning("No data available to display the heatmap.")
        else:
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap, cmap='viridis')
            st.pyplot(fig)

        if selected_user == "Overall":
            st.title('Most Busy Users 🗽')
            df_most_busy = helper.fetch_most_busy_users(df)
            x = df_most_busy.index

            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)
            with col1:
                custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9']
                ax.bar(x, x.values, color=custom_colors)

                plt.xticks(rotation=45)
                st.pyplot(fig)

            with col2:
                st.dataframe(df_most_busy)

        st.title("Word Cloud ☁")
        Word_Cloud = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(Word_Cloud)
        st.pyplot(fig)

        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9']
        ax.barh(most_common_df[0], most_common_df[1], color=custom_colors)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            custom_colors = ['#F2C53D', '#6BBE45', '#2AABE2', '#F95D6A', '#A64AC9']
            ax.barh(emoji_df['Emoji'].head(), emoji_df['Count'].head(), color=custom_colors)
            plt.xticks(rotation=45)
            st.pyplot(fig)

        st.title("Sentiment Analysis")
        df_sentiment = sentiment.polarity_score(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_sentiment)
        with col2:
            l = [np.mean(df_sentiment['Negative']), np.mean(df_sentiment['Neutral']),
                 np.mean(df_sentiment['Positive'])]
            labels = ['Negative', 'Neutral', 'Positive']
            fig, ax = plt.subplots(figsize=(4, 6))
            ax.pie(l, labels=labels, autopct='%1.1f%%', startangle=140, colors=['red', 'gray', 'green'])
            ax.axis('equal')
            st.pyplot(fig)
else:
    url = "https://assets9.lottiefiles.com/packages/lf20_M9p23l.json"
    lottie_json = requests.get(url).json()
    st_lottie(lottie_json, loop=True)
