import psycopg2
import urllib.parse as urlparse

# Get the DATABASE_URL from Heroku
DATABASE_URL = "postgres://uf193nqndlreo:p43fef620c8179d83333a371b3b2685d588170391b56c6e9e02d78c672251f415@c2v3jin4rntblb.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d6oh1ls4v8smd1" 

# Parse the database URL
url = urlparse.urlparse(DATABASE_URL)

# Connect to the Heroku PostgreSQL database
conn = psycopg2.connect(
    database=url.path[1:],  # The database name
    user=url.username,       # The username
    password=url.password,   # The password
    host=url.hostname,       # The host
    port=url.port            # The port
)

dbCursor = conn.cursor()

# counter = 0
# Open the file and insert data into the database
with open('fragrances.txt', 'r') as file:
    for i, line in enumerate(file):
        # counter += 1
        fullLine = line.strip().split(" by ")
        name = fullLine[0].strip()
        house = fullLine[1].strip()[:-5]
        
        query = "INSERT INTO Fragrance (Name, House) VALUES (%s, %s)"
        
        try:
            dbCursor.execute(query, (name, house))
            conn.commit()
        except Exception as e:
            print("Failed to insert into query:", e)
            conn.rollback()
        # if counter == 50:
        #     break

# Close the cursor and connection
dbCursor.close()
conn.close()