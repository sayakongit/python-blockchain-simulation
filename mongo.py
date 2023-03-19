import pymongo

if __name__ == "__main__":

    # data = {
    #     'index': -45,
    #     'timestamp': 'test2255',
    #     'data': 'sample data',
    #     'proof': 'jhdpioahdihdajd5453dfad',
    #     'previous_hash': 'none',
    # }
    
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['college']
    collection = db['blockTest']

    def mongo_commit(data):
        collection.insert_one(data)
        print("Data inserted to DB")
    
    # mongo_commit(data)
    print("Mongo Client up and running!")