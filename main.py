import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from textblob import TextBlob
import spacy
from gensim.summarization import summarize


st.title("Sentiment Analysis of Tweets on COVID19 and Depression (COVIDEP)")
st.sidebar.title("Sentiment Analysis of Tweets on COVID19 and Depression (COVIDEP)")

st.markdown("Analysing the sentiments during COVID19 pandemic and how it affects the mental health during the pandemic period")
st.sidebar.markdown("Analysing the sentiments during COVID19 pandemic and how it affects the mental health during the pandemic period")

DATA_URL = ("covidep_processed_final.csv")
def load_data():
    data = pd.read_csv(DATA_URL)
    data['tweetcreatedts'] = pd.to_datetime(data['tweetcreatedts'])
    return data

data = load_data()
def main():

        if st.subheader("Analyse Your Tweet!"):

            message = st.text_area("Enter Text","Type Here ..")
            if st.button("Analyse"):
                blob = TextBlob(message)
                result_sentiment = blob.sentiment
                st.success(result_sentiment)

if __name__ == '__main__':
    main()

st.sidebar.subheader("Example of tweets")
random_tweet = st.sidebar.radio('Choose Twitter Sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('sentiment == @random_tweet')[["clean_tweet"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### Number of tweets by sentiment")
sentiment_count = data['sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})
st.markdown("### Number of tweets by sentiment")
fig = px.bar(sentiment_count,x='Sentiment', y='Tweets', color='Tweets', height=600)
st.plotly_chart(fig)
    


st.sidebar.header("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))
st.header('Word cloud for %s sentiment' % (word_sentiment))
df = data[data['sentiment']==word_sentiment]
words = ' '.join(df['clean_tweet'])
processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
plt.imshow(wordcloud)
plt.xticks([])
plt.yticks([])
st.pyplot()
