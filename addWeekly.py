import psycopg2
import csv
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




with open('WeeklyFragrances.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)  # Using DictReader for easier access by column name
    
    for row in reader:
        # Extracting values from the CSV
        week_number = int(row['week_number'])
        fragrance_name = row['fragrance_name'].strip()
        description = row['description'].strip()
        image_url = row['image_url'].strip()

        # Insert the data into the database
        query = """
            INSERT INTO FragranceOfTheWeek (week_number, fragrance_name, description, image_url)
            VALUES (%s, %s, %s, %s)
        """
        
        try:
            dbCursor.execute(query, (week_number, fragrance_name, description, image_url))
            conn.commit()
        except Exception as e:
            print("Failed to insert into database:", e)
            conn.rollback()

# Close the cursor and connection
dbCursor.close()
conn.close()