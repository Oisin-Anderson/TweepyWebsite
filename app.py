import tweepy
from flask import Flask, render_template, request
import os
import tweepy as tp
import pandas as pd
from textblob import TextBlob
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['CSV_FOLDER'] = 'static/CSV'

consumer_key = '7QYQH7qf0q9Lk3XNChkoJpWtQ'
consumer_secret = '8URqQMLRulnBZ2zBg6INwgBcSy1n2nmqcivQrLevgOXLBuVoLd'
access_token = '1440589430016729096-4foIMmmDWo3HlPX4F118EgV3MP43bL'
access_token_secret = 'nCdz73VOiNPH1V4QVZsnwvRdlOMxAFahvUMQWSuqdNcC0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


vpositive_tweets = []
vnegative_tweets = []
vneutral_tweets = []
tpositive_tweets = []
tnegative_tweets = []
tneutral_tweets = []
dpositive_tweets = []
dnegative_tweets = []
dneutral_tweets = []
bubbleChart = []
userName1 = []
userLocation1 = []


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/reset')
def reset():
    positive_tweets.clear()
    negative_tweets.clear()
    neutral_tweets.clear()
    return render_template('about.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/drill')
def drill():
    return render_template('drilldown.html')


@app.route('/dd', methods=['POST'])
def dd():
    if request.method == 'POST':
        print("here")
        query_one = "trump"
        tweets = tp.Cursor(api.search_tweets, q=query_one, lang="en", result_type="popular").items(50)
        sid_obj = SentimentIntensityAnalyzer()

        for tweet in tweets:
            print(tweet.text)
            sentiment_dict = sid_obj.polarity_scores(tweet.text)

            if sentiment_dict['compound'] >= 0.25:
                dpositive_tweets.append(tweet)
            elif sentiment_dict['compound'] <= - 0.25:
                dnegative_tweets.append(tweet)
            else:
                dneutral_tweets.append(tweet)

        dpos = len(dpositive_tweets)
        dneg = len(dnegative_tweets)
        dneu = len(dneutral_tweets)

        posname1 = dpositive_tweets[0].user.name
        posname2 = dpositive_tweets[1].user.name
        posname3 = dpositive_tweets[2].user.name
        posname4 = dpositive_tweets[3].user.name

        posfol1 = dpositive_tweets[0].user.followers_count
        posfol2 = dpositive_tweets[1].user.followers_count
        posfol3 = dpositive_tweets[2].user.followers_count
        posfol4 = dpositive_tweets[3].user.followers_count

        neuname1 = dneutral_tweets[0].user.name
        neuname2 = dneutral_tweets[1].user.name
        neuname3 = dneutral_tweets[2].user.name
        neuname4 = dneutral_tweets[3].user.name

        neufol1 = dneutral_tweets[0].user.followers_count
        neufol2 = dneutral_tweets[1].user.followers_count
        neufol3 = dneutral_tweets[2].user.followers_count
        neufol4 = dneutral_tweets[3].user.followers_count

        negname1 = dnegative_tweets[0].user.name
        negname2 = dnegative_tweets[1].user.name
        negname3 = dnegative_tweets[2].user.name
        negname4 = dnegative_tweets[3].user.name

        negfol1 = dnegative_tweets[0].user.followers_count
        negfol2 = dnegative_tweets[1].user.followers_count
        negfol3 = dnegative_tweets[2].user.followers_count
        negfol4 = dnegative_tweets[3].user.followers_count

    return render_template('drilldown.html', pos=dpos, neg=dneg, neu=dneu,
                           posname1=posname1, posname2=posname2, posname3=posname3, posname4=posname4,
                           negname1=negname1, negname2=negname2, negname3=negname3, negname4=negname4,
                           neuname1=neuname1, neuname2=neuname2, neuname3=neuname3, neuname4=neuname4,
                           posfol1=posfol1, posfol2=posfol2, posfol3=posfol3, posfol4=posfol4,
                           negfol1=negfol1, negfol2=negfol2, negfol3=negfol3, negfol4=negfol4,
                           neufol1=neufol1, neufol2=neufol2, neufol3=neufol3, neufol4=neufol4, )


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        print("here")
        query_one = request.form["input_one"]
        tweets = tp.Cursor(api.search_tweets, q=query_one, lang="en", result_type="popular").items(50)
        sid_obj = SentimentIntensityAnalyzer()

        for tweet in tweets:
            print(tweet.text)
            sentiment_dict = sid_obj.polarity_scores(tweet.text)
            print("Overall sentiment dictionary is : ", sentiment_dict)
            print("sentence was rated as ", sentiment_dict['neg'] * 100, "% Negative")
            print("sentence was rated as ", sentiment_dict['neu'] * 100, "% Neutral")
            print("sentence was rated as ", sentiment_dict['pos'] * 100, "% Positive")

            print("Sentence Overall Rated As", end=" ")

            if sentiment_dict['compound'] >= 0.25:
                vpositive_tweets.append(tweet)
                print("Positive")

            elif sentiment_dict['compound'] <= - 0.25:
                vnegative_tweets.append(tweet)
                print("Negative")

            else:
                vneutral_tweets.append(tweet)
                print("Neutral")

            vpos = len(vpositive_tweets)
            vneg = len(vnegative_tweets)
            vneu = len(vneutral_tweets)

            dict = {"name": tweet.user.name, "location": tweet.user.location}
            bubbleChart.append(dict)

            userName1.append(tweet.user.name)
            userLocation1.append(tweet.user.location)

            analysis = TextBlob(tweet.text)
            print(analysis.sentiment)

            if analysis.sentiment[0] >= 0.25:
                tpositive_tweets.append(tweet)
                print('Positive')
            elif analysis.sentiment[0] <= 0.25:
                tnegative_tweets.append(tweet)
                print('Negative')
            else:
                tneutral_tweets.append(tweet)
                print('Neutral')

            tpos = len(tpositive_tweets)
            tneg = len(tnegative_tweets)
            tneu = len(tneutral_tweets)

            print('*************')
            print(tweet.user)
            print(userName1[0])
            print(userLocation1[0])
            print('*************')

    return render_template('chart.html', vpositive=vpos, vnegative=vneg, vneutral=vneu, tpositive=tpos, tnegative=tneg, tneutral=tneu, data=bubbleChart)


if __name__ == '__main__':
    app.run(debug=True)
