import ast

import os
import random
import traceback

import pyrebase
import sys

master = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.append(master)


from sandbox import take_photo


# firebase.conf file must be like this
# _____________________________________________________________
#
# {
#   "apiKey": "apiKey",
#   "authDomain": "projectId.firebaseapp.com",
#   "databaseURL": "https://databaseName.firebaseio.com",
#   "storageBucket": "projectId.appspot.com",
#   "serviceAccount": "path/to/serviceAccountCredentials.json"
# }
# ______________________________________________________________

def get_firebase():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file = dir_path + '/firebase.conf'
    with open(config_file, 'r') as f:
        config = ast.literal_eval(f.read())
        # for service account //future maybe :)
        # config["serviceAccount"]=os.path.dirname(os.path.realpath(__file__))+"/google-services.json"
        # print(config)
        try:
            firebase = pyrebase.initialize_app(config)
            return firebase
        except:
            traceback.print_exc()
            print("Couldnt initialize firebase")


def upload_file(cloud_location, file, filename):
    storage = get_firebase().storage()
    user = get_firebase_user()
    storage.child(cloud_location + filename).put(file, user['idToken'])
    return storage.child(cloud_location + filename).get_url(user['idToken'])


def capture_upload_photo():
    file_path, file_name_l = take_photo.get_photo()
    child = "drobox/"
    return upload_file(child, file_path, file_name_l)


def get_user_login_details():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    user_key = dir_path + '/user.key'
    if os.path.isfile(user_key):
        return tuple(open(user_key, 'r').read().split())
    else:
        get_firebase_user()
    return tuple(open(user_key, 'r').read().split())


def get_firebase_user():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    user_key = dir_path + '/user.key'
    if os.path.isfile(user_key):
        cred = tuple(open(user_key, 'r').read().split())
        # print("User Exists : "+str(cred))
        firebase = get_firebase()
        auth = firebase.auth()
        email_id, password = cred
        user = auth.sign_in_with_email_and_password(email_id, password)
        return user
    else:
        random_words = ['amazing', 'exclusive', 'absolutely', 'lowest', 'expert', 'accordingly', 'exploit', 'advice',
                        'extra', 'alert', 'famous', 'extraordinary', 'amazing', 'fascinating', 'anniversary', 'first',
                        'announcing', 'focus', 'anonymous', 'fortune', 'adorable', 'free', 'approved', 'full', 'as',
                        'a', 'result', 'fundamentals', 'astonishing', 'genuine', 'attractive', 'gigantic', 'authentic',
                        'greatest', 'backed', 'growth', 'bargain', 'guarantee', 'basic', 'guaranteed', 'beautiful',
                        'help', 'because', 'helpful', 'best', 'hightech', 'best-selling', 'highest', 'better', 'hot',
                        'big', 'hot', 'special', 'bonanza', 'how', 'to', 'bonus', 'huge', 'gift', 'bottom', 'line',
                        'hurry', 'breakthrough', 'imagination', 'bargain', 'immediately', 'cancel', 'anytime',
                        'important', 'caused', 'by', 'improve', 'certified', 'improved', 'challenge', 'improvement',
                        'colorful', 'increase', 'colossal', "it's", 'here', 'come', 'along', 'informative', 'compare',
                        'innovative', 'competitive', 'insider', 'complete', 'inspires', 'compromise', 'instructive',
                        'confidential', 'interesting', 'consequently', 'introducing', 'crammed', 'ironclad', 'daring',
                        'join', 'delighted', 'just', 'arrived', 'delivered', 'largest', 'destiny', 'last', 'chance',
                        'direct', 'last', 'minute', 'discount', 'latest', 'discover', 'launching', 'download',
                        'lavishly', 'due', 'to', 'learn', 'easily', 'liberal', 'easy', 'lifetime', 'edge', 'limited',
                        'emerging', 'love', 'endorsed', 'luxury', 'energy', 'mainstream', 'enormous', 'miracle',
                        'excellent', 'money', 'exciting', 'money', 'back']

        cred = str(random.choice(random_words) + random.choice(random_words) + "@missm.com"), str(
            random.choice(random_words) + random.choice(random_words))
        try:
            firebase = get_firebase()
            auth = firebase.auth()
            email_id, password = cred
            auth.create_user_with_email_and_password(email_id, password)
            print("User created : " + str(cred))
            filek = open(user_key, 'w')
            filek.write(str(cred[0] + "\n" + cred[1]))
            filek.flush()
            return auth.sign_in_with_email_and_password(email_id, password)
        except:
            traceback.print_exc()
            print("couldnt create user ")


if __name__ == '__main__':
    # print(get_user_login_details())
    # print(capture_upload_photo())
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # file_name = 'emma.jpg'
    # emma = dir_path + "/" + file_name
    # print(emma)
    # upload_file(emma, file_name)
    user=get_user_login_details()
    print(user)
