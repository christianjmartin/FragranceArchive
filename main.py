

#START HERE, COMMAND LINE ARGS ... i have a macbook. may be different for windows 

# python3 -m venv path/to/venv
# source path/to/venv/bin/activate
# python3 -m pip install psycopg2
# python3 -m pip install flask

#TO RUN

# python3 main.py


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from urllib.parse import unquote
from datetime import datetime
import psycopg2
# import junk
import logic

import urllib.parse as urlparse
import os

app = Flask(__name__)
# app.secret_key = '123456789'

# app.secret_key = 'IISAODN-2421S-QWFQ13QV-193C1aaa'
app.secret_key = os.getenv('SECRET_KEY')

# Parse the database URL provided by Heroku
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    url = urlparse.urlparse(DATABASE_URL)
    conn = psycopg2.connect(
        database=url.path[1:],  # Remove leading '/'
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
else:
    # Fallback to local settings (useful for local development)
    conn = psycopg2.connect(
        host="localhost",
        database="FragranceDatabase",
        user="postgres",
        password=os.getenv('DB_PASSWORD'),
    )

dbCursor = conn.cursor()

@app.route('/')
def home():
    session.clear()
    # Render the home page template
    return render_template('index.html')



@app.route('/back_to_index', methods=['GET', 'POST'])
def back_to_index():
    return render_template('index.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def handle_signup():
    if request.method == 'POST':
        # Handle form submission
        name = request.form.get('name')
        email = request.form.get('email')
        lastname = request.form.get('lastname')
        username = request.form.get('username')
        session['username'] = username
        session['email'] = email
        session['name'] = name
        password = request.form.get('password')

        # Process form data (validate, create user, etc.)
        if name and email and password:
            validSignup = logic.validateSignup(dbCursor, conn, name, email, password, lastname, username)
            if validSignup == 3:
                return redirect(url_for('handle_menu', userName = session['name']))  # Placeholder response
            elif validSignup == 0:
                return 'Invalid Password, Password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one digit, and one special character.'
            elif validSignup == 1:
                return 'An account with this email address already exists, please choose a different email or go back and log in'
            elif validSignup == 2:
                return 'An account with this username already exists, please choose a different username or go back and log in'
            elif validSignup == 4:
                return 'The username you have entered is too long, the maximum number of characters allowed is 21'
            else:
                return 'Internal error'
        else:
            return 'Invalid form data. Please provide email and password.'

    else:
        # Render the sign-up form template for GET requests
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def handle_login():
    if request.method == 'POST':
        # Handle form submission
        email = request.form.get('email')
        password = request.form.get('password')
        session['email'] = email
        session['name'] = logic.getName(dbCursor, email)

        # Process form data (validate, create user, etc.)
        if email and password:
            validSignup = logic.validateLogin(dbCursor, email, password)
            if validSignup:
                return redirect(url_for('handle_menu', userName = session['name']))  # Placeholder response
            else:
                return 'An account with this email & password combination \n does not exist, please choose a different email or go back and create a new account with us'
        else:
            return 'Invalid form data. Please provide email and password.'

    else:
        # Render the login form template for GET requests
        return render_template('login.html')

@app.route('/handle_menu', methods=['GET', 'POST'])
def handle_menu():
    # Handle the main menu
    week_number = datetime.now().isocalendar()[1]
    # week_number = (week_number - 1) % 52 + 1
    fragranceOfWeek = logic.getFragranceOfWeek(dbCursor, week_number)
    
    # if fragranceOfWeek:
    #     print(fragranceOfWeek['image_url'])
    return render_template('menu.html', userName = session['name'], fragranceOfWeek=fragranceOfWeek)






# SEARCHING FOR JS HERE 

@app.route('/search_fragrances_by_name', methods=['GET'])
def search_fragrances_by_name():
    query = request.args.get('query')
    query = query.lower()
    results = logic.searchFragranceByName(dbCursor, query)
    if results is not None:
        return jsonify(results)
    else:
        return jsonify([])
    

    
@app.route('/search_fragrances_by_house', methods=['GET'])
def search_fragrances_by_house():
    query = request.args.get('query')
    query = query.lower()
    results = logic.searchFragranceByHouse(dbCursor, query)
    if results is not None:
        return jsonify(results)
    else:
        return jsonify([])
    

@app.route('/search_fragrances_by_name_and_house', methods=['GET'])
def search_fragrances_by_name_and_house():
    name = request.args.get('name_query')
    house = request.args.get('house_query')
    name = name.lower()
    house = house.lower()

    results = logic.searchFragranceByNameAndHouse(dbCursor, name, house)
    if results is not None:
        #print(results)
        return jsonify(results)
    else:
        return jsonify([])
    


    



# COLLECTION HERE

@app.route('/handle_collection', methods=['GET', 'POST'])
def handle_collection():
    # Handle the colleciton
    sorting = "NONE"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)


@app.route('/add_collection', methods=['GET', 'POST'])
def add_collection():
    if request.method == "POST":
        fragrance = request.form.get('frag')
        if fragrance is not None:
            print("fragrance is " + fragrance)
        else:
            print("No fragrance name provided")
        return redirect(url_for('handle_collection'))
    else:
        return render_template('addCollection.html')



@app.route('/add_fragrance_to_collection', methods=['POST'])
def add_fragrance_to_collection():
    # Get the fragrance name from the form submission
    fragrance_name = request.form.get('fragrance_name')
    if fragrance_name is None:
        fragrance_name = request.form.get('fragrance_house')
        
    # print(fragrance_name)
    email = session.get('email')
    addedSuccessfully = logic.addToCollection(dbCursor, conn, email, fragrance_name)
   
    if addedSuccessfully:
        return redirect(url_for('handle_collection'))
    else:
        return jsonify({'message': str(fragrance_name) + ' was not not found, or it is already a part of your collection... go back and try again'})


@app.route('/remove_collection', methods=['GET', 'POST'])
def remove_collection():
    sorting = "NONE"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('removeCollection.html', fragrance_collection=fragrance_collection)


@app.route('/remove_fragrance', methods=['POST'])
def remove_fragrance():
    name = request.form.get('fragrance_name')
    house = request.form.get('fragrance_house')
    logic.removeFragrance(dbCursor, conn, name, house, session['email'])
    return redirect(url_for('handle_collection'))

@app.route('/back_to_collection', methods=['POST', 'GET'])
def back_to_collection():
    return redirect(url_for('handle_collection'))








#WISHLIST HERE 

@app.route('/handle_wishlist', methods=['POST', 'GET'])
def handle_wishlist():
    sorting = "NONE"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)


