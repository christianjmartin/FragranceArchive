
def passwordChecker(password):
    if len(password) < 8:
        return False

    counter_upper = False
    counter_lower = False
    counter_digit = False
    counter_symbol = False

    for i in password:
        if 'A' <= i <= 'Z':
            counter_upper = True
        elif 'a' <= i <= 'z':
            counter_lower = True
        elif '0' <= i <= '9':
            counter_digit = True
        else:
            counter_symbol = True

    if counter_upper == False or counter_lower == False or counter_digit == False or counter_symbol == False:
        return False
    else:
        return True
    

def validateSignup(dbCursor, conn, name, email, password, lastname, username):
    name = name.strip()
    email = email.strip()
    password = password.strip()

    passwordCheck = passwordChecker(password)
    if passwordCheck == False:
        return 0
    
    if len(username) > 24:
        return 4

    query = "SELECT * FROM Client WHERE Email = %s"
    try: 
        dbCursor.execute(query, (email,))
        row = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return -1

    if row is not None:
        return 1
    
    query2 = "SELECT * FROM Client WHERE Username = %s"
    try: 
        dbCursor.execute(query2, (username,))
        row2 = dbCursor.fetchone()
    except Exception as e:
        print("error in query execution" + e)
        return -1

    if row2 is not None:
        return 2
    
    query3 = "INSERT INTO Client (Email, Name, Password, LastName, Username) VALUES (%s, %s, %s, %s, %s)"
    try: 
        dbCursor.execute(query3, (email, name, password, lastname, username))
        conn.commit()
        return 3
    except Exception as e:
        print("error in query execution" + e)
        conn.rollback()
        return -1




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
    email = email.strip()
    name = name.strip()
    house = house.strip()

    # Get the client's USERNAME
    getName = "SELECT Username FROM Client WHERE Email = %s"
    dbCursor.execute(getName, (email,))
    clientName = dbCursor.fetchone() #THIS IS ACTUALLY THE USERNAME 

    try:
        # Insert the review into the Reviews table
        if rating != '':
            query = "INSERT INTO Reviews (Name, House, Review, ClientEmail, ClientName, Rating) VALUES (%s, %s, %s, %s, %s, %s) RETURNING ReviewID"
            dbCursor.execute(query, (name, house, reviewText, email, clientName[0], rating))
            conn.commit()
        else:
            query = "INSERT INTO Reviews (Name, House, Review, ClientEmail, ClientName) VALUES (%s, %s, %s, %s, %s) RETURNING ReviewID"
            dbCursor.execute(query, (name, house, reviewText, email, clientName[0]))
            conn.commit()



        # Insert or update the ReviewRatings table
        if rating != '':
            check = "SELECT * FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
            dbCursor.execute(check, (email, name, house))
            result = dbCursor.fetchone()

            if result:
                query2 = "UPDATE ReviewRatings SET Rating = %s WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
                dbCursor.execute(query2, (rating, email, name, house))
                conn.commit()
            else:
                query = "INSERT INTO ReviewRatings (Client_Email, Rating, FragName, FragHouse) VALUES (%s, %s, %s, %s)"
                dbCursor.execute(query, (email, rating, name, house))
                conn.commit()

        return True
    except Exception as e:
        print("error in query execution: " + str(e))
        conn.rollback()
        return False

    
    # check = "SELECT Client_Email, FragName, FragHouse FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s" 
    # dbCursor.execute(check, (email, name, house))
    # result = dbCursor.fetchone()
    # if result is not None and rating != '':
    #     #print(result)
    #         try:
    #             query2 = "UPDATE ReviewRatings SET Rating = %s WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
    #             dbCursor.execute(query2, (rating, email, name, house))
    #             conn.commit()
    #             return True
    #         except Exception as e:
    #             print("error in query execution" + e)
    #             conn.rollback()
    #             return False
    # else:
    #     if rating != '':
    #         query = "INSERT INTO ReviewRatings (Client_Email, Rating, FragName, FragHouse) VALUES (%s, %s, %s, %s)"
    #         try: 
    #             dbCursor.execute(query, (email, rating, name, house))
    #             conn.commit()
    #             return True
    #         except Exception as e:
    #             print("error in query execution" + e)
    #             conn.rollback()
    #             return False




