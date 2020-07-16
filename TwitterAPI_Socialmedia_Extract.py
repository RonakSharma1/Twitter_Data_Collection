#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:50:09 2020

@author: ronaksharma
"""
#-------Python Libraries-------#
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
    
# Sanitises the Twitter Text by be separating the URL of Tweet and removing any other URLs within the Tweet
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

# Creating and storing any twitter errors in a text file
def logTwitterError(twitterIndex, error):
    errorPointer=open('Error_Log.txt','a')
    writeToFile=str(twitterIndex)+"\t"+error+"\n"
    errorPointer.write(writeToFile)
    errorPointer.close()

# Resets and increments some variables required to correctly store the Twitter Data
def counterResetter(tweetIndex,tweetImageIndex,imageName):
    tweetIndex+=1 #Twitter Count incremented to store other tweets
    tweetImageIndex='a'#Re-initiliased to 'a' assuming that the whole tweet has an error instead of a single image
    del imageName[:] # Re-initialised the image names assuming the whole tweet will fail instead of just a single image
    return tweetIndex,tweetImageIndex,imageName

print("-"*10,"Twitter Media Extraction Programme","-"*10)

#----------Creating a CSV file-------------#
filename = "Twitter_API_Result.csv"
csvFileObject = open(filename, "w")
csvWriter = csv.writer(csvFileObject)
csvFields=['S.No','Name','Date','Time','Twitter Text','Image Titles','Image URL','Tweet URL']    
csvWriter.writerow(csvFields)
#-----------------------------------------#

open("Error_Log.txt", "w").close() # Deleting all the erros from any previous sessions
   
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
   
#---User Input Paramters-----#
twitterFilter= " -filter:retweets" + " filter:twimg"# Filtering on tweets with images and removing any retweets
finalSearchQuery=twitterQuery+twitterFilter # Final Search query consisting of hashtags and filters
startDate = input("\nEnter the start date for the search(YY-MM-DD)\n") # Date to start searching the Twitter database
endDate=input("\nEnter the end date(exclusive) for the search(YY-MM-DD)\n") # Exclusive of the date. +1 this argument to include the date
numberOfTweets=int(input("\nEnter the number of tweets you want to store\n"))

#--- Initialising Data Structures for Twitter Data----#
tweetImageNames=[]
dictOfMediaURL=defaultdict(list)
authorisationFailure=0

#--- Initialising Counters-----#
uniqueIdentifierTweet=1
uniqueIdenifierImage='a'

#------- Authentication and Authorisation-----------#
auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

try:
    auth.get_authorization_url()
except tweepy.TweepError as twitterError: # Raise authentication failure if an error occurs here
    authorisationFailure=1
    logTwitterError(uniqueIdentifierTweet,twitterError.reason)

if(authorisationFailure==0):
    # Setting the 'rate_limit' arguments pauses the programe and notifies the user when limit reached than throwing an error
    api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True,compression=True) # Using tweepy's API class
    
    #--- Fetching Twitter query data-----#
    listOfTweetsAttributes=tweepy.Cursor(api.search,
                                         q=finalSearchQuery, # Search Query
                                         lang='en', # Language
                                         since=startDate, until=endDate,
                                         result_type='recent', # Returns recent tweets
                                         tweet_mode='extended', # Prevent getting truncated response as the return limit is 140 characters
                                         exclude_replies=True, # Remove replies
                                         include_entities=True, # This is required to capture full text and all images in a tweet
                                         monitor_rate_limit=True).items(numberOfTweets)
    
    for tweet in listOfTweetsAttributes:
        try:
            #-------Processing raw date time data------------#
            tweetDate,tweetTime=getDateTimeOfTweet(tweet.created_at) # Passing Time Stamps of tweet to extract date and time
            
            #------ Sanitising tweet caption----------#
            tweetURL,tweetWithoutURL=separateUrl(tweet.full_text) # Passing the Twitter caption/ tweet description
        
            #----- Storing the meta data in a list ------------#
            for image in  tweet.extended_entities['media']: # 'extended_entities' allows to loop through all media entities
                dictOfMediaURL[uniqueIdentifierTweet].append(image['media_url']) # Dictionary allows to store tweets assiated with multiple images
                downloadTwitterImage(image['media_url'],uniqueIdentifierTweet,uniqueIdenifierImage,".jpg") # Downloads the images in local folder
                tweetImageNames.append(str(uniqueIdentifierTweet)+uniqueIdenifierImage) # Creates twitter image names such as '1' + 'a' = '1a'
                uniqueIdenifierImage = chr(ord(uniqueIdenifierImage) + 1) # Increments when multiple images associated with a tweet
            
            #----- Storing Twitter Data into a CSV file using 'writeToTwitterCSV'
            writeToTwitterCSV(csvWriter,uniqueIdentifierTweet,tweet.user.screen_name,tweetDate,tweetTime,tweetWithoutURL,tweetImageNames,dictOfMediaURL[uniqueIdentifierTweet],tweetURL)
            
            #-------Counter Reset/Inrementation--------#
            uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames=counterResetter(uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames)
            
            #---- Update User with the API status-----#
            if(uniqueIdentifierTweet%10==0): # Display a message to user every 10 tweets
                print("Ten tweets added to CSV file")
                
        except tweepy.TweepError as twitterError: # Raises an error when Twitter API fails
            logTwitterError(uniqueIdentifierTweet,twitterError.reason) # Logs the error
            uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames=counterResetter(uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames)
        
        except: # Raises an error when the programme fails due to any other reason except from twitter API
            logTwitterError(uniqueIdentifierTweet,"Unknown error found") # Logs the error
            uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames=counterResetter(uniqueIdentifierTweet,uniqueIdenifierImage,tweetImageNames)
    
    csvFileObject.close()