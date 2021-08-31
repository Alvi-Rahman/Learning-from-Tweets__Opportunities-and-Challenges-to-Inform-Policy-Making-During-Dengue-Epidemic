import csv
import os
import json
import codecs
import re

files=os.listdir(path='C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\TweetScraper-master\\Data\\data_bangladesh_dengue')

idf=open("data_ID.txt", mode="w")
useridf=open("data_user_id.txt", mode="w")
output_file=open("data_tweet.csv", mode="w")


fieldnames = ["usernameTweet", "ID", "text", "url", "nbr_retweet", "nbr_favorite","nbr_reply","datetime","has_media", "medias", "is_reply", "is_retweet","user_id"]
writer = csv.DictWriter(output_file, fieldnames=fieldnames, delimiter=';')

writer.writeheader()
idf.writelines("ID\n")
useridf.writelines("user_id\n")

for fname in files:

    f=open('C:\\Users\\Alvi Rahman\\Desktop\\Farhana Miss\\TweetScraper-master\\Data\\data_bangladesh_dengue\\'+fname)
    data=json.load(f)
    f.close()

    fulltext=data['text']
    fulltext=fulltext.replace('\b',' ')
    fulltext=fulltext.replace('\n',' ')
    fulltext=fulltext.replace('\t',' ')
    fulltext=fulltext.replace('\r',' ')
    fulltext=fulltext.replace('\f',' ')
    fulltext=re.sub(' +',' ',fulltext)

    data['text']=fulltext

    writer.writerow(data)
    idf.writelines(data['ID']+"\n")
    useridf.writelines(data['user_id']+"\n")

        
idf.close()
useridf.close()
output_file.close()
    