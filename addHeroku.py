# import psycopg2
# import urllib.parse as urlparse
# import os

# # Get the DATABASE_URL from Heroku
# DATABASE_URL = os.getenv('DATABASE_URL')

# # Parse the database URL
# if DATABASE_URL:
#     url = urlparse.urlparse(DATABASE_URL)

#     # Connect to the Heroku PostgreSQL database
#     conn = psycopg2.connect(
#         database=url.path[1:],  # The database name
#         user=url.username,       # The username
#         password=url.password,   # The password
#         host=url.hostname,       # The host
#         port=url.port            # The port
#     )

#     dbCursor = conn.cursor()

#     # counter = 0
#     # Open the file and insert data into the database
#     with open('fragrances.txt', 'r') as file:
#         for i, line in enumerate(file):
#             # counter += 1
#             fullLine = line.strip().split(" by ")
#             name = fullLine[0].strip()
#             house = fullLine[1].strip()[:-5]
            
#             query = "INSERT INTO Fragrance (Name, House) VALUES (%s, %s)"
            
#             try:
#                 dbCursor.execute(query, (name, house))
#                 conn.commit()
#             except Exception as e:
#                 print("Failed to insert into query:", e)
#                 conn.rollback()
#             # if counter == 50:
#             #     break

#     # Close the cursor and connection
#     dbCursor.close()
#     conn.close()
# else:
#     print("no databse url")