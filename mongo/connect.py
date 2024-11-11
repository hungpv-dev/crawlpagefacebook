from pymongo.mongo_client import MongoClient

uri = 'mongodb+srv://hungpv:hungpv@crawlpagefacebook.h5qui.mongodb.net/?retryWrites=true&w=majority&appName=crawlpagefacebook'

client = MongoClient(uri)

try:
    client.admin.command('ping')
except Exception as e:
    print(e)
