def validateSignup(dbCursor, conn, name, email, password):
    name = name.strip()
    email = email.strip()
    password = password.strip()
    query = "SELECT * FROM Client WHERE Email = %s"
    try: 
        dbCursor.execute(query, (email,))
        row = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return False

    if row is not None:
        return False
    
    query2 = "INSERT INTO Client (Email, Name, Password) VALUES (%s, %s, %s)"
    try: 
        dbCursor.execute(query2, (email, name, password))
        conn.commit()
        return True
    except Exception as e:
        print("error in query execution" + e)
        conn.rollback()
        return False




def getName(dbCursor, email):
    query = "SELECT Name FROM Client WHERE Email = %s"
    dbCursor.execute(query,(email,))
    result = dbCursor.fetchone()
    if result is not None:
        return result[0]
    else:
        return None


def validateLogin(dbCursor, email, password):
    email = email.strip()
    password = password.strip()
    query = "SELECT * FROM Client WHERE Email = %s AND Password = %s"
    try: 
        dbCursor.execute(query, (email, password))
        row = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return False

    if row is None:
        return False
    
    return True


def searchFragranceByName(dbCursor, query):
    query = query.strip()
    input = '%' + query + '%'
    query = "SELECT * FROM Fragrance WHERE REPLACE(LOWER(Name), ' ', '') LIKE REPLACE(LOWER(%s), ' ', '')"
    try: 
        dbCursor.execute(query, (input,))
        rows = dbCursor.fetchall()
    except Exception as e:
        print("error in query execution" + e)
        return None
    if rows is not None:
        fragrances = [{'name': row[1], 'house': row[2]} for row in rows]
        return fragrances
    else:
        return None
    

def searchFragranceByHouse(dbCursor, query):
    query = query.strip()
    input = '%' + query + '%'
    query = "SELECT * FROM Fragrance WHERE REPLACE(LOWER(House), ' ', '') LIKE REPLACE(LOWER(%s), ' ', '')"
    try: 
        dbCursor.execute(query, (input,))
        rows = dbCursor.fetchall()
    except Exception as e:
        print("error in query execution" + e)
        return None
    if rows is not None:
        fragrances = [{'name': row[1], 'house': row[2]} for row in rows]
        return fragrances
    else:
        return None
    


def searchFragranceByNameAndHouse(dbCursor, name, house):
    name = name.strip()
    house = house.strip()
    input = '%' + name + '%'
    input2 = '%' + house + '%'
    query = "SELECT * FROM Fragrance WHERE REPLACE(LOWER(name), ' ', '') LIKE REPLACE(LOWER(%s), ' ', '') \
             AND REPLACE(LOWER(house), ' ', '') LIKE REPLACE(LOWER(%s), ' ', '')"
    try: 
        dbCursor.execute(query, (input, input2))
        rows = dbCursor.fetchall()
    except Exception as e:
        print("error in query execution" + e)
        return None
    if rows is not None:
        fragrances = [{'name': row[1], 'house': row[2]} for row in rows]
        return fragrances
    else:
        return None
        

def addToCollection(dbCursor, conn, email, fragrance):
    actual = fragrance.strip().split(" by ")
    if len(actual) == 1:
        return False
    name = actual[0]
    house = actual[1]
    # print(name)
    # print(house)
    query = "SELECT FragranceID FROM Fragrance WHERE Name = %s AND House = %s"
    try:
        dbCursor.execute(query, (name, house))
        result = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return False
    if result is None:
        print("this fragrance doesnt exist somehow...")
        return False
    else:
        fragID = result[0]
        check = "SELECT FragranceID FROM Collection WHERE FragranceID = %s AND ClientEmail = %s"
        query2 = "INSERT INTO Collection (ClientEmail, FragranceID) VALUES (%s, %s)"
        try:
            dbCursor.execute(check, (fragID, email))
            result2 = dbCursor.fetchone()
            if result2 is None:
                dbCursor.execute(query2, (email, fragID))
                conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print("error in query execution" + e)
            return False


def addToWishlist(dbCursor, conn, email, fragrance):
    actual = fragrance.strip().split(" by ")
    if len(actual) == 1:
        return False
    name = actual[0]
    house = actual[1]
    # print(name)
    # print(house)
    query = "SELECT FragranceID FROM Fragrance WHERE Name = %s AND House = %s"
    try:
        dbCursor.execute(query, (name, house))
        result = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return False
    if result is None:
        print("this fragrance doesnt exist somehow...")
        return False
    else:
        fragID = result[0]
        check = "SELECT FragranceID FROM Wishlist WHERE FragranceID = %s AND ClientEmail = %s"
        query2 = "INSERT INTO Wishlist (ClientEmail, FragranceID) VALUES (%s, %s)"
        try:
            dbCursor.execute(check, (fragID, email))
            result2 = dbCursor.fetchone()
            if result2 is None:
                dbCursor.execute(query2, (email, fragID))
                conn.commit()
                return True
            else:
                return False
        except Exception as e:
            print("error in query execution" + e)
            return False




