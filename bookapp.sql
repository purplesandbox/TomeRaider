CREATE DATABASE Bookapp;

USE Bookapp;
CREATE TABLE books(
    id INTEGER PRIMARY KEY,
    title VARCHAR(200),
    author VARCHAR(200),
    series VARCHAR(200),
    book_type VARCHAR(200),
    lexile_min INTEGER,
    lexile_max INTEGER
);


INSERT INTO books(title, author, series, book_type, lexile_min, lexile_max)
VALUES()