@app.route('/add_wishlist', methods=['GET', 'POST'])
def add_wishlist():
    if request.method == "POST":
        fragrance = request.form.get('frag')
        if fragrance is not None:
            print("fragrance is " + fragrance)
        else:
            print("No fragrance name provided")
        return redirect(url_for('handle_wishlist'))
    else:
        return render_template('addWishlist.html')
    

@app.route('/add_fragrance_to_wishlist', methods=['POST', 'GET'])
def add_fragrance_to_wishlist():
    # Get the fragrance name from the form submission
    fragrance_name = request.form.get('fragrance_name')
    if fragrance_name is None:
        fragrance_name = request.form.get('fragrance_house')
        
    # print(fragrance_name)
    email = session.get('email')
    addedSuccessfully = logic.addToWishlist(dbCursor, conn, email, fragrance_name)
   
    if addedSuccessfully:
        return redirect(url_for('handle_wishlist'))
    else:
        return jsonify({'message': str(fragrance_name) + ' was not not found, or it is already a part of your wishlist... go back and try again'})


@app.route('/remove_wishlist', methods=['GET', 'POST'])
def remove_wishlist():
    sorting = "NONE"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('removeWishlist.html', fragrance_wishlist=fragrance_wishlist)

@app.route('/remove_fragrance_wishlist', methods=['POST', 'GET'])
def remove_fragrance_wishlist():
    name = request.form.get('fragrance_name')
    house = request.form.get('fragrance_house')
    logic.removeFragranceWishlist(dbCursor, conn, name, house, session['email'])
    return redirect(url_for('handle_wishlist'))


@app.route('/back_to_wishlist', methods=['POST', 'GET'])
def back_to_wishlist():
    return redirect(url_for('handle_wishlist'))









#SORTING FOR COLLECTION HERE 

@app.route('/alphabetically_sort_name_AZ_collection', methods=['POST', 'GET'])
def alphabetically_sort_name_AZ_collection():
    sorting = "AZbyName"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)


@app.route('/alphabetically_sort_name_ZA_collection', methods=['POST', 'GET'])
def alphabetically_sort_name_ZA_collection():
    sorting = "ZAbyName"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)


@app.route('/alphabetically_sort_house_AZ_collection', methods=['POST', 'GET'])
def alphabetically_sort_house_AZ_collection():
    sorting = "AZbyHouse"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)


