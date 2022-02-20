import firebase_admin
from firebase_admin import credentials, firestore

class firebaseClient():

    def __init__(self):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
          'projectId': 'quartobattlestation'
        })
        self.firestore_client = firestore.client()

    def get_elo(self, player_name):
        AI_data = self.firestore_client.collection(u'AIs').document(player_name).get()
        return AI_data.to_dict()['ELO'] if AI_data.exists else 1200

    def update_elo(self, player_name, new_elo):
        self.firestore_client.collection(u'AIs').document(player_name).set({'ELO': new_elo})
