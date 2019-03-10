import pandas as pd
import uuid
from pymongo import MongoClient
from model.post import Post


print("\n\n###############################################")
print("# STEP 1 - PARSE SPREADSHEET INTO OBJECTS")
print("###############################################\n")

# Assign spreadsheet filename to `file`
file = '../resources/BACC_Posts.xlsx'

# Load spreadsheet
xl = pd.ExcelFile(file)

# Load a sheet into a DataFrame by name: df
df = xl.parse('Sheet1')

loaded_posts = []

for index, row in df.iterrows():
    post = Post(uuid.uuid1(),
                row['user_id'],
                row['creation time'],
                row['text'],
                row['image_url'],
                row['expiration in hour'])
    loaded_posts.append(post)

print("Total loaded posts in memory: {}".format(len(loaded_posts)))

print("\n\n###############################################")
print("# STEP 2 - SAVE OBJECTS INTO MONGODB")
print("###############################################\n")

#TODO: In a "real world app" I would externalize
#      the connection string to some properties file
client = MongoClient('mongodb://localhost:27017/')
instSnap = client.instSnap
posts_collection = instSnap.posts

print("Cleaning out the collection in order to start clean")
posts_collection.drop()

for post in loaded_posts:
    posts_collection.insert_one(post.to_dictionary())


print("\n\n###############################################")
print("# STEP 3 - SANITY CHECKS")
print("###############################################\n")

total_posts_inserted = instSnap.command("collstats", "posts")['count']
expected_posts_inserted = len(loaded_posts)

if total_posts_inserted != expected_posts_inserted:
    print("Only {} out of {} expected posts were inserted !!".format(total_posts_inserted, expected_posts_inserted))
else:
    print("All {} posts were inserted".format(total_posts_inserted))

client.close()