def getFragranceCollection(dbCursor, email, sorting):
    if sorting == "NONE":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Collection.CollectionID DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    elif sorting == "AZbyName":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Fragrance.Name ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    elif sorting == "ZAbyName":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Fragrance.Name DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    elif sorting == "AZbyHouse":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Fragrance.House ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    elif sorting == "ZAbyHouse":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Fragrance.House DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    elif sorting == "oldest":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Collection \
            JOIN Fragrance ON Collection.FragranceID = Fragrance.FragranceID \
            WHERE Collection.ClientEmail = %s \
            ORDER BY Collection.CollectionID ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_collection = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_collection
    








def getFragranceWishlist(dbCursor, email, sorting):
    if sorting == "NONE":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Wishlist.WishlistID DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    elif sorting == "AZbyName":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Fragrance.Name ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    elif sorting == "ZAbyName":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Fragrance.Name DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    elif sorting == "AZbyHouse":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Fragrance.House ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    elif sorting == "ZAbyHouse":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Fragrance.House DESC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    elif sorting == "oldest":
        query = "SELECT Fragrance.Name, Fragrance.House \
            FROM Wishlist \
            JOIN Fragrance ON Wishlist.FragranceID = Fragrance.FragranceID \
            WHERE Wishlist.ClientEmail = %s \
            ORDER BY Wishlist.WishlistID ASC"
        dbCursor.execute(query, (email,))
        rows = dbCursor.fetchall()
        fragrance_wishlist = [{'name': row[0], 'house': row[1]} for row in rows]
        return fragrance_wishlist
    


def removeFragrance(dbCursor, conn, name, house, email):
    query = "SELECT FragranceID FROM Fragrance WHERE Name = %s AND House = %s"
    dbCursor.execute(query, (name, house))
    result = dbCursor.fetchone()
    if result is None:
        print("how...")
        return False
    else:
        try:
            query2 = "DELETE FROM Collection WHERE ClientEmail = %s AND FragranceID = %s"
            dbCursor.execute(query2, (email, result[0]))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution" + e)
            return False
        
def removeFragranceWishlist(dbCursor, conn, name, house, email):
    query = "SELECT FragranceID FROM Fragrance WHERE Name = %s AND House = %s"
    dbCursor.execute(query, (name, house))
    result = dbCursor.fetchone()
    if result is None:
        print("how...")
        return False
    else:
        try:
            query2 = "DELETE FROM Wishlist WHERE ClientEmail = %s AND FragranceID = %s"
            dbCursor.execute(query2, (email, result[0]))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution" + e)
            return False
        




def sendRequest(dbCursor, conn, name, house, email):
    query = "INSERT INTO Requests (Name, House, ClientEmail) VALUES (%s, %s, %s)"
    try: 
        dbCursor.execute(query, (name, house, email))
        conn.commit()
        return True
    except Exception as e:
        print("error in query execution" + e)
        conn.rollback()
        return False
    




def getFragranceReviews(dbCursor, name, house):
    query = "SELECT ClientName, Review FROM Reviews WHERE Name = %s AND House = %s ORDER BY ReviewID Desc"
    try:
        dbCursor.execute(query, (name, house))
        rows = dbCursor.fetchall()
        if rows is None:
            return ''
        else:
            reviews = [{'name': row[0], 'review': row[1]} for row in rows]
            return reviews
    except Exception as e:
        print("error in query execution" + e)
        return False
    


