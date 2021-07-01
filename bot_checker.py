import sys
from helpers import *
import traceback

#contains functions
    #main function
        #Takes an account json and tweets json and returns a resulting json
        #that contains analysis of account
    # analyze accounts
    #analyze tweets

#only functions directly related to bot checking


#analyze accounts
    #takes a dictionary
    #returns total score json related to account



#const


PATH_TO_REGULAR = "jsons/regular/"
PATH_TO_BOT = "jsons/bot/"
HOTSPOT_LIST = [""]

#returns tweet dict given tweet id
def get_tweetfile_toDict(tweet_id):
    #add postfix to string
    path = PATH_TO_REGULAR + tweet_id
    path += ".json"

    # print("Trying path to regular....")
    while True: #checks both directories for tweets 
        try:
            data = fileToJson(path)
            break
        except FileNotFoundError:
            path = PATH_TO_BOT + tweet_id + ".json"
            # print("Trying path to bot....")
            data = fileToJson(path)

    return data



def analyze_accounts(account_dict):
    """
    Calls each helper function and returns a combined json of all of them
    """
    tw_1 = get_tweetfile_toDict(account_dict["tweets"]["0"])
    tw_2 = get_tweetfile_toDict(account_dict["tweets"]["1"])
    tw_3 = get_tweetfile_toDict(account_dict["tweets"]["2"])

    # return_json = {
    #     ratio_created_tweets(account_dict),
    #     location_created(account_dict, HOTSPOT_LIST),
    #     d_profile_image(account_dict),
    #     ratio_following_followers(account_dict),
    #     small_following_followers(account_dict),
    #     quick_tweeting_score(tw_1, tw_2, tw_3),
    #     similar_tweet_content(tw_1,tw_2,tw_3)
    #     }

    # return_json = {
    #     dict(ratio_created_tweets(account_dict).items()
    #     + location_created(account_dict, HOTSPOT_LIST).items()
    #     + d_profile_image(account_dict).items()
    #     + ratio_following_followers(account_dict).items()
    #     + small_following_followers(account_dict).items()
    #     + quick_tweeting_score(tw_1, tw_2, tw_3).items()
    #     + similar_tweet_content(tw_1,tw_2,tw_3).items())
    #     }

    return_json = {}
    return_json.update(ratio_created_tweets(account_dict))
    return_json.update(location_created(account_dict, HOTSPOT_LIST))
    return_json.update(d_profile_image(account_dict))
    return_json.update(ratio_following_followers(account_dict))
    return_json.update(small_following_followers(account_dict))
    return_json.update(quick_tweeting_score(tw_1, tw_2, tw_3))
    return_json.update(similar_tweet_content(tw_1,tw_2,tw_3))
    return_json.update(location_spoofer(tw_1, tw_2, tw_3))

    return return_json

def main():
    #account json = sys.argv[1]
    #tweet json = sys.argv[2]
    if not len(sys.argv) == 2:
        print("Invalid arguments")
        print("Usage: bot_checker.py <account.json>")
        return

    path_to_account_json = sys.argv[1]

    """
    {
    "<Pass or fail>":
        {
        score: <total score>

        "scores"
            {
            "Ratio_Tweet": <int>,
            "location_created": <int>,
            "d_profile_image": <int>,
            "Ratio_Follower": <int>,
            "Ratio_Follower": <int>,
            "quick_tweet": <int>,
            "similar_tweet_content": <int>
            "Location Spoofer": <int>
            }
        }
    }
    """

    #Get account json and tweet json
    account_dict = fileToJson(path_to_account_json)

    #get all of the scores
    score_json = analyze_accounts(account_dict["user"])

    #get total score based on all jsons
    total_score = (int(score_json["Ratio_Tweet"]) + int(score_json["location_created"])
        + int(score_json["d_profile_image"]) + int(score_json["Ratio_Follower"])
        + int(score_json["small_following_base"]) + int(score_json["quick_tweet"])
        + int(score_json["similar_tweet_content"])   + int(score_json["location_spoofer"]))

    if(total_score > 14):
        pass_fail = "True"
    else:
        pass_fail = "False"
    #create return json
    return_json = {
        "is_bot": pass_fail,
        "score": total_score,
        "score_breakdown": score_json
        } #nested json

    print(return_json)

if __name__ == '__main__':
    main()
