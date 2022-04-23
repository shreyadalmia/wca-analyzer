import pandas as pd
import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Select a file")                         # for uploading chats for analysis
if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     dataset = bytes_data.decode("utf-8")                                          # converting the data into string
     df = preprocessor.preprocess(dataset)

     # st.dataframe(df)                                                              # to display the dataset

     # fetch unique users
     list_of_users = df['sender'].unique().tolist()                                # list of the users in the chat
     list_of_users.remove('group_notification')
     list_of_users.sort()                                                          # user's names in ascending order
     list_of_users.insert(0,"Overall analysis")                                    # for overall analysis of the group
     selected_sender = st.sidebar.selectbox("Show analysis wrt",list_of_users)     # drop down box for the list of users

     if st.sidebar.button("show analysis"):
          total_msg,num_words,num_media,num_links = helper.fetch_stats(selected_sender,df)
          
          st.title('Overall Comprehensive Chat Details')
          col1,col2,col3,col4 = st.columns(4)

          with col1:                                                               # column 1 -> total no of messages
               st.header("Total Number of Messages")
               st.title(total_msg)
          with col2:                                                               # column 2 -> total no of words
               st.header("Total Number of Words")
               st.title(num_words)
          with col3:                                                               # column 3 -> total no of media messages shared
               st.header("Total Number of Media")
               st.title(num_media)
          with col4:                                                               # column 4 -> total no. of links shared
               st.header("Total Number of links")
               st.title(num_links)


          #timelines
          # MONTHLY
          st.title('Monthly Analysis')                                             # Monthly analysis of a group or a particular user
          timeline = helper.monthly_ana(selected_sender,df)
          fig,ax = plt.subplots()
          ax.plot(timeline['time'], timeline['messages'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # DAILY
          st.title('Daily Analysis')                                               #  Monthly analysis of a group or a particular user
          daily_timeline = helper.daily_ana(selected_sender, df)
          fig, ax = plt.subplots()
          ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          # activity map
          # day activity
          st.title('Day Activity')                                                 # Most Busy day for a group or a particular user
          st.header("Most Busy Day")
          busy_day = helper.active_day(selected_sender,df)
          fig,ax = plt.subplots()
          ax.bar(busy_day.index,busy_day.values,color='#1BB2BB')            #DEUTERANOTIA
          plt.xticks(rotation='vertical')
          st.pyplot(fig)
          #month activity
          st.title('Monthly Activity')
          st.header("Busiest Month")
          busy_month = helper.active_month(selected_sender,df)
          fig,ax = plt.subplots()
          ax.bar(busy_month.index,busy_month.values,color='orange')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)


          st.title('Active Hours')                                                          # active hours in a day
          user_active_hours = helper.active_hours(selected_sender,df)                       # heatmap - light - active , dark - not active
          fig,ax = plt.subplots()
          ax = sns.heatmap(user_active_hours)
          st.pyplot(fig)


          # finding the most active user in the group (group level analysis)
          if selected_sender == "Overall analysis":
               st.title("Most Active Users")
               x,y= helper.most_active_users(df)
               fig,ax = plt.subplots()
               col1,col2 = st.columns(2)

               with col1:
                    ax.bar(x.index,x.values,color='#AA98A9')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(y)
          # wordcloud
          st.title("Most Used Words")
          df_wc = helper.create_wordcloud(selected_sender,df)
          fig,ax = plt.subplots()
          ax.imshow(df_wc)
          st.pyplot(fig)

          #most used words
          most_uw = helper.most_used_words(selected_sender,df)
          fig,ax = plt.subplots()
          ax.barh(most_uw[0],most_uw[1],color='purple')
          # plt.xticks(rotation='vertical')
          st.title('Statistics for Most Used Words')
          st.pyplot(fig)
          # st.dataframe(most_uw)

          # emojis
          emojis_mu = helper.mu_emojis(selected_sender,df)
          st.title("Most Used Emojis")
          col1,col2 = st.columns(2)
          with col1:
               st.dataframe(emojis_mu)
          with col2:
               fig,ax = plt.subplots()
               #ax.pie(emojis_mu[1].head(10),labels = emojis_mu[0].head(10),autopct="%0.2f")
               ax.bar(emojis_mu[0].head(10),emojis_mu[1].head(10),color='#EDA6C4')
               st.pyplot(fig)

          # sentimental analysis
          from nltk.sentiment.vader import SentimentIntensityAnalyzer
          sentiments = SentimentIntensityAnalyzer()                     # for each message we are checking its sentiment
          st.title('Sentimental Analysis')
          df["positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["messages"]]
          df["negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["messages"]]
          df["neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["messages"]]
          st.dataframe(df)