def saveFragranceReview(dbCursor, conn, name, house, reviewText, email, rating):
    # IF A RATING ALREADY EXISTS, UPDATE IT WHEN REVIEW IS WRITTEN 
    email = email.strip()
    name = name.strip()
    house = house.strip()
    getName = "SELECT Name FROM Client WHERE Email = %s"
    dbCursor.execute(getName, (email,))
    clientName = dbCursor.fetchone()
    if rating != '':
        query = "INSERT INTO Reviews (Name, House, Review, ClientEmail, ClientName, Rating) VALUES (%s, %s, %s, %s, %s, %s)"
        try: 
            dbCursor.execute(query, (name, house, reviewText, email, clientName, rating))
            conn.commit()
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
            return False
    else:
        query = "INSERT INTO Reviews (Name, House, Review, ClientEmail, ClientName) VALUES (%s, %s, %s, %s, %s)"
        try: 
            dbCursor.execute(query, (name, house, reviewText, email, clientName))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
            return False

    
    check = "SELECT Client_Email, FragName, FragHouse FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s" 
    dbCursor.execute(check, (email, name, house))
    result = dbCursor.fetchone()
    if result is not None and rating != '':
        #print(result)
            try:
                query2 = "UPDATE ReviewRatings SET Rating = %s WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
                dbCursor.execute(query2, (rating, email, name, house))
                conn.commit()
                return True
            except Exception as e:
                print("error in query execution" + e)
                conn.rollback()
                return False
    else:
        if rating != '':
            query = "INSERT INTO ReviewRatings (Client_Email, Rating, FragName, FragHouse) VALUES (%s, %s, %s, %s)"
            try: 
                dbCursor.execute(query, (email, rating, name, house))
                conn.commit()
                return True
            except Exception as e:
                print("error in query execution" + e)
                conn.rollback()
                return False




def getAllReviews(dbCursor, sorting):
    if sorting == "NONE":
        query = "SELECT ReviewID, ClientName, Review, Name, House, Likes, Rating \
                 FROM Reviews \
                 ORDER BY ReviewID DESC"
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6]} for row in rows]
        return reviews
    elif sorting == "oldest":
        query = "SELECT ReviewID, ClientName, Review, Name, House, Likes, Rating \
                 FROM Reviews \
                 ORDER BY ReviewID ASC"
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6]} for row in rows]
        return reviews
    elif sorting == "popularity":
        query = "SELECT ReviewID, ClientName, Review, Name, House, Likes, Rating \
                 FROM Reviews \
                 ORDER BY Likes DESC, ReviewID DESC"
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6]} for row in rows]
        return reviews
    elif sorting == "highRated":
        query = "SELECT ReviewID, ClientName, Review, Name, House, Likes, Rating \
                 FROM Reviews \
                 ORDER BY CASE WHEN Rating IS NULL THEN 1 ELSE 0 END, Rating DESC, ReviewID DESC"
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6]} for row in rows]
        return reviews
    elif sorting == "lowRated":
        query = "SELECT ReviewID, ClientName, Review, Name, House, Likes, Rating \
                 FROM Reviews \
                 ORDER BY CASE WHEN Rating IS NULL THEN 1 ELSE 0 END, Rating ASC, ReviewID DESC"
        dbCursor.execute(query)
        rows = dbCursor.fetchall()
        reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6]} for row in rows]
        return reviews




    
def add_like_review(dbCursor, conn, email, reviewID):
    checkBefore = "SELECT * FROM ReviewLikes WHERE ClientEmail = %s AND Review_ID = %s"
    dbCursor.execute(checkBefore, (email, reviewID))
    result = dbCursor.fetchone()
    if result is None:
        query = "UPDATE Reviews SET Likes = Likes + 1 WHERE ReviewID = %s"
        try:
            dbCursor.execute(query, (reviewID,))
            conn.commit()
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
        insertion = "INSERT INTO ReviewLikes (ClientEmail, Review_ID) VALUES (%s, %s)"
        try:
            dbCursor.execute(insertion, (email, reviewID))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
    else:
        return False


def addRating(dbCursor, conn, email, rating, name, house):
    email = email.strip()
    name = name.strip()
    house = house.strip()
    check = "SELECT * FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s" 
    dbCursor.execute(check, (email, name, house))
    result = dbCursor.fetchone()
    if result is None:
        query = "INSERT INTO ReviewRatings (Client_Email, Rating, FragName, FragHouse) VALUES (%s, %s, %s, %s)"
        try: 
            dbCursor.execute(query, (email, rating, name, house))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
            return False
    else:
        try:
            query2 = "UPDATE ReviewRatings SET Rating = %s WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
            dbCursor.execute(query2, (rating, email, name, house))
            conn.commit()
        except Exception as e:
            print("error in query execution" + e)
            conn.rollback()
            return False
        




def getAverageRating(dbCursor, name, house):
    try: 
        query = "SELECT AVG(Rating) as average FROM ReviewRatings WHERE FragName = %s AND FragHouse = %s"
        dbCursor.execute(query, (name, house))
        result = dbCursor.fetchone()
        if result and result[0] is not None:
            return round(result[0], 2)  # Return the average rating rounded to 2 decimal places
        else:
            return None  # No ratings found
    except Exception as e:
        print("error in query execution" + e)
        return False

    
    