# # python3 -m venv path/to/venv
# # source path/to/venv/bin/activate
# import psycopg2


# with open('fragrances.txt', 'r') as file:
#     # Read the first 10 lines of the file
#     i = 0
#     for i, line in enumerate(file):
#         fullLine = line.strip().split(" by ")
#         name = fullLine[0].strip()
#         house = fullLine[1].strip()[:-5]
#         # print(name + ": " + house)
#         query = "INSERT INTO Fragrance (Name, House) VALUES (%s, %s)"
#         try:
#             dbCursor.execute(query, (name, house))
#             conn.commit()
#         except Exception as e:
#             print("Failed to insert into query:", e)
#             conn.rollback()
    
# dbCursor.close()
# conn.close()
