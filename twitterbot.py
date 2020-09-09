# Program goes into twitter user ProblemSet1 and responds to tweets (previously not responded to by @ProblemSet1) from @FreedoniaNews expressing certain political opinions.
# Uses Tweepy for authorization, to fetch tweets, and to respond. Uses Vader for sentiment analysis. 

import tweepy
import tkinter 
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer




def mainFunction():
# format for authorization from https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607
	consumer_key = #redacted
	consumer_secret = #redacted
	access_token = #redacted
	access_token_secret = #redacted 

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

# checks for correct authorization of user 
	user = api.me()
# print(user.name)
	
# create lists for tweets I have responded to and tweets from freedonianews
	my_responded_tweets = []
	theirtweets = [] 

# fetch tweets, store id (use to check if responded) and text
# tweepy cursor usage from https://medium.freecodecamp.org/creating-a-twitter-bot-in-python-with-tweepy-ac524157a607
	for tweet in tweepy.Cursor(api.user_timeline, screen_name="ProblemSet1").items(50):
		try:
			my_responded_tweets.append(tweet.in_reply_to_status_id_str)
			# print("found a tweet in response to " + tweet.in_reply_to_status_id_str + " \n")
		except: 
			#do nothing 
			r = 1
			# print("didn't work 1.0\n")
	for tweet in tweepy.Cursor(api.user_timeline, screen_name="FreedoniaNews").items(50):
		try: 
			tweetID = tweet.id_str
			# username = "@freedonianews"
			tweettext = tweet.text
			# print("analysing tweet with id " + tweetID + " \n")
		except:
		 	# do nothing 
		 	r = 1 
			# print("didn't work 2.0\n")

# checks for tweets I have already responded to and makes sure that isn't putting in duplicates 
		if (not ((tweetID in theirtweets) or (tweetID in my_responded_tweets))):
			# print("putting tweetid " + str(tweetID) + " into list\n") 
			theirtweets.append(tweetID)
			theirtweets.append(tweettext)

# Create bank of tweets for responding 
	pro_Sylvania = ["@FreedoniaNews This is ridiculous! Sylvania is perhaps the greatest country ever to exist.", "@FreedoniaNews Utter baffonery. This falsehood has no place in our news. Sylvania is great.", "@FreedoniaNews Astonishing that a NEWS service would tweet something so blatantly false. SAD. Sylvania is great.", "@FreedoniaNews Hail Sylvania, the greatest country ever to exist. Seems like #fakenews to me.", "@FreedoniaNews Horrible journalism--cannot believe someone would say this about Sylvania. SAD.", "@FreedoniaNews Makes me so sad to read this terrible journalism, clouding the greatness of Sylvania.", "@FreedoniaNews Nice try, but Sylvania's great reputation will not be tarnished by this sorry excuse for journalism."]
	pro_Trentino = ["@FreedoniaNews Why would someone say something so false about Trentino. One of the greatest ambassadors to ever live", "@FreedoniaNews Fact check: this is very false. Trentino has been one of the most productive and successful ambassadors ever.", "@FreedoniaNews Nobody who has met Trentino could possibly believe this--an amazing person with great leadership.", "@FreedoniaNews Trentino is an amazing leader. Great style, great face, and the grace of a unicorn.", "@FreedoniaNews Trentino's leadership is the only thing that will return us to greatness. Cannot believe what some people are saying about him.", "@FreedoniaNews This is so false. Trentino is amazing--free sandwich in my shop anytime!", "@FreedoniaNews Trentino--what a bro! Dude has saved my life at least 100 times. No idea why anyone wouldn't like him."]
	anti_Freedonia = ["@FreedoniaNews I can't fathom why someone would say this about Freedonia. What a terrible place--unemployment at 28 percent and some of the most vicious politics ever.", "@FreedoniaNews Freedonia is very gross.", "@FreedoniaNews Freedonia is responsible for the international trade wars and global economic downturn. Don't believe anything positive you hear about Freedonia!", "@FreedoniaNews Freedonia is full of drunk losers. Would never go there.", "@FreedoniaNews Freedonia the land of the free and the brave? I think not. More like the land of the stupid.", "@FreedoniaNews Freedonia literally is run by comedians.", "@FreedoniaNews Horrible reporting. Hope this gets taken down. Freedonia is garbage."]
	anti_Rufus = ["@FreedoniaNews Rufus T Firefly is a complete idiot. He should be fired immediately", "@FreedoniaNews Firefly's record speaks for itself--economic downturn, restriction of the peoples' rights, and more. Never trust him.", "@FreedoniaNews I have a proposal. How about we make a TV program all the old white men like Rufus T Firefly have to watch instead of ruining their country.", "@FreedoniaNews Firefly likes the word moist--can't trust people like that.", "@FreedoniaNews"]
	
# Iterate through tweets in "theirtweets" which has only tweets I have not yet responded to. Note that 0, 2, 4, 6... index tweetIDs and 1, 3, 5, 7... index tweet text. 
	for i in range((len(theirtweets))//2):
# Set tweettext and tweetid variables
		tweet_text = theirtweets[(2 * i) + 1]
		tweet_id = theirtweets[(2 * i)]
		# print(tweet_text + " " + tweet_id + str(int(tweet_id)) + "\n")

# Analyze positivity or negativity of tweet, set as score variable from -1 to 1
		score = SentimentIntensityAnalyzer().polarity_scores(tweet_text)["compound"]

# Check for subject of tweet, pick random tweet from responses, and update status 
		if "Sylvania" in tweet_text: 
			if score < 0:
				random_num = random.randint(0, (len(pro_Sylvania) - 1))
				to_tweet_text = pro_Sylvania[random_num]
				api.update_status(status=to_tweet_text, in_reply_to_status_id=int(tweet_id))
			#elif score > 0:
			#	print("dont need to respond to positive tweet about sylvania\n")

		elif "Trentino" in tweet_text: 
			if score < 0:
				random_num = random.randint(0, (len(pro_Trentino) - 1))
				to_tweet_text = pro_Trentino[random_num]
				api.update_status(status=to_tweet_text, in_reply_to_status_id=int(tweet_id))
			#elif score > 0: 
			#	print("dont need to respond to positive tweet about trentino\n")

		elif "Freedonia" in tweet_text: 
			#if score < 0: 
			#	print("dont need to respond to negative tweet about freedonia\n")
			if score > 0:
				random_num = random.randint(0, (len(anti_Freedonia) - 1))
				to_tweet_text = anti_Freedonia[random_num]
				api.update_status(status=to_tweet_text, in_reply_to_status_id=int(tweet_id))
				
		elif "Firefly" in tweet_text: 
			#if score < 0: 
			#	print("dont need to respond to negative tweet about firefly\n")
			if score > 0: 
				random_num = random.randint(0, (len(anti_Rufus) - 1))
				to_tweet_text = anti_Rufus[random_num]
				api.update_status(status=to_tweet_text, in_reply_to_status_id=int(tweet_id))
				
# run mainFunction 
mainFunction()