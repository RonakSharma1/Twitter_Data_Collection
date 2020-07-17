# Aim
Within a user specified timeframe, the programme extracts the Twitter data (Tweets) that matches user specified query parameters i.e. a list of hashtags and expressions

# Data Constraints
The programme filters out any retweets, replies, non-image tweets and also sanitises tweets by removing the non-ASCII characters.

# Result
1. 'Twitter_API_Result.csv': Stores the following information related to the data constrained tweets; Twitter Handle, Time Stamp, Tweet(Description), Names of Images associated to each Tweet,URL of images, URL of Tweets
2. Images are downloaded and stored locally using their URL extracted from Tweets  
3. 'Error_Log.txt': Logs any errors generated during the API call

# Structure of Folder
1. 'TwitterAPI_Socialmedia_Extract.py': Main Python file to run
2. 'credentials.txt': Contains the credentials of a Twitter Developer Account
3. 'hashtags.txt': Contains the list of hashtags (or any other query parameter) separated by ','. To understand the format of this file, check the Procedure Section


# Installation
1. Installing 'Tweepy' library in Anaconda on Mac OS
```
conda install -c conda-forge tweepy
```

# Procedure
1. Clone the 'credentials.txt' and replace the keys and tokens with the your credentials obtained via Twitter Developer Account

2. Clone the 'hashtags.txt' and enter the query parameters separated by ','.All the queries in the first row are OR'd. This expression is then AND'd with the OR'd query expression of second row. Example:
Row1: Science,Data
Row2. Research,Academic
Final Query= (Science OR Data) AND (Research OR Academic)

3. Run 'TwitterAPI_Socialmedia_Extract.py'. You will be asked to enter start and end date of the search and number of Tweets you want to store
 

# Documentation
1. [Twitter Query Python Tutorial](https://www.earthdatascience.org/courses/use-data-open-source-python/intro-to-apis/social-media-text-mining-python/)
2. [Tweepy Documentation](https://github.com/tweepy/tweepy)
3. [Tweepy GitHub Repository](https://github.com/tweepy/tweepy)