@app.route('/alphabetically_sort_house_ZA_collection', methods=['POST', 'GET'])
def alphabetically_sort_house_ZA_collection():
    sorting = "ZAbyHouse"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)

@app.route('/newest_added_collection', methods=['POST', 'GET'])
def newest_added_collection():
    sorting = "NONE"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)


@app.route('/oldest_added_collection', methods=['POST', 'GET'])
def oldest_added_collection():
    sorting = "oldest"
    fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
    return render_template('collection.html', fragrance_collection=fragrance_collection)
















#SORTING FOR WISHLIST HERE 

@app.route('/alphabetically_sort_name_AZ', methods=['POST', 'GET'])
def alphabetically_sort_name_AZ():
    sorting = "AZbyName"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)


@app.route('/alphabetically_sort_name_ZA', methods=['POST', 'GET'])
def alphabetically_sort_name_ZA():
    sorting = "ZAbyName"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)


@app.route('/alphabetically_sort_house_AZ', methods=['POST', 'GET'])
def alphabetically_sort_house_AZ():
    sorting = "AZbyHouse"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)


@app.route('/alphabetically_sort_house_ZA', methods=['POST', 'GET'])
def alphabetically_sort_house_ZA():
    sorting = "ZAbyHouse"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)

@app.route('/newest_added', methods=['POST', 'GET'])
def newest_added():
    sorting = "NONE"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)


@app.route('/oldest_added', methods=['POST', 'GET'])
def oldest_added():
    sorting = "oldest"
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
    return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)








# REVIEWS HERE 

@app.route('/handle_reviews', methods=['POST', 'GET'])
def handle_reviews():
    sorting = "NONE"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    # print(reviews)
    return render_template('reviews.html', reviews=reviews, email=email)

@app.route('/back_to_reviews', methods=['POST', 'GET'])
def back_to_reviews():
    sorting = "NONE"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)


@app.route('/search_reviews', methods=['POST', 'GET'])
def search_reviews():
    if request.method == 'POST':
        fragrance = request.form.get('fragrance_name')
        return redirect(url_for('review_page', fragrance=fragrance))
    else:
        return render_template('reviewSearch.html')


@app.route('/review_page', methods=['GET'])
def review_page():
    email = session.get('email')  # Get the user's email from the session
    test = request.args.get('fragrance_house')
    if test is None:
        fragrance = request.args.get('fragrance_name')
        actual = fragrance.strip().split(" by ")
        if len(actual) == 1:
            return False
        fragrance_name = actual[0]
        fragrance_house = actual[1]
        if fragrance_name:
            fragrance_name = unquote(fragrance_name)
        if fragrance_house:
            fragrance_house = unquote(fragrance_house)
    else:
        fragrance_name = request.args.get('fragrance_name')
        fragrance_house = request.args.get('fragrance_house')
        if fragrance_name:
            fragrance_name = unquote(fragrance_name)
        if fragrance_house:
            fragrance_house = unquote(fragrance_house)

    sorting = request.args.get('sort_by', 'NONE')
    reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
    reviews = reviews_tuples
    average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
    user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating

    return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)


