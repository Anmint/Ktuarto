import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import uuid

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

    def upload_game_record(self, game_records, firstAI, secondAI, _winner):
        print('-' * 10)
        winner = None
        if _winner == 0:
            winner = 'firstAI'
        elif _winner == 1:
            winner = 'secondAI'

        record_id = str(uuid.uuid1())
        record_summary = {
                'createdAt': datetime.now(),
                'firstAI': firstAI,
                'secondAI': secondAI,
                'winner': winner
                }

        self.firestore_client.collection(u'GameRecords').document(record_id).set(record_summary)

        for index, _record in enumerate(game_records):
            record = _record[0].toDict()
            record['coordinate_left'] = int(_record[1][0])
            record['coordinate_top'] = int(_record[1][1])
            record['callingQuarto'] = _record[2] == 'Quarto'
            self.firestore_client.collection(u'GameRecords').document(record_id).collection('records').document(str(index)).set(record)
