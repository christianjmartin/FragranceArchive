

#START HERE, COMMAND LINE ARGS ... i have a macbook. may be different for windows 

# python3 -m venv path/to/venv
# source path/to/venv/bin/activate
# python3 -m pip install psycopg2
# python3 -m pip install flask

#TO RUN

# python3 main.py


from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import psycopg2
import junk
import logic

app = Flask(__name__)
app.secret_key = '123456789'

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="FragranceDatabase",
    user="postgres",
    password=junk.string_list[45],
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
        session['email'] = email
        session['name'] = name
        password = request.form.get('password')

        # Process form data (validate, create user, etc.)
        if name and email and password:
            validSignup = logic.validateSignup(dbCursor, conn, name, email, password)
            if validSignup:
                return redirect(url_for('handle_menu', userName = session['name']))  # Placeholder response
            else:
                return 'An account with this email address already exists, please choose a different email or go back and log in'
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
    return render_template('menu.html', userName = session['name'])






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
    reviews = logic.getAllReviews(dbCursor, sorting)
    # print(reviews)
    return render_template('reviews.html', reviews=reviews)

@app.route('/back_to_reviews', methods=['POST', 'GET'])
def back_to_reviews():
    sorting = "NONE"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)


@app.route('/search_reviews', methods=['POST', 'GET'])
def search_reviews():
    if request.method == 'POST':
        fragrance = request.form.get('fragrance_name')
        return redirect(url_for('review_page', fragrance=fragrance))
    else:
        return render_template('reviewSearch.html')


@app.route('/review_page', methods=['GET'])
def review_page():
    test = request.args.get('fragrance_house')
    if test is None:
        fragrance = request.args.get('fragrance_name')
        actual = fragrance.strip().split(" by ")
        if len(actual) == 1:
            return False
        fragrance_name = actual[0]
        fragrance_house = actual[1]
    else:
        fragrance_name = request.args.get('fragrance_name')
        fragrance_house = request.args.get('fragrance_house')

    reviews_tuples = logic.getFragranceReviews(dbCursor, fragrance_name, fragrance_house)
    reviews = reviews_tuples
    average_rating = logic.getAverageRating(dbCursor, fragrance_name, fragrance_house)
    return render_template('reviewPage.html', fragrance_name=fragrance_name, fragrance_house=fragrance_house, reviews=reviews, average_rating=average_rating)


@app.route('/write_review', methods=['POST', 'GET'])
def write_review():
    name = request.form.get('fragrance_name')
    house = request.form.get('fragrance_house')
    return render_template('writeReview.html', fragrance_name=name, fragrance_house=house)


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
    app.logger.info(f"Received data: fragrance_name={name}, fragrance_house={house}, review_text={reviewText}, rating={rating}, email={email}")

    # If rating is None, handle it as you wish (e.g., set it to a specific value or leave it as None)

    # Logic to save the review and rating in the database
    try:
        success = logic.saveFragranceReview(dbCursor, conn, name, house, reviewText, email, rating)
        conn.commit()
        if success:
            app.logger.info("Review and rating saved successfully.")
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
    reviewID = request.form.get('review_id')
    email = session['email']
    if logic.add_like_review(dbCursor, conn, email, reviewID):
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="You've already liked this fragrance")
    

    
@app.route('/rate_fragrance',  methods=['POST'])
def rate_fragrance():
    rating = request.form.get('rating')
    email = session['email']    
    fragrance_name = request.form.get('fragrance_name')
    fragrance_house = request.form.get('fragrance_house')
    logic.addRating(dbCursor, conn, email, rating, fragrance_name, fragrance_house)
    return jsonify(success=True)















#SORTING FOR REVIEWS HERE 

@app.route('/sort_reviews_oldest', methods=['POST', 'GET'])
def sort_reviews_oldest():
    sorting = "oldest"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)

@app.route('/sort_reviews_newest', methods=['POST', 'GET'])
def sort_reviews_newest():
    sorting = "NONE"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)

@app.route('/sort_reviews_popularity', methods=['POST', 'GET'])
def sort_reviews_popularity():
    sorting = "popularity"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)


# HMMM HOW TO DO THIS??? NEED TO JOIN TABLES FOR THE reviews OBJECT, BUT NEED REVIEWS FROM REVIEWSRATING TABLE
# since adding a review auto rates a frag, the reviewratings table should always have all info and more, however without duplicates
@app.route('/sort_reviews_highest_rated', methods=['POST', 'GET'])
def sort_reviews_highest_rated():
    sorting = "highRated"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)

@app.route('/sort_reviews_lowest_rated', methods=['POST', 'GET'])
def sort_reviews_lowest_rated():
    sorting = "lowRated"
    reviews = logic.getAllReviews(dbCursor, sorting)
    return render_template('reviews.html', reviews=reviews)














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
            fragrance_collection = logic.getFragranceCollection(dbCursor, session['email'], sorting)
            return render_template('wishlist.html', fragrance_collection=fragrance_collection)
        else:
            return jsonify({'message': 'There was an error submitting your request, please try again'})
        # call fucntion in logic
    else:
        return render_template('requestsWishlist.html')



@app.route('/logout', methods=['POST'])
def logout():
    # Clear the user session
    session.clear()
    # Redirect to the index page
    return redirect(url_for('home'))

# You can define more routes as needed

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)