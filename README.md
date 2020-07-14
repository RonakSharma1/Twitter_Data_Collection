#Twitter_Data_Collection

#Aim


#Installation
1. Installing 'Tweepy' library on Anaconda
```
conda install -c conda-forge tweepy
```

#Procedure
1. Clone the 'credentials.txt' and replace the keys/tokens with the your credentials
2. Clone the 'hashtags.txt' and enter the query parameters separated by ','
3. Run 'TwitterAPI_Socialmedia_Extract.py'. You will be asked to enter start and end date of the search and number of Tweets you want to store
 
#Result
1. A 'Twitter_API_Result.csv' will be generated consisting of username, timestamps, twitter text, image name, and URLs of images and tweets
2. An 'Error_Log.txt' will be created consisting of any errors received during the API calls

#Structure of Folder



#Guidelines
1.[Twitter Query Python Tutorial](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/social-media-text-mining-python/)
2.[Tweepy Documentation](https://github.com/tweepy/tweepy)
3.[Tweepy GitHub Repository](https://github.com/tweepy/tweepy)