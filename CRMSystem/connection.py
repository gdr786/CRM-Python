import pymongo

# cluster connection
client = pymongo.MongoClient(
    'mongodb+srv://gdr:1231@testcluster.4fvy9vq.mongodb.net/?retryWrites=true&w=majority')
# database and collection connection
db = client['CRM_Python']