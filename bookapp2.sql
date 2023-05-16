CREATE DATABASE Bookapp;

USE Bookapp;


CREATE TABLE read_books( 
 id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    category AS genre VARCHAR(200),
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
    category AS genre VARCHAR(200),
    lexile_min INTEGER,
    lexile_max INTEGER,
    PRIMARY KEY (id)
);

 
