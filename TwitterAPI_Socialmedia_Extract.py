#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:50:09 2020

@author: ronaksharma
"""

# Guide
# http://docs.tweepy.org/en/latest/
# https://github.com/tweepy/tweepy
# Tutorial: https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/social-media-text-mining-python/
# API methods: http://docs.tweepy.org/en/latest/api.html#api-reference

# Installtion of library for Anaconda
# conda install -c conda-forge tweepy
   
# Libraries
import tweepy
import re
import urllib.request 
import csv
from collections import defaultdict
#------------ Functions--------#

# Extract date and time information from a tweet
def getDateTimeOfTweet(dateTimeObject):
    date=dateTimeObject.strftime("%d %b %Y ") # Extracting date information
    time=dateTimeObject.strftime("%H:%M:%S") # Extracting time information
    return date,time


# Sanitises the URL be separating the URLs and the actual text in a Tweet
def separateUrl(tweet):
    # Regular expression to identify URLs in a tweet
    urlRegex = re.compile(r'https?://\S+|www\.\S+')   # Starts with 'https' and then continous until no whitespace is found. That is essentially the format of a URL
    url = re.findall(urlRegex,tweet)
    tweetURL=url[-1] #The last URL in a tweet is the valid image URL
    tweetWithoutURL = urlRegex.sub(r'', tweet)
    tweetWithoutURL=tweetWithoutURL.replace('\n','').replace('\t','').strip() # Removes next line character and tab spaces before encoding
    return tweetURL,tweetWithoutURL.encode('ascii', 'ignore')#Encoding only ascii characters and ignoring the rest of characters

# Downloads the images using the Twitter URL
def downloadTwitterImage(imageUrl,filenameTweet,filenameImage,imageExtension):
    urllib.request.urlretrieve(imageUrl,str(filenameTweet)+str(filenameImage)+imageExtension)

# Writes twitter data into the CSV file pointing to 'csvWriterPointer'
def writeToTwitterCSV(csvWriterPointer,serialNumber,userName,date,time,tweetWithoutURL,imageNames,mediaURL,twitterURL):
    imageNames=','.join(imageNames)
    mediaURL=','.join(mediaURL)
    csvRow=[serialNumber,userName,date,time,tweetWithoutURL,imageNames,mediaURL,twitterURL]
    csvWriterPointer.writerow(csvRow) 


#----------Creating a CSV file-------------#
filename = "Twitter_API_Result.csv"
csvFileObject = open(filename, "w")
csvWriter = csv.writer(csvFileObject)
csvFields=['S.No','Name','Date','Time','Twitter Text','Image Titles','Image URL','Tweet URL']    
csvWriter.writerow(csvFields)
#-----------------------------------------#

   
#-------------Reading credentials to access Twitter API-------------------#
# Each line is stored as an element in the list. Each element is then split
# at '=' character and then the trailing '\n' is removed.
with open('credentials.txt','r') as listOfCredentials:
   credentials=listOfCredentials.readlines()
   consumer_key=(credentials[0].split('=')[1]).strip()
   consumer_secret=(credentials[1].split('=')[1]).strip()
   access_token=(credentials[2].split('=')[1]).strip()
   access_token_secret=(credentials[3].split('=')[1]).strip()

#--------Reading hashtags to access input contraints--------------------#
with open('hashtags.txt','r') as listOfHashtags:
   hashtags=listOfHashtags.readline()
   hashtags=hashtags.split(',')
   twitterQuery=' OR '.join(hashtags)

 
#---Search Paramters-----#
twitterFilter= " -filter:retweets" + " filter:twimg"# Filtering on tweets with images and removing any retweets
finalSearchQuery=twitterQuery+twitterFilter # Final Search query consisting of hashtags and filters
startDate = "2020-07-10"
endDate="2020-07-13" # Exclusive of the date. +1 this argument to include the date
numberOfTweets=7
listOfTweets=[]
listOfUserName=[]
listOfDate=[]
listOfTime=[]
listOfTweetURL=[]
tweetImageNames=[]
dictOfMediaURL=defaultdict(list)
dictOfMediaName=dict()
uniqueIdentifierTweet=0
displayMessageCounter=1
uniqueIdenifierImage='a'

#------- Authentication and Authorisation-----------#
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True) # Using tweepy's API class
# Setting the 'rate_limit' arguments pauses the programe and notifies the user when limit reached than throwing an error

#-----Posting a Tweet-----#
#api.update_status("First tweet using #Python")

#-- Fetching Timeline data----#
#for tweet in tweepy.Cursor(api.user_timeline).items(3): # Pagination allows to specify the amount of pages to extract information from
##for tweet in publicTweets:
#    print(tweet.text)

#--- Fetching Hashtag Data-----#
listOfTweetsAttributes=tweepy.Cursor(api.search,
                                     q=finalSearchQuery, # Search Query
                                     lang='en', # Language
                                     since=startDate, until=endDate,
                                     result_type='recent', # Returns recent tweets
                                     tweet_mode='extended', # Prevent getting truncated response as the return limit is 140 characters
                                     exclude_replies=True,
                                     include_entities=True,
                                     monitor_rate_limit=True).items(numberOfTweets)

for tweet in listOfTweetsAttributes:
    #-------Processing raw date time data------------#
    tweetDate,tweetTime=getDateTimeOfTweet(tweet.created_at) # Passing Time Stamps of tweet to extract date and time
    
    #------ Sanitising tweet caption----------#
    tweetURL,tweetWithoutURL=separateUrl(tweet.full_text)

    #----- Storing the meta data in a list ------------#
    for image in  tweet.extended_entities['media']: # 'extended_entities' allows to loop through all media entities
        dictOfMediaURL[uniqueIdentifierTweet].append(image['media_url']) # Dictionary allows to store tweets assiated with multiple images
        downloadTwitterImage(image['media_url'],uniqueIdentifierTweet,uniqueIdenifierImage,".jpg")
        tweetImageNames.append(str(uniqueIdentifierTweet)+uniqueIdenifierImage)
        uniqueIdenifierImage = chr(ord(uniqueIdenifierImage) + 1)
    
    listOfDate.append(tweetDate) # Timestamp of the tweet
    listOfTime.append(tweetTime)
    listOfUserName.append(tweet.user.screen_name) #User name
    listOfTweets.append(tweetWithoutURL) # Tweet Captions
    listOfTweetURL.append(tweetURL)
    writeToTwitterCSV(csvWriter,(uniqueIdentifierTweet+1),tweet.user.screen_name,tweetDate,tweetTime,tweetWithoutURL,tweetImageNames,dictOfMediaURL[uniqueIdentifierTweet],tweetURL)
    
    #-------Counters--------#
    uniqueIdentifierTweet+=1
    uniqueIdenifierImage='a'
    displayMessageCounter+=1
    
    del tweetImageNames[:] # Delete all elements from a list in Python
    
    if(displayMessageCounter==2): # Counter to display a message every 10 tweets
        print("Tweets added to CSV file") 
        displayMessageCounter=1 # Resetting the Counter
    
csvFileObject.close()
