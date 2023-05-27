CREATE DATABASE TomeRaider;

USE TomeRaider;


CREATE TABLE read_books( 
 id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    category VARCHAR(200),
    review MEDIUMTEXT,
    star_rating ENUM('1','2','3','4','5'),
    PRIMARY KEY (id)
);

CREATE TABLE to_read_books( 
 id int NOT NULL AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(200),
    category VARCHAR(200),
    PRIMARY KEY (id)
);

 
