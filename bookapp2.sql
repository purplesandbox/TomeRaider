CREATE DATABASE Bookapp;

USE Bookapp;
CREATE TABLE books(
    id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    series VARCHAR(200),
    book_type VARCHAR(200),
    lexile_min INTEGER,
    lexile_max INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE read_books( 
 id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    series VARCHAR(200),
    book_type VARCHAR(200),
    lexile_min INTEGER,
    lexile_max INTEGER,
    review MEDIUMTEXT,
    star_rating ENUM('1','2','3','4','5'),
    PRIMARY KEY (id)
);

CREATE TABLE to_read_books( 
 id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    series VARCHAR(200),
    book_type VARCHAR(200),
    lexile_min INTEGER,
    lexile_max INTEGER,
    PRIMARY KEY (id)
);

SELECT * FROM to_read_books;
    

-- INSERT INTO books(title, author, series, book_type, lexile_min, lexile_max)
-- VALUES()

