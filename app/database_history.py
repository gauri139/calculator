import pymongo
# import project_config


def get_history():
    url = f"mongodb://localhost:27017"
    mongo_client = pymongo.MongoClient(url)

    db = mongo_client['cal_db']
    history_collection= db['history']
    
    return history_collection