#!/usr/bin/env python
import psycopg2

# Fetch records from the database.
try:
    db = psycopg2.connect("dbname=news")
except Exception:
    print ("Unable to connect to the database")
    raise

c = db.cursor()

articles_query = "SELECT * FROM top_articles_titles"
authors_query = "SELECT * FROM top_authors_articles"
error_date_query = "SELECT * FROM error_date"
c.execute(articles_query)
articles = c.fetchall()
c.execute(authors_query)
authors = c.fetchall()
c.execute(error_date_query)
error_dates = c.fetchall()

question1 = "What are the most popular three articles of all time?"
question2 = "Who are the most popular article authors of all time?"
question3 = "On which days did more than 1'%' of requests lead to errors?"

# Log reports
print question1
for row in articles:
    row = list(row)
    print(" "+row[0]+" with "+str(row[1])+" Views")
print
print question2
for row in authors:
    row = list(row)
    print(" "+row[0]+" with "+str(row[1])+" Views")
print
print question3
for row in error_dates:
    print(" "+str(row[0])+" with "+str(round(row[3], 2))+"% Views")
db.close()
