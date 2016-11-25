from twython import Twython
import ConfigParser, os, sys, json
import tweepy
import time
#Reading credentials from config file
CC = ConfigParser.ConfigParser()
if not os.path.exists("keys.cfg"):
    print "Cannot find keys file"
    sys.exit(1)
CC.read("keys.cfg")
url_followers = CC.get("keys", "url_followers")
url_tweets = CC.get("keys", "url_tweets")
consumer_key = CC.get("keys", "consumer_key")
consumer_secret = CC.get("keys", "consumer_secret")
auth_token = CC.get("keys", "auth_token")
auth_token_secret = CC.get("keys", "auth_token_secret")

twitter = Twython(consumer_key, consumer_secret, auth_token, auth_token_secret)

class Twitter_Followers(object):

	def get_followers(self,user_name):
		lst =[]
		try:
			followers = twitter.get_followers_list(screen_name = user_name)
		except Exception as e:
			return e
		user = followers['users']
		follower_names = [i['screen_name'] for i in user]
		#returns all names of followers
		return follower_names
		
		'''
		accountvar = user_name

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(auth_token, auth_token_secret)

		api = tweepy.API(auth)

		users = tweepy.Cursor(api.followers, screen_name=accountvar).items()
		i = 0
		while True:
			i+=1
			try:
				user = next(users)
			except tweepy.TweepError:
				time.sleep(60*15)
				user = next(users)
			except StopIteration:
				break
			lst.append(user.screen_name)
		return lst
		'''
	def common_followers(self,user_a,user_b):
		
		try:
			#calling get_follower to get all follower names
			follower_names_a = self.get_followers(user_a)
			follower_names_b = self.get_followers(user_b)
			# inner join to get common followers
			followers = list(set(follower_names_a) & set(follower_names_b))
			followers = json.dumps(followers)
			#returning list of common followers
			return followers
		except Exception as e:
			return e

class Twitter_User_Keyword(object):
	
	def tweet_keyword(self,user_name,word):
		try:
			tweets=twitter.get_user_timeline(screen_name=user_name, count=100)
		except Exception as e:
			return e
		#list of tweets with word in it
		word_in_tweet = [i['text'] for i in tweets if word.lower() in i['text'].lower()]
		#returning all tweets where word in it.
		return word_in_tweet

	