@app.route('/write_review', methods=['GET', 'POST'])
def write_review():
    if request.method == 'POST':
        fragrance_name = unquote(request.form.get('fragrance_name'))
        fragrance_house = unquote(request.form.get('fragrance_house'))
    else:
        fragrance_name = unquote(request.args.get('fragrance_name'))
        fragrance_house = unquote(request.args.get('fragrance_house'))

    # Ensure fragrance_name and fragrance_house are not None
    if not fragrance_name or not fragrance_house:
        return "Fragrance name and house are required.", 400

    return render_template('writeReview.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house)






# @app.route('/edit_review', methods=['POST','GET'])
# def edit_review():
#     revID = request.form.get('review_id')
#     name = request.form.get('fragrance_name')
#     house = request.form.get('fragrance_house')
#     review = request.form.get('review_text')
#     rating = request.form.get('rating')
#     if rating:
#         if rating >= '1' and rating <= '5':
#             rating = int(rating)
#     return render_template('editReview.html', fragrance_name=name, fragrance_house=house, review_text=review, rating=rating, review_id=revID)

@app.route('/edit_review')
def edit_review():
    review_id = request.args.get('review_id')
    fragrance_name = unquote(request.args.get('fragrance_name'))  # Decode the URL-encoded string
    fragrance_house = unquote(request.args.get('fragrance_house'))  # Decode the URL-encoded string
    
    # Query the database to get the review details based on the review_id
    review = logic.getFragranceReviewByID(dbCursor, review_id)
    
    # Ensure the review was found
    if not review:
        return "Review not found", 404

    # Pass the data to the template for rendering
    return render_template('editReview.html', 
                           review_id=review_id, 
                           fragrance_name=fragrance_name, 
                           fragrance_house=fragrance_house, 
                           review_text=review['Text'], 
                           rating=review['Rating'])

@app.route('/delete_review', methods=['POST'])
def delete_review():
    review_id = request.form.get('review_id')
    try:
        # Delete review from the database
        query1 = "DELETE FROM ReviewLikes WHERE Review_ID = %s"
        dbCursor.execute(query1, (review_id,))
        conn.commit()

        query3 = "DELETE FROM Reviews WHERE ReviewID = %s"
        dbCursor.execute(query3, (review_id,))
        conn.commit()
        return jsonify(success=True)
    except Exception as e:
        print(f"Error deleting review: {e}")
        conn.rollback()
        return jsonify(success=False)



@app.route('/submit_edited_review', methods=['POST'])
def submit_edited_review():
    name = request.form.get('fragrance_name')
    house = request.form.get('fragrance_house')
    reviewText = request.form.get('review_text')
    email = session.get('email')
    rating = request.form.get('rating')
    review_id = request.form.get('review_id')

    if not email:
        app.logger.warning("User not logged in.")
        return jsonify(success=False, message="User not logged in.")

    # Log the received data
    # app.logger.info(f"Received data: fragrance_name={name}, fragrance_house={house}, review_text={reviewText}, rating={rating}, email={email}")

    # If rating is None, handle it as you wish (e.g., set it to a specific value or leave it as None)

    # Logic to save the review and rating in the database
    try:
        success = logic.saveEditedFragranceReview(dbCursor, conn, name, house, reviewText, email, rating, review_id)
        if success:
            # app.logger.info("Review and rating saved successfully.")
            review_page_url = url_for('review_page', fragrance_name=name, fragrance_house=house)
            return jsonify(success=True, redirect_url=review_page_url)
        else:
            app.logger.warning("Failed to save review and rating in logic function.")
            return jsonify(success=False, message="Could not submit review and rating.")
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify(success=False, message=f"An error occurred while submitting review and rating: {str(e)}")




@app.route('/submit_review', methods=['POST'])
def submit_review():
    name = request.form.get('fragrance_name')
    house = request.form.get('fragrance_house')
    reviewText = request.form.get('review_text')
    email = session.get('email')
    rating = request.form.get('rating')

    if not email:
        app.logger.warning("User not logged in.")
        return jsonify(success=False, message="User not logged in.")

    # Log the received data
    # app.logger.info(f"Received data: fragrance_name={name}, fragrance_house={house}, review_text={reviewText}, rating={rating}, email={email}")

    # If rating is None, handle it as you wish (e.g., set it to a specific value or leave it as None)

    # Logic to save the review and rating in the database
    try:
        success = logic.saveFragranceReview(dbCursor, conn, name, house, reviewText, email, rating)
        conn.commit()
        if success:
            # app.logger.info("Review and rating saved successfully.")
            review_page_url = url_for('review_page', fragrance_name=name, fragrance_house=house)
            return jsonify(success=True, redirect_url=review_page_url)
        else:
            app.logger.warning("Failed to save review and rating in logic function.")
            return jsonify(success=False, message="Could not submit review and rating.")
    except Exception as e:
        app.logger.error(f"Exception occurred: {str(e)}")
        return jsonify(success=False, message=f"An error occurred while submitting review and rating: {str(e)}")



@app.route('/like_review', methods=['POST'])
def like_review():
    review_id = request.form['review_id']
    email = session['email']

    success = logic.add_like_review(dbCursor, conn, email, review_id)
    
    if success:
        query_check_like = "SELECT * FROM ReviewLikes WHERE ClientEmail = %s AND Review_ID = %s"
        dbCursor.execute(query_check_like, (email, review_id))
        like = dbCursor.fetchone()
        return jsonify(success=True, liked=(like is not None))
    else:
        return jsonify(success=False)
    

    
@app.route('/rate_fragrance',  methods=['POST'])
def rate_fragrance():
    rating = request.form.get('rating')
    email = session['email']    
    fragrance_name = request.form.get('fragrance_name')
    fragrance_house = request.form.get('fragrance_house')
    logic.addRating(dbCursor, conn, email, rating, fragrance_name, fragrance_house)
    return jsonify(success=True)


@app.route('/remove_rating', methods=['POST'])
def remove_rating():
    fragrance_name = request.form.get('fragrance_name')
    fragrance_house = request.form.get('fragrance_house')
    email = session.get('email')

    if not email:
        return jsonify(success=False, message="User not logged in.")

    try:
        # Remove the rating from ReviewRatings table
        deleteRating = "DELETE FROM ReviewRatings WHERE Client_Email = %s AND FragName = %s AND FragHouse = %s"
        dbCursor.execute(deleteRating, (email, fragrance_name, fragrance_house))
        conn.commit()

        return jsonify(success=True, message="Rating removed successfully.")
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, message=f"An error occurred while removing rating: {str(e)}")





