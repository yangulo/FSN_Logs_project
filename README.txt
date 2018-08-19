**DESCRIPTION**
This project extracts data from the news databse and reports results.

In order to access the news database you need to have VM and vagrant installed. 1. First cd vagrant and run vagrant ssh and vagrant up
2. Use psql -d news -f newsdata.sql
3. Run psql, then use \c news to connect to news databse

**FILES**
newsdata.py
newsdata_output.txt

**CREATE VIEW COMMANDS**
CREATE VIEW top_articles AS
SELECT title, total, author
FROM (
select substring(path,10, 7) as short_title, count(*) as total
from log
group by short_title
order by total desc) AS top_articles
INNER JOIN articles
ON short_title = replace(lower(substring(title,1,7)),' ', '-') 
ORDER BY total DESC
LIMIT 3;

CREATE VIEW top_authors AS
SELECT a.id, a.name, title, total
FROM authors AS a
INNER JOIN  
top_articles
ON a.id=top_articles.author 
ORDER BY title desc;

CREATE VIEW error_date AS
SELECT A.date_tmp, total_errors, total_requests, (total_errors*100.0/total_requests) as percentage 
FROM 
(SELECT date(time) as date_tmp, count(*) as total_errors
FROM log
WHERE status <> '200 OK'
GROUP BY date_tmp
ORDER BY 1) as A
INNER JOIN
(SELECT date(time) as date_tmp, count(*) as total_requests
FROM log
GROUP BY date_tmp
ORDER BY 1) as B
ON A.date_tmp=B.date_tmp
WHERE (total_errors*100.0/total_requests) >1;

**QUESTIONS**
What are the most popular three articles of all time?
Who are the most popular article authors of all time?
On which days did more than 1% of requests lead to errors?


