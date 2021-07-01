from datetime import datetime
import traceback
import json
from strsimpy.levenshtein import Levenshtein
#parsing json
#take in json file and return a json object

def fileToJson(name_of_file, print = False):
    try:
        with open(f"{name_of_file}") as json_file:
            data = json.load(json_file)
    except Exception as e:
        if print:
            print(f"\n\nUnable to retrieve json ({name_of_file})")
            print(e)
            print("\n\n")
            traceback.print_exc()
        raise


    return data

#all helper functions that parse json and return int

# all fuctions take in dictionary

#helpers

def ratio_created_tweets(account_dict): #tylers func
    """
    Takes account dict and returns a dict of format and returns score in format:

    {"Ratio_Tweet":<int>}
    """

    score = {"Ratio_Tweet":0}
    today = datetime.now()
    parsed = account_dict["created_at"].split(" ")
    Months_D = {"January":31,"February":59,"March":90,"April":120,"May":151,"June":181,"July":212,"August":243,"September":273,"October":304,"November":334,"December":365}
    Days_of_Months = [31,28,31,30,31,30,31,31,30,31,30,31]
    Months_of_Year = ["January","February","March","April","May","June","July","August","September","October","November","December"]
    if Months_of_Year.index(parsed[1])>=1:
        x = 0
    else:
        x = 1
    Creation_Days = Months_D[parsed[1]]+int(parsed[2])-Days_of_Months[Months_of_Year.index(parsed[1])]+(365*int(parsed[5])+int(parsed[5])/4-x)
    if today.month >= 2:
        x = 0
    else:
        x = 1
    Current_Day = Months_D[Months_of_Year[today.month-1]]+today.day-Days_of_Months[today.month-1]+(365*today.year+today.year/4-x)
    time = parsed[3].split(":")
    UTC = parsed[4]
    if UTC[0] == "+":
        y = 1
    else:
        y = -1
    created_seconds = 60*(int(time[0])+y*(int(UTC[1])*10+int(UTC[2])))*60*int(time[1])+int(time[2])
    current_seconds = 60*(today.hour-8)*60*today.minute+today.second
    if created_seconds-current_seconds<=0:
        z = 1
    else:
        z = 0
    Total_Days = Current_Day - Creation_Days - z
    #All of this was for the total days a twitter account is active
    if int(account_dict["total_tweets"])/Total_Days>9:
        score["Ratio_Tweet"]=1
        return score
    else:
        return score



def location_created(account_dict, hotspot_list): # JOSEPH func
    """
    Takes account dict
    return dict
    format: {"location_created":score}

    """
    account_addr = account_dict.get("location")
    score = 0
    for location in hotspot_list:
        if location == account_addr:
            score = 1
    result = {"location_created":score}
    return result



def d_profile_image(account_dict):
    """
    Takes account dict

    return: {"d_profile_image":score}

    """
    if account_dict["default_profile"]==True and account_dict["default_profile_image"]==True :
        score = 1
    else:
        score = 0
    result = {"d_profile_image":score}
    return result


def ratio_following_followers(account_dict): #tyler's
    """
    takes account dict and returns ratio of following/followers

    format: score = {"Ratio_Follower":<int>}

    """

    #removed first part
    score = {"Ratio_Follower":0}

    following_count = int (account_dict["following_count"])
    follower_count = int(account_dict["followers_count"])

    ratio = (following_count / follower_count)

    if ((following_count > 1000) and ratio >= 2):
        score["Ratio_Follower"]=min(ratio, 5)
        return score
    else:
        return score

def small_following_followers(account_dict): #split ratio ratio_following_followers from tyler
    score = {"small_following_base":0}
    if int(account_dict["followers_count"])+int(account_dict["following_count"])<=10:
        score["Ratio_Follower"]=1
        return score

    return score



def quick_tweeting_score(tw_1, tw_2, tw_3):

    # Create list of tweet dicts for easier processing
    tweet_list = [tw_1, tw_2, tw_3]

    time_list = []

    # Creating a list of datetime objects based on "created_at" key
    for tweet in tweet_list:
        time_str = tweet["created_at"]
        tweet_datetime = datetime.strptime(time_str, '%c')
        time_list.append(tweet_datetime)

    # Sorts the list for us so we can check diff between most and least recent tweet
    time_list.sort()
    time_diff = (time_list[2] - time_list[0]).total_seconds()

    # If time_diff is NOT less than 10, passed = True
    passed = bool(time_diff >= 10)
    score = 0 if (passed == True) else 1
    qts_result_dict = dict([("quick_tweet", score)])


    return qts_result_dict


def similar_tweet_content(tweet1,tweet2,tweet3):
    tweet1text = tweet1.get('text')
    tweet2text = tweet2.get('text')
    tweet3text = tweet3.get('text')
    tweet1len=len(tweet1text)
    tweet2len=len(tweet2text)
    tweet3len=len(tweet3text)
    levenshtein = Levenshtein()
    check12 = levenshtein.distance(tweet1text,tweet2text)
    check23 = levenshtein.distance(tweet2text,tweet3text)
    check13 = levenshtein.distance(tweet1text,tweet3text)
    if check12 > 0.25*maximum(tweet1len,tweet2len) or check23 > 0.25*maximum(tweet3len,tweet2len) or check13 > 0.25*maximum(tweet1len,tweet3len):
        score = 0
    else:
        score = 3
    result = {"similar_tweet_content":score}
    return result


def location_spoofer(tw_1, tw_2, tw_3):

    # Create list of tweet dicts for easier processing
    tweet_list = [tw_1, tw_2, tw_3]

    loc_list, time_list = [], []

    # Creating a list of datetime objects based on "created_at" key
    for tweet in tweet_list:
        time_str = tweet["created_at"]
        tweet_datetime = datetime.strptime(time_str, '%c')
        time_list.append(tweet_datetime)

    # Sorts the list for us so we can check diff between most and least recent tweet
    # Creates a time boolean for future use
    time_list.sort()
    time_diff = (time_list[2] - time_list[0]).total_seconds()
    passed_time = bool(time_diff >= 7200)

    # Create list of location country codes (USA/RUS etc...)
    for tweet in tweet_list:
        temp_str = tweet["location"][-3:]
        loc_list.append(temp_str)

    # Check if all 3 locations are unique.
    # If all 3 ARE unique, passed_loc = False
    passed_loc = not bool(len(set(loc_list)) == len(loc_list))

    # If tweets fail both location AND time checks, then account is flagged
    score = 0 if ((passed_loc == True) or (passed_time == True)) else 1
    ls_result_dict = dict([("location_spoofer", score)])


    return ls_result_dict


def maximum(a, b):
    if a >= b:
        return a
    else:
        return b
