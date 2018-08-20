**DESCRIPTION**
This project extracts data from the news databse and reports results to answer the three following questions

What are the most popular three articles of all time?
Who are the most popular article authors of all time?
On which days did more than 1% of requests lead to errors?

I created views on the database to extract the information which are listed below. The file newsdata.py has a script that brings the information from the database and reports it in plain text to make it easy to understand.

**TO INSTALL**
1. You need to have python 3 installed. Follow the instruction in the link below depending on your OS system
https://realpython.com/installing-python/
2. Install VirtualBox. VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, in the following link
https://www.virtualbox.org/wiki/Download_Old_Builds_5_1
3. Install Vagrant. Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com. 
In order to access the news database you need to have VM and vagrant installed. 1. First cd vagrant and run vagrant ssh and vagrant up
2. Use psql -d news -f newsdata.sql
3. Run psql, then use \c news to connect to news databse

**FILES**
newsdata.py
newsdata_output.txt

**CREATE VIEW COMMANDS**
CREATE VIEW top_articles AS
SELECT substring(path,10,length(path)) AS ns, 
count(*) AS total 
FROM log
GROUP BY ns
HAVING substring(path,10,length(path)) <> ''
ORDER BY total DESC
LIMIT 3;

CREATE VIEW top_articles_titles AS 
SELECT title, total
FROM articles
INNER JOIN top_articles
ON ns=slug
LIMIT 3;

CREATE VIEW top_authors AS
SELECT sum(total) as total, author
FROM top_articles
INNER JOIN articles
ON slug=ns
GROUP BY author
ORDER BY total DESC;

CREATE VIEW top_authors_articles AS
SELECT name, total
FROM authors
INNER JOIN top_authors
ON id=author;

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