def saveEditedFragranceReview(dbCursor, conn, name, house, reviewText, email, rating, review_id):
    email = email.strip()
    name = name.strip()
    house = house.strip()
    reviewText = reviewText.strip()
    
    getName = "SELECT Username FROM Client WHERE Email = %s"
    dbCursor.execute(getName, (email,))
    clientName = dbCursor.fetchone()
    
    # Check if the review exists
    checkReview = "SELECT * FROM Reviews WHERE ReviewID = %s AND ClientEmail = %s"
    dbCursor.execute(checkReview, (review_id, email))
    existingReview = dbCursor.fetchone()

    if existingReview:
        # Update the existing review
        if rating != '':
            query = "UPDATE Reviews SET Name = %s, House = %s, Review = %s, ClientName = %s, Rating = %s WHERE ReviewID = %s AND ClientEmail = %s"
            try: 
                dbCursor.execute(query, (name, house, reviewText, clientName, rating, review_id, email))
                conn.commit()
            except Exception as e:
                print("error in query execution" + str(e))
                conn.rollback()
                return False
        else:
            query = "UPDATE Reviews SET Name = %s, House = %s, Review = %s, ClientName = %s WHERE ReviewID = %s AND ClientEmail = %s"
            try: 
                dbCursor.execute(query, (name, house, reviewText, clientName, review_id, email))
                conn.commit()
                return True
            except Exception as e:
                print("error in query execution" + str(e))
                conn.rollback()
                return False

        # Update the ReviewRatings table
        check = "SELECT Client_Email, FragName, FragHouse FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s" 
        dbCursor.execute(check, (email, name, house))
        result = dbCursor.fetchone()
        if result is not None and rating != '':
            try:
                query2 = "UPDATE ReviewRatings SET Rating = %s WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
                dbCursor.execute(query2, (rating, email, name, house))
                conn.commit()
                return True
            except Exception as e:
                print("error in query execution" + str(e))
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
                    print("error in query execution" + str(e))
                    conn.rollback()
                    return False
    else:
        # Handle case where review does not exist (optional, based on your application logic)
        print("Review does not exist.")
        return False






def getAllReviews(dbCursor, email, sorting):
    if sorting == "NONE":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            ORDER BY r.ReviewID DESC
        """
        dbCursor.execute(query, (email,))
    elif sorting == "oldest":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            ORDER BY r.ReviewID ASC
        """
        dbCursor.execute(query, (email,))
    elif sorting == "popularity":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            ORDER BY r.Likes DESC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email,))
    elif sorting == "highRated":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            ORDER BY CASE WHEN r.Rating IS NULL THEN 1 ELSE 0 END, r.Rating DESC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email,))
    elif sorting == "lowRated":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            ORDER BY CASE WHEN r.Rating IS NULL THEN 1 ELSE 0 END, r.Rating ASC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email,))

    rows = dbCursor.fetchall()
    reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6], 'user_liked': row[7], 'review_email': row[8]} for row in rows]
    return reviews


    






def getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house):
    if sorting == "NONE":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            WHERE r.Name = %s AND r.House = %s
            ORDER BY r.ReviewID DESC
        """
        dbCursor.execute(query, (email, fragrance_name, fragrance_house))
    elif sorting == "oldest":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            WHERE r.Name = %s AND r.House = %s
            ORDER BY r.ReviewID ASC
        """
        dbCursor.execute(query, (email, fragrance_name, fragrance_house))
    elif sorting == "popularity":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            WHERE r.Name = %s AND r.House = %s
            ORDER BY r.Likes DESC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email, fragrance_name, fragrance_house))
    elif sorting == "highRated":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            WHERE r.Name = %s AND r.House = %s
            ORDER BY CASE WHEN r.Rating IS NULL THEN 1 ELSE 0 END, r.Rating DESC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email, fragrance_name, fragrance_house))
    elif sorting == "lowRated":
        query = """
            SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, l.ReviewLikesID IS NOT NULL AS UserLiked, r.ClientEmail
            FROM Reviews r
            LEFT JOIN ReviewLikes l ON r.ReviewID = l.Review_ID AND l.ClientEmail = %s
            WHERE r.Name = %s AND r.House = %s
            ORDER BY CASE WHEN r.Rating IS NULL THEN 1 ELSE 0 END, r.Rating ASC, r.ReviewID DESC
        """
        dbCursor.execute(query, (email, fragrance_name, fragrance_house))

    rows = dbCursor.fetchall()
    reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6], 'user_liked': row[7], 'review_email': row[8]} for row in rows]
    return reviews




