CREATE TABLE Client (
    Email VARCHAR(100) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Username VARCHAR(100) NOT NULL UNIQUE
);


CREATE TABLE Fragrance (
    FragranceID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    House VARCHAR(100)
);


CREATE TABLE Collection (
    CollectionID SERIAL PRIMARY KEY,
    ClientEmail VARCHAR(100) NOT NULL,
    FragranceID INT NOT NULL,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (FragranceID) REFERENCES Fragrance(FragranceID)
);


CREATE TABLE Wishlist (
    WishlistID SERIAL PRIMARY KEY,
    ClientEmail VARCHAR(100) NOT NULL,
    FragranceID INT NOT NULL,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (FragranceID) REFERENCES Fragrance(FragranceID)
);

CREATE TABLE Requests (
    RequestID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    House VARCHAR(100),
    ClientEmail VARCHAR(100) NOT NULL,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email)
);


CREATE TABLE Reviews (
    ReviewID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    House VARCHAR(100),
    Review TEXT,
    ClientEmail VARCHAR(100) NOT NULL,
    ClientName VARCHAR(100) NOT NULL,
    Likes INT DEFAULT 0,
    Rating INTEGER,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email)
);

CREATE TABLE ReviewLikes (
    ReviewLikesID SERIAL PRIMARY KEY,
    ClientEmail VARCHAR(100) NOT NULL,
    Review_ID INTEGER,
    UNIQUE(ClientEmail, Review_ID),
    FOREIGN KEY (Review_ID) REFERENCES Reviews(ReviewID),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email)
);


CREATE TABLE ReviewRatings (
    ReviewRatingsID SERIAL PRIMARY KEY,
    Client_Email VARCHAR(100) NOT NULL,
    Rating INTEGER NOT NULL,
    FragName VARCHAR(255),
    FragHouse VARCHAR(100),
    FOREIGN KEY (Client_Email) REFERENCES Client(Email)
);

CREATE TABLE Follows (
    FollowerEmail VARCHAR(100) NOT NULL,
    FollowingEmail VARCHAR(100) NOT NULL,
    DateFollowed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (FollowerEmail, FollowingEmail),
    FOREIGN KEY (FollowerEmail) REFERENCES Client(Email),
    FOREIGN KEY (FollowingEmail) REFERENCES Client(Email)
);

CREATE TABLE fragrance_of_the_week (
    id SERIAL PRIMARY KEY,
    week_number INT NOT NULL,
    fragrance_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    image_url VARCHAR(255) NOT NULL
);

-- CREATE TABLE Reviews ();




-- CREATE TABLE Client (
--     Email VARCHAR(100) PRIMARY KEY,
--     Name VARCHAR(100) NOT NULL,
--     Password VARCHAR(100) NOT NULL,
--     ProfilePicture VARCHAR(255)
-- );

-- CREATE TABLE Fragrance (
--     FragranceID SERIAL PRIMARY KEY,
--     Name VARCHAR(255),
--     House VARCHAR(100)
-- );

-- CREATE TABLE Collection (
--     CollectionID SERIAL PRIMARY KEY,
--     ClientEmail VARCHAR(100) NOT NULL,
--     FragranceID INT NOT NULL,
--     FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
--     FOREIGN KEY (FragranceID) REFERENCES Fragrance(FragranceID)
-- );

-- CREATE TABLE Wishlist (
--     WishlistID SERIAL PRIMARY KEY,
--     ClientEmail VARCHAR(100) NOT NULL,
--     FragranceID INT NOT NULL,
--     FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
--     FOREIGN KEY (FragranceID) REFERENCES Fragrance(FragranceID)
-- );

-- CREATE TABLE Requests (
--     RequestID SERIAL PRIMARY KEY,
--     ClientEmail VARCHAR(100) NOT NULL,
--     Name VARCHAR(255),
--     House VARCHAR(100),
--     FOREIGN KEY (ClientEmail) REFERENCES Client(Email)
-- );

-- CREATE TABLE Follows (
--     FollowerEmail VARCHAR(100) NOT NULL,
--     FollowingEmail VARCHAR(100) NOT NULL,
--     PRIMARY KEY (FollowerEmail, FollowingEmail),
--     FOREIGN KEY (FollowerEmail) REFERENCES Client(Email),
--     FOREIGN KEY (FollowingEmail) REFERENCES Client(Email)
-- );

-- CREATE TABLE Reviews (
--     ReviewID SERIAL PRIMARY KEY,
--     ClientEmail VARCHAR(100) NOT NULL,
--     FragranceID INT NOT NULL,
--     ReviewText TEXT,
--     Rating INT,
--     FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
--     FOREIGN KEY (FragranceID) REFERENCES Fragrance(FragranceID)
-- );