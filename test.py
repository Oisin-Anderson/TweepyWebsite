import tweepy

# Consumer keys and access tokens, used for OAuth
consumer_key = '7QYQH7qf0q9Lk3XNChkoJpWtQ'
consumer_secret = '8URqQMLRulnBZ2zBg6INwgBcSy1n2nmqcivQrLevgOXLBuVoLd'
access_token = '1440589430016729096-4foIMmmDWo3HlPX4F118EgV3MP43bL'
access_token_secret = 'nCdz73VOiNPH1V4QVZsnwvRdlOMxAFahvUMQWSuqdNcC0'

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Sample method, used to update a status
api.update_status('Hello Python Central!')
