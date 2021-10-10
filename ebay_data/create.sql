PRAGMA foreign_keys = ON;


DROP TABLE if exists Item;
DROP TABLE if exists Bid;
DROP TABLE if exists Person;
DROP TABLE if exists Category;



CREATE TABLE Person (
    id VARCHAR(20) PRIMARY KEY,
    rating INT,
    location VARCHAR(20) NOT NULL,
    country VARCHAR(20) NOT NULL
  
);

CREATE TABLE Item (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    currently VARCHAR(20),
    buy_price VARCHAR(20),
    first_bid VARCHAR(20),
    location VARCHAR(20),
    country VARCHAR(20),
    started VARCHAR(20),
    ends VARCHAR(20),
    description VARCHAR(20),
    seller VARCHAR(20),
    FOREIGN KEY (seller) REFERENCES Person(id)
);

CREATE TABLE Bid (
    id INT PRIMARY KEY,
    time VARCHAR(20) NOT NULL,
    amount VARCHAR(20) NOT NULL,
    bidder VARCHAR(20),
    bid_on INT,
    FOREIGN KEY (bidder) REFERENCES Person (id),
    FOREIGN KEY (bid_on) REFERENCES Item (id)
);

CREATE TABLE Category (
    name VARCHAR(20),
    item INT,
    PRIMARY KEY (name, item)
);