def getUserReviews(dbCursor, user_email, viewer_email):
    query = """
        SELECT r.ReviewID, r.ClientName, r.Review, r.Name, r.House, r.Likes, r.Rating, 
               CASE WHEN rl.ClientEmail IS NOT NULL THEN 1 ELSE 0 END AS UserLiked
        FROM Reviews r
        LEFT JOIN ReviewLikes rl ON r.ReviewID = rl.Review_ID AND rl.ClientEmail = %s
        WHERE r.ClientEmail = %s
        ORDER BY r.ReviewID DESC
    """
    dbCursor.execute(query, (viewer_email, user_email))
    rows = dbCursor.fetchall()
    reviews = [{'review_id': row[0], 'name': row[1], 'review': row[2], 'fragrance_name': row[3], 'fragrance_house': row[4], 'likes': row[5], 'rating': row[6], 'user_liked': row[7]} for row in rows]
    return reviews















def add_like_review(dbCursor, conn, email, reviewID):
    checkBefore = "SELECT * FROM ReviewLikes WHERE ClientEmail = %s AND Review_ID = %s"
    dbCursor.execute(checkBefore, (email, reviewID))
    result = dbCursor.fetchone()
    
    if result is None:
        # Add like
        query = "UPDATE Reviews SET Likes = Likes + 1 WHERE ReviewID = %s"
        try:
            dbCursor.execute(query, (reviewID,))
            conn.commit()
        except Exception as e:
            print("error in query execution: " + str(e))
            conn.rollback()
            return False
        
        insertion = "INSERT INTO ReviewLikes (ClientEmail, Review_ID) VALUES (%s, %s)"
        try:
            dbCursor.execute(insertion, (email, reviewID))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution: " + str(e))
            conn.rollback()
            return False
    else:
        # Remove like
        query = "UPDATE Reviews SET Likes = Likes - 1 WHERE ReviewID = %s"
        try:
            dbCursor.execute(query, (reviewID,))
            conn.commit()
        except Exception as e:
            print("error in query execution: " + str(e))
            conn.rollback()
            return False
        
        deletion = "DELETE FROM ReviewLikes WHERE ClientEmail = %s AND Review_ID = %s"
        try:
            dbCursor.execute(deletion, (email, reviewID))
            conn.commit()
            return True
        except Exception as e:
            print("error in query execution: " + str(e))
            conn.rollback()
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

    
    

def getUserRating(dbCursor, email, fragrance_name, fragrance_house):
    query = "SELECT Rating FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
    dbCursor.execute(query, (email, fragrance_name, fragrance_house))
    result = dbCursor.fetchone()
    return result[0] if result else None





def searchUsers(dbCursor, query):
    search_query = f"%{query}%"
    query = """
        SELECT Username, Email 
        FROM Client 
        WHERE Username ILIKE %s
    """
    dbCursor.execute(query, (search_query,))
    users = dbCursor.fetchall()
    return [{'username': user[0], 'email': user[1]} for user in users]



def getUserEmailByUsername(dbCursor, username):
    query = "SELECT Email FROM Client WHERE Username = %s"
    dbCursor.execute(query, (username,))
    result = dbCursor.fetchone()
    return result[0] if result else None


def getUsername(dbCursor, email):
    query = "SELECT Username FROM Client WHERE Email = %s"
    dbCursor.execute(query, (email,))
    result = dbCursor.fetchone()
    return result[0] if result else None





def is_following(dbCursor, follower_email, following_email):
    query = "SELECT 1 FROM Follows WHERE FollowerEmail = %s AND FollowingEmail = %s"
    dbCursor.execute(query, (follower_email, following_email))
    return dbCursor.fetchone() is not None

def getFollowers(dbCursor, email):
    query = """
        SELECT c.Username, c.Email 
        FROM Follows f
        JOIN Client c ON f.FollowerEmail = c.Email
        WHERE f.FollowingEmail = %s
        ORDER BY DateFollowed DESC
    """
    dbCursor.execute(query, (email,))
    followers = dbCursor.fetchall()
    return [{'username': follower[0], 'email': follower[1]} for follower in followers]

def getFollowing(dbCursor, email):
    query = """
        SELECT c.Username, c.Email 
        FROM Follows f
        JOIN Client c ON f.FollowingEmail = c.Email
        WHERE f.FollowerEmail = %s
        ORDER BY DateFollowed DESC
    """
    dbCursor.execute(query, (email,))
    following = dbCursor.fetchall()
    return [{'username': follower[0], 'email': follower[1]} for follower in following]




def getFragranceOfWeek(dbCursor, week_number):
    query = "SELECT * FROM FragranceOfTheWeek WHERE week_number = %s"
    dbCursor.execute(query, (week_number,))
    fragrance = dbCursor.fetchone()
    return {'fragrance_name': fragrance[2], 'description': fragrance[3], 'image_url': fragrance[4]}
