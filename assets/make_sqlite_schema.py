import sqlite3 

conn = sqlite3.connect('remoters.db')

curs = conn.cursor()

create_article_stmt = """
CREATE TABLE article
(
    ARTICLE_ID INT PRIMARY KEY  NOT NULL,
    URL TEXT                    NOT NULL, 
    DATE TEXT                   NOT NULL, --SQLite has no date datatype
    PLAIN_TEXT TEXT             NOT NULL,
    SOURCE TEXT                 NOT NULL
);
"""

create_sentiment_rating_stmt = """
CREATE TABLE sentiment_rating
(
    ARTICLE_ID INT NOT NULL,
    METHOD TEXT NOT NULL,
    RATING FLOAT NOT NULL,
    FOREIGN KEY(ARTICLE_ID) REFERENCES article(ARTICLE_ID)
);
"""

# Checking if tables exist
tables_list = curs.execute(
  """SELECT tableName FROM sqlite_master WHERE type='table'
  AND (tableName='ARTICLE' OR tableName='SENTIMENT_RATING'); """).fetchall()

assert len(tables_list) == 0, "Error: Database already has tables!"

curs.execute(create_article_stmt)

conn.commit()

curs.execute(create_sentiment_rating_stmt)

conn.commit()
print("Tables created successfully")
conn.close()