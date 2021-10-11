
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Item;
DROP TABLE IF EXISTS Bid;
DROP TABLE IF EXISTS Category;

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Person (
    id VARCHAR(20) PRIMARY KEY,
    rating INT,
    location VARCHAR(20),
    country VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS  Item (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    currently VARCHAR(20),
    buy_price VARCHAR(20),
    first_bid VARCHAR(20),
    number_of_bids INT,
    started VARCHAR(20),
    ends VARCHAR(20),
    seller VARCHAR(20),
    description VARCHAR(20),
    FOREIGN KEY (seller) REFERENCES Person(id)
);

CREATE TABLE IF NOT EXISTS  Bid (
    id INT PRIMARY KEY,
    time VARCHAR(20) NOT NULL,
    bidder VARCHAR(20),
    amount VARCHAR(20) NOT NULL,
    bid_on INT,
    FOREIGN KEY (bidder) REFERENCES Person (id),
    FOREIGN KEY (bid_on) REFERENCES Item (id)
);

CREATE TABLE IF NOT EXISTS  Category (
    name VARCHAR(20),
    item INT,
    PRIMARY KEY (name, item)
);

