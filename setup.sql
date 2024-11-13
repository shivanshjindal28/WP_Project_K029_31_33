-- SQL file to set up the PostgreSQL database structure

CREATE TABLE Users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE Transactions (
  transaction_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES Users(user_id),
  amount DECIMAL NOT NULL,
  type VARCHAR(10) CHECK (type IN ('income', 'expense')),
  category VARCHAR(30),
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
