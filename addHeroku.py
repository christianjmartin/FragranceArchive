import psycopg2
import urllib.parse as urlparse
import csv 
import os
import re 

# Get the DATABASE_URL from Heroku
DATABASE_URL = os.getenv('DATABASE_URL')

# Parse the database URL
if DATABASE_URL:
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

    csv_file_path = 'parfumo_datos.csv'

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)  # Assumes CSV has headers: Name, Brand, ReleaseYear

        for row in reader:

            name = row['URL'].strip()
            name = name.split("/")[-1]
            name = re.sub(r"[_\-]", " ", name)
            name = re.sub(r"\s+", " ", name)
            name = name.strip().lower().title()

            house = row['Brand'].strip()

            # Insert data into the Fragrance table
            try:
                dbCursor.execute(
                "INSERT INTO Fragrance (Name, House) VALUES (%s, %s)",
                (name, house)
                )
                conn.commit()
            except Exception as e:
                print("Failed to insert into query:", e)
                conn.rollback()
            # if counter == 50:
            #     break

    # Close the cursor and connection
    dbCursor.close()
    conn.close()
else:
    print("no databse url")