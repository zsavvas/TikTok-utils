import json
from optparse import OptionParser
from distutils.util import strtobool
import sys

ADS_KEY = 'Ads and data'
ACTIVITY_KEY = 'Activity'
COMMENTS_KEY = 'Comment'



# method to anonymize the TikTok data
def anonymize_tiktok_data(json_object, 
                            donate_like_history=True,
                            donate_search_history=True,
                            donate_share_history=True,
                            donate_session_times=True,
                            donate_favorites=True,
                            donate_following=True,
                            donate_followers=True,
                            donate_comments=True,
                            donate_comments_text=True,
                            donate_ads=True,
                            donate_settings=True):

    # verify that the data has indeed the fields that we absolutely need. if something is missing
    # return False meaning we are unable to recognize the TikTok data
    if ACTIVITY_KEY in json_object:
        activity = json_object[ACTIVITY_KEY]
        if 'Video Browsing History' not in activity:
            return False
        if 'Like List' not in activity:
            return False
        if 'Search History' not in activity:
            return False
        if 'Share History' not in activity:
            return False
    else:
        return False
    
    comments = json_object[COMMENTS_KEY]
    
    # remove optional activity fields based on params

    # remove followers if they exist
    if donate_followers==False:
        if 'Follower List' in activity:
            del activity['Follower List']

    # remove following if they exist
    if donate_following==False:
        if 'Following List' in activity:
            del activity['Following List']

    # remove favorites if they exist
    if donate_followers==False:
        if 'Favorite Effects' in activity:
            del activity['Favorite Effects']

        if 'Favorite Sounds' in activity:
            del activity['Favorite Sounds']

        if 'Favorite Hashtags' in activity:
            del activity['Favorite Hashtags']

        if 'Favorite Videos' in activity:
            del activity['Favorite Videos']

    if donate_like_history==False:
        if 'Like List' in activity:
            del activity['Like List']

    if donate_search_history==False:
        if 'Search History' in activity:
            del activity['Search History']

    if donate_share_history==False:
        if 'Share History' in activity:
            del activity['Share History']

    # Iterate through sessions and delete personal data
    if donate_session_times:
        try:
            login_history_list = activity['Login History']['LoginHistoryList']
            for session in login_history_list:
                del session['IP']
                del session['DeviceModel']
                del session['DeviceSystem']
                del session['NetworkType']
                del session['Carrier']
        except KeyError:
            pass
    else:
        del activity['Login History']

    if 'Purchase History' in activity:
        del activity['Purchase History']
    if 'Status' in activity:
        del activity['Status']


    if donate_comments==False:
        anonymized_user_object = {'Activity': activity}
    else:
        try:
            if donate_comments_text==False:
                for comment in comments['Comments']['CommentsList']:
                    comment['Comment'] = "[redacted]"
            anonymized_user_object = {'Activity': activity, 'Comment':comments}
        except:
            pass


    if 'App Settings' in json_object:
        settings = json_object['App Settings']['Settings']['SettingsMap']
        if donate_settings:
            anonymized_user_object['Settings'] = settings

    if donate_ads:
        if ADS_KEY in json_object:
            ads = json_object[ADS_KEY]
            anonymized_user_object[ADS_KEY] = ads 


    
    return anonymized_user_object




if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option("-f", "--file", dest='input', default='user_data.json', help="TikTok data file")
    parser.add_option("-o", "--output", dest='output', default='user_data_anonymized.json',help="Output file")
    parser.add_option("-l", "--like-history", dest='like_history', default="True", help="Donate Like History")
    parser.add_option("-k", "--share-history", dest='share_history', default="True", help="Donate Share History")
    parser.add_option("-a", "--search-history", dest='search_history', default="True", help="Donate Search History")
    parser.add_option("-b", "--favorites", dest='favorites', default="True", help="Donate Favorites")
    parser.add_option("-c", "--followers", dest='followers', default="True", help="Donate Followers")
    parser.add_option("-d", "--following", dest='following', default="True", help="Donate Following")
    parser.add_option("-e", "--comments", dest='comments', default="True", help="Donate Comments")
    parser.add_option("-g", "--comments-text", dest='comments_text', default="True", help="Donate Comments text")
    parser.add_option("-m", "--ads", dest='ads', default="True", help="Donate ads")
    parser.add_option("-j", "--settings", dest='settings', default="True", help="Donate App Settings")
    parser.add_option("-i", "--session-times", dest='session_times', default="True", help="Donate Session Times")



    (options, args) = parser.parse_args()

    inp = options.input
    out = options.output
    session_times = bool(strtobool(options.session_times))
    like_history = bool(strtobool(options.like_history))
    share_history = bool(strtobool(options.share_history))
    search_history = bool(strtobool(options.search_history))
    favorites = bool(strtobool(options.favorites))
    followers = bool(strtobool(options.followers))
    following = bool(strtobool(options.following))
    comments = bool(strtobool(options.comments))
    comments_text = bool(strtobool(options.comments_text))
    ads = bool(strtobool(options.ads))
    settings = bool(strtobool(options.settings))

    # load input data
    try:
        with open(inp, "r") as user_file:
            user_object = json.load(user_file)
    except:
        print("It seems that you did not provide a valid json file. Make sure to provide a file downloaded from TikTok.")
        sys.exit(0)
    # write anonymized output
    anonymized_user_data = anonymize_tiktok_data(user_object, 
                                                donate_like_history=like_history,
                                                donate_search_history=search_history,
                                                donate_share_history=share_history,
                                                donate_session_times=session_times,
                                                donate_favorites=favorites,
                                                donate_following=following,
                                                donate_followers=followers,
                                                donate_comments=comments,
                                                donate_comments_text=comments_text,
                                                donate_ads=ads,
                                                donate_settings=settings)
    if anonymized_user_data:
        with open(out, 'w') as d_file:
            json.dump(anonymized_user_data, d_file, indent=4, sort_keys=True)
            print("Depersonalized file with name " + out  + ' written!')
    else:
        print("Unable to recognize TikTok data.")