# PROFILE PAGE HERE 
@app.route('/profile_page', methods=['POST', 'GET'])
def profile_page():
    review_email = request.args.get('user_email', session.get('email')) # the one of the review
    viewer_email = session['email'] 
    sorting = "NONE"
    fragrance_collection = logic.getFragranceCollection(dbCursor, review_email, sorting)
    fragrance_wishlist = logic.getFragranceWishlist(dbCursor, review_email, sorting)
    reviews = logic.getUserReviews(dbCursor, review_email, viewer_email)
    username = logic.getUsername(dbCursor, review_email)
    following_status = logic.is_following(dbCursor, viewer_email, review_email)

    followers = logic.getFollowers(dbCursor, review_email)
    following = logic.getFollowing(dbCursor, review_email)
    follower_count = len(followers)
    following_count = len(following)

    # follower_count = 79233
    if follower_count > 1000000:
        follower_count = f"{follower_count / 1000000:.1f}M"
    elif follower_count > 10000:
        follower_count = str(follower_count)[:-3] + "K"

    # print(follower_count)
    # following_count = 12343
    if following_count > 1000000:
        following_count = f"{following_count / 1000000:.1f}M"
    elif following_count > 10000:
        following_count = str(following_count)[:-3] + "K"

    # print(following_count)
    # userDetails = logic.getUserDetails(dbCursor, email)
    return render_template('profilePage.html', reviews=reviews, fragrance_collection=fragrance_collection, fragrance_wishlist=fragrance_wishlist, viewer_email=viewer_email, user_email=review_email, username=username, following_status=following_status, follower_count=follower_count, following_count=following_count, followers=followers, following=following)















#SORTING FOR REVIEWS HERE 

@app.route('/sort_reviews_oldest', methods=['POST', 'GET'])
def sort_reviews_oldest():
    sorting = "oldest"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)

@app.route('/sort_reviews_newest', methods=['POST', 'GET'])
def sort_reviews_newest():
    sorting = "NONE"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)

@app.route('/sort_reviews_popularity', methods=['POST', 'GET'])
def sort_reviews_popularity():
    sorting = "popularity"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)

@app.route('/sort_reviews_highest_rated', methods=['POST', 'GET'])
def sort_reviews_highest_rated():
    sorting = "highRated"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)

@app.route('/sort_reviews_lowest_rated', methods=['POST', 'GET'])
def sort_reviews_lowest_rated():
    sorting = "lowRated"
    email = session['email']
    reviews = logic.getAllReviews(dbCursor, email, sorting)
    return render_template('reviews.html', reviews=reviews, email=email)








#SORTING FOR REVIEWS HERE ON REVIEW PAGE
# ON REVIEW PAGE 

# @app.route('/sort_reviews_oldest_onpage', methods=['POST', 'GET'])
# def sort_reviews_oldest_onpage():
#     sorting = "oldest"
#     email = session['email']
#     fragrance_name = request.form.get('fragrance_name')
#     fragrance_house = request.form.get('fragrance_house')
#     print(fragrance_name)
#     print(fragrance_house)

#     reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
#     reviews = reviews_tuples
#     average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
#     user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating
#     return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)
    

# @app.route('/sort_reviews_newest_onpage', methods=['POST', 'GET'])
# def sort_reviews_newest_onpage():
#     sorting = "NONE"
#     email = session['email']
#     fragrance_name = request.form.get('fragrance_name')
#     fragrance_house = request.form.get('fragrance_house')
#     reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
#     reviews = reviews_tuples
#     average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
#     user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating
#     return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)

