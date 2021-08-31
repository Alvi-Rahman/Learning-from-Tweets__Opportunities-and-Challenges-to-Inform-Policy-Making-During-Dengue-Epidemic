import tweepy
import csv
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

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth)

auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterStream = Stream(auth,TweetListener())


f=open('C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\allUser.txt',"r")
allusers=f.readlines()
f.close()

csv_file= open("twitter_users.tsv", mode="w",encoding="UTF-16")
fieldnames = ["name", "ID", "location", "followers", "friends","statuses"]
writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter='\t')

writer.writeheader()

for id in range(len(allusers)):
    try:
        usid=allusers[id].replace('\n','')
        user=api.get_user(usid)
        writer.writerow({'name':user.screen_name, 'ID': str(user.id_str), 'location': user.location, 'followers':str(user.followers_count),'friends':str(user.friends_count),'statuses':str(user.statuses_count)})
    except:
        writer.writerow({'name':'xxxx', 'ID': str(usid), 'location': 'xxxx', 'followers':'xxxx','friends':'xxxx','statuses':'xxxx'})
        continue