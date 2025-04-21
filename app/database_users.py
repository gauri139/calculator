import pymongo
# import project_config


def get_db():
    url = f"mongodb://localhost:27017"
    mongo_client = pymongo.MongoClient(url)

    db = mongo_client['calculator_db']
    user_collection = db['users']
    history_collection=db['history']
    
    return user_collection