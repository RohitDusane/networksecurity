from pymongo import MongoClient
import os

uri = "mongodb+srv://statdata247:Admin123@cluster0.eldxjk4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Ping your deployment. You are successfully connected to MongoDB.")
except Exception as e:
    print(e)
