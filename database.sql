/* create tables */

/* Create table for Client */
CREATE TABLE Client (
    Email VARCHAR(100) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Password VARCHAR(100) NOT NULL
);

/* create table for Address */
CREATE TABLE Address (
    AddressID SERIAL PRIMARY KEY,
    Street VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(100),
    ZipCode VARCHAR(20) NOT NULL
);

/* Intermediary table for Client-Address relationship to allow multiple addresses per client */
CREATE TABLE ClientAddress (
    ClientEmail VARCHAR(100) NOT NULL,
    AddressID INT NOT NULL,
    PRIMARY KEY (ClientEmail, AddressID),
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (AddressID) REFERENCES Address(AddressID)
);

/* create table for Credit Card */
CREATE TABLE CreditCard (
    CardNumber VARCHAR(20) PRIMARY KEY,
    ExpiryDate DATE NOT NULL,
    CVV VARCHAR(10) NOT NULL,
    BillingAddressID INT NOT NULL,
    FOREIGN KEY (BillingAddressID) REFERENCES Address(AddressID)
);

/* create table for Payment */
CREATE TABLE Payment (
    PaymentID SERIAL PRIMARY KEY,
    Amount DECIMAL(10,2) NOT NULL,
    Date TIMESTAMP NOT NULL,
    ClientEmail VARCHAR(100) NOT NULL,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email)
);

/* create table for Librarian */
CREATE TABLE Librarian (
    SSN NUMERIC(9,0) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Salary DECIMAL(10,2) NOT NULL
);


/* create table for Document */
CREATE TABLE Document (
    DocumentID SERIAL PRIMARY KEY,
    Title VARCHAR(255),
    Type VARCHAR(100),
    Author VARCHAR(255),
    Publisher VARCHAR(255),
    AvailableCopies INT NOT NULL DEFAULT 0,
    TotalCopies INT NOT NULL DEFAULT 0
);

/* create table for Book */
CREATE TABLE Book (
    ISBN VARCHAR(20) PRIMARY KEY,
    Genre VARCHAR(100),
	
	/* maybe we should add these to the ER model */
    DocumentID INT NOT NULL,
    FOREIGN KEY (DocumentID) REFERENCES Document(DocumentID)
);

/* create table for Magazine */
CREATE TABLE Magazine (
    ISSN VARCHAR(20) PRIMARY KEY,
    Genre VARCHAR(100),
    DocumentID INT NOT NULL,
    FOREIGN KEY (DocumentID) REFERENCES Document(DocumentID)
);

/* Create table for Journal Article */
CREATE TABLE JournalArticle (
    ArticleID SERIAL PRIMARY KEY,
    JournalName VARCHAR(255),
    DocumentID INT NOT NULL,
    FOREIGN KEY (DocumentID) REFERENCES Document(DocumentID)
);

/* create table for Borrowing */ 
CREATE TABLE Borrowing (
    BorrowID SERIAL PRIMARY KEY,
    ClientEmail VARCHAR(100) NOT NULL,
    DocumentID INT NOT NULL,
    BorrowDate TIMESTAMP,
    ReturnDate TIMESTAMP,
    FOREIGN KEY (ClientEmail) REFERENCES Client(Email),
    FOREIGN KEY (DocumentID) REFERENCES Document(DocumentID)
);

/* Indexes for performance */
CREATE INDEX index_client_email ON Client(Email);

CREATE INDEX index_borrowing_doc_id ON Borrowing(DocumentID);
CREATE INDEX index_book_doc_id ON Book(DocumentID);
CREATE INDEX index_magazine_doc_id ON Magazine(DocumentID);
CREATE INDEX index_article_doc_id ON JournalArticle(DocumentID);