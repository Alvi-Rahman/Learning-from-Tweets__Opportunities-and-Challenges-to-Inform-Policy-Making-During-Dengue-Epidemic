import tweepy
import re


from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

CONSUMER_KEY = 'tmQA8jMSgOC7iQf5m71tnkcqI'
CONSUMER_SECRET = 'loivHciSuBh7tQYnljgVpxxUYna3dZBEYBlgQ6uxKfFXOWth7Y'
ACCESS_KEY = '1016000990489657345-FQVnuSXmuG8Q0tdmFpIh81lIdDg8B1'
ACCESS_SECRET = 'tuzca8muwJvKM1evnnY0CYCvEfb9n7mXF7ckCMwcp5YLw'

class TweetListener(StreamListener):
    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

#set wait_on_rate_limit so that program doesn't terminate erverytime
auth = tweepy.AppAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

#auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterStream = Stream(auth,TweetListener())

f=open('C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\fnfUser.txt','r', encoding='utf-8')
allusers=f.readlines()
f.close()

fnf=open('C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\fnf.txt',"w", encoding="UTF-16")


following_whom=[]
followed_by_whom=[]
mutual_friends=[]

#removing \n from the end of each str id
allusers=[s.replace('\n','') for s in allusers]


for f in range(15367,16001):

	print(f)
    
	try:
        
		friends=api.friends_ids(allusers[f])
		followers=api.followers_ids(allusers[f])

		#converting int ids to str ids
		friends=[str(i) for i in friends]
		followers=[str(i) for i in followers]

		#mutual friends follow one another
		mutual_friends=list(set(followers).intersection(friends))
		mutual_friends=list(set(allusers).intersection(mutual_friends))

		for m in range(len(mutual_friends)):
			fnf.write(allusers[f]+'\t'+mutual_friends[m]+'\n')
			fnf.write(mutual_friends[m]+'\t'+allusers[f]+'\n')

		#following
		following_whom=list(set(friends).intersection(allusers))
		following_whom=list(set(following_whom)-set(mutual_friends))

		for m in range(len(following_whom)):
			fnf.write(allusers[f]+'\t'+following_whom[m]+'\n')

		#followed by
		followed_by_whom=list(set(followers).intersection(allusers))
		followed_by_whom=list(set(followed_by_whom)-set(mutual_friends))

		for m in range(len(followed_by_whom)):
			fnf.write(followed_by_whom[m]+'\t'+allusers[f]+'\n')

	except tweepy.error.TweepError:
		continue


fnf.close()

