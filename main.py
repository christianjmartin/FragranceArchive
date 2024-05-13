

#START HERE, COMMAND LINE ARGS ... i have a macbook. may be different for windows 

# python3 -m venv path/to/venv
# source path/to/venv/bin/activate
# python3 -m pip install psycopg2
# python3 -m pip install flask

#TO RUN

# python3 main.py


from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="LibraryProject",
    user="postgres",
    password="Blackopz2!"
)
dbCursor = conn.cursor()

def sampleFunc(dbCursor):
    query = "SELECT * FROM Document"
    dbCursor.execute(query)
    rows = dbCursor.fetchall()
    return rows  # Return the rows to be displayed in the template

@app.route('/')
def home():
    # Render the home page template
    return render_template('index.html')

@app.route('/handle_collection', methods=['POST'])
def handle_collection():
    # Handle the colleciton
    return render_template('collection.html')

@app.route('/handle_wishlist', methods=['POST'])
def handle_wishlist():
    # Handle the wishlist
    return render_template('wishlist.html')

# You can define more routes as needed

if __name__ == '__main__':
    # Run the Flask application
    app.run(debug=True)