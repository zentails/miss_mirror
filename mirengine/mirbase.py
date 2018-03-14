import ast
import os
import random
import traceback

import pyrebase

import mirtools


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

class Mirbase(metaclass=mirtools.Singleton):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_file = dir_path + '/firebase.conf'
        with open(config_file, 'r') as f:
            config = ast.literal_eval(f.read())
            # for service/admin account //future maybe :)
            # config["serviceAccount"]=os.path.dirname(os.path.realpath(__file__))+"/google-services.json"
            # print(config)
            try:
                self.firebase = pyrebase.initialize_app(config)
                self.auth = self.firebase.auth()
                self.database = self.firebase.database()
                self.storage = self.firebase.storage()
                self.user = self.generate_firebase_user()
                self.token = self.user['idToken']
                self.uid = self.user['localId']
            except:
                traceback.print_exc()
                print("Couldn't initialize firebase")

    # Essential for setup

    def generate_firebase_user(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        user_key = dir_path + '/user.key'
        if os.path.isfile(user_key):
            cred = tuple(open(user_key, 'r').read().split())
            # print("User Exists : "+str(cred))
            email_id, password = cred
            return self.auth.sign_in_with_email_and_password(email_id, password)
        else:
            random_words = ['amazing', 'exclusive', 'absolutely', 'lowest', 'expert', 'accordingly', 'exploit',
                            'advice',
                            'extra', 'alert', 'famous', 'extraordinary', 'amazing', 'fascinating', 'anniversary',
                            'first',
                            'announcing', 'focus', 'anonymous', 'fortune', 'adorable', 'free', 'approved', 'full', 'as',
                            'a', 'result', 'fundamentals', 'astonishing', 'genuine', 'attractive', 'gigantic',
                            'authentic',
                            'greatest', 'backed', 'growth', 'bargain', 'guarantee', 'basic', 'guaranteed', 'beautiful',
                            'help', 'because', 'helpful', 'best', 'hightech', 'best-selling', 'highest', 'better',
                            'hot',
                            'big', 'hot', 'special', 'bonanza', 'how', 'to', 'bonus', 'huge', 'gift', 'bottom', 'line',
                            'hurry', 'breakthrough', 'imagination', 'bargain', 'immediately', 'cancel', 'anytime',
                            'important', 'caused', 'by', 'improve', 'certified', 'improved', 'challenge', 'improvement',
                            'colorful', 'increase', 'colossal', "it's", 'here', 'come', 'along', 'informative',
                            'compare',
                            'innovative', 'competitive', 'insider', 'complete', 'inspires', 'compromise', 'instructive',
                            'confidential', 'interesting', 'consequently', 'introducing', 'crammed', 'ironclad',
                            'daring',
                            'join', 'delighted', 'just', 'arrived', 'delivered', 'largest', 'destiny', 'last', 'chance',
                            'direct', 'last', 'minute', 'discount', 'latest', 'discover', 'launching', 'download',
                            'lavishly', 'due', 'to', 'learn', 'easily', 'liberal', 'easy', 'lifetime', 'edge',
                            'limited',
                            'emerging', 'love', 'endorsed', 'luxury', 'energy', 'mainstream', 'enormous', 'miracle',
                            'excellent', 'money', 'exciting', 'money', 'back']

            cred = str(random.choice(random_words) + random.choice(random_words) + "@missm.com"), str(
                random.choice(random_words) + random.choice(random_words))
            try:
                email_id, password = cred
                self.auth.create_user_with_email_and_password(email_id, password)
                print("User created : " + str(cred))
                filek = open(user_key, 'w')
                filek.write(str(cred[0] + "\n" + cred[1]))
                filek.flush()
                filek.close()
                return self.auth.sign_in_with_email_and_password(email_id, password)
            except:
                traceback.print_exc()
                print("couldn't create user ")

    # Mirbase Tools
    def get_token(self):
        if int(self.user['expiresIn']) < 60:
            self.token = self.auth.refresh(refresh_token=self.user['refreshToken'])['idToken']
        return self.token

    def get_compartment(self):
        return self.database.child("users").child(self.uid)

    def get_users(self):
        self.get_compartment().child("jola").push({"hola": "chhola"}, self.get_token())

    def upload_file(self, cloud_location, file, filename):
        storage = self.firebase.storage()
        user = self.get_firebase_user()
        storage.child(cloud_location + filename).put(file, user['idToken'])
        return storage.child(cloud_location + filename).get_url(user['idToken'])

    def capture_upload_photo(self):
        file_path, file_name_l = mirtools.get_photo()
        child = "drobox/"
        return self.upload_file(child, file_path, file_name_l)

    @staticmethod
    def get_user_login_details():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        user_key = dir_path + '/user.key'
        return tuple(open(user_key, 'r').read().split())

    def get_firebase_user(self):
        return self.user


if __name__ == '__main__':
    Mirbase().get_users()