# @app.route('/sort_reviews_popularity_onpage', methods=['POST', 'GET'])
# def sort_reviews_popularity_onpage():
#     sorting = "popularity"
#     email = session['email']
#     fragrance_name = request.form.get('fragrance_name')
#     fragrance_house = request.form.get('fragrance_house')
#     reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
#     reviews = reviews_tuples
#     average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
#     user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating
#     return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)


# @app.route('/sort_reviews_highest_rated_onpage', methods=['POST', 'GET'])
# def sort_reviews_highest_rated_onpage():
#     sorting = "highRated"
#     email = session['email']
#     fragrance_name = request.form.get('fragrance_name')
#     fragrance_house = request.form.get('fragrance_house')
#     reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
#     reviews = reviews_tuples
#     average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
#     user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating
#     return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)

# @app.route('/sort_reviews_lowest_rated_onpage', methods=['POST', 'GET'])
# def sort_reviews_lowest_rated_onpage():
#     sorting = "lowRated"
#     email = session['email']
#     fragrance_name = request.form.get('fragrance_name')
#     fragrance_house = request.form.get('fragrance_house')
#     reviews_tuples = logic.getAllReviewsForReviewPage(dbCursor, email, sorting, fragrance_name, fragrance_house)
#     reviews = reviews_tuples
#     average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
#     user_rating = logic.getUserRating(dbCursor, email, fragrance_name, fragrance_house)  # Get the user's rating
#     return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating, user_rating=user_rating, email=email)










#REQUESTS HERE
@app.route('/request_fragrance', methods=['GET', 'POST'])
def request_fragrance():
    if request.method == 'POST':
        name = request.form.get('name')
        house = request.form.get('house')
        # print(name)
        # print(house)
        goodRequest = logic.sendRequest(dbCursor, conn, name, house, session['email'])
        if goodRequest:
            sorting = "NONE"
            fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
            return render_template('collection.html', fragrance_collection=fragrance_collection)
        else:
            return jsonify({'message': 'There was an error submitting your request, please try again'})
        # call fucntion in logic
    else:
        return render_template('requests.html')


@app.route('/request_fragrance_wishlist', methods=['GET', 'POST'])
def request_fragrance_wishlist():
    if request.method == 'POST':
        name = request.form.get('name')
        house = request.form.get('house')
        # print(name)
        # print(house)
        goodRequest = logic.sendRequest(dbCursor, conn, name, house, session['email'])
        if goodRequest:
            sorting = "NONE"
            fragrance_wishlist = logic.getFragranceWishlist(dbCursor, session['email'], sorting)
            return render_template('wishlist.html', fragrance_wishlist=fragrance_wishlist)
        else:
            return jsonify({'message': 'There was an error submitting your request, please try again'})
        # call fucntion in logic
    else:
        return render_template('requestsWishlist.html')
    



#FOLLOWING HERE
@app.route('/toggle_follow', methods=['POST'])
def toggle_follow():
    follower_email = request.form.get('follower_email')
    following_email = request.form.get('following_email')
    # print(follower_email)
    # print("this is following" + following_email)
    # print()
    if logic.is_following(dbCursor, follower_email, following_email):
        # Unfollow the user
        query = "DELETE FROM Follows WHERE FollowerEmail = %s AND FollowingEmail = %s"
        dbCursor.execute(query, (follower_email, following_email))
        conn.commit()
    else:
        # Follow the user
        query = "INSERT INTO Follows (FollowerEmail, FollowingEmail, DateFollowed) VALUES (%s, %s, CURRENT_TIMESTAMP)"
        dbCursor.execute(query, (follower_email, following_email))
        conn.commit()
    print(follower_email) # cjm (me)
    print(following_email) # oliver (other)
    return redirect(url_for('profile_page', user_email=following_email))



# SEARCHING FOR USERS HERE 
@app.route('/search_users', methods=['POST', 'GET'])
def search_users():
    if request.method == 'GET':
        email = session['email']
        return render_template('userSearch.html', viewer_email=email)
    elif request.method == 'POST':
        query = request.form.get('query', '')
        if query:
            users = logic.searchUsers(dbCursor, query)
            # print(users)
            return jsonify(users)
        return jsonify([])


@app.route('/go_to_user_profile', methods=['POST'])
def go_to_user_profile():
    username = request.form.get('user')
    # print(username)
    user_email = logic.getUserEmailByUsername(dbCursor, username)
    if user_email:
        return redirect(url_for('profile_page', user_email=user_email))
    return redirect(url_for('profile_page'))





@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session
    session.clear()
    # Redirect to the index page
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)