<h1>Project Description</h1>
<p>This project extracts and interprets data from the news databse in order to answwer these three following questions;</p>
<ul>
 <li>What are the most popular three articles of all time?</li>
 <li>Who are the most popular article authors of all time?</li>
 <li>On which days did more than 1% of requests lead to errors?</li>
</ul>

<p>I have created some views on the database listed below. The file newsdata.py has a script that presents the information from the database and reports it in plain text to make it easy to understand for the user.</p>

<h2>TO INSTALL</h2>
<ol>
 <li>You need to have python 3 installed. Follow the instruction in the link below depending on your OS system
 https://realpython.com/installing-python/</li>
 <li>Install VirtualBox. VirtualBox is the software that actually runs the virtual machine. You can download it from virtualbox.org, in the following link
 https://www.virtualbox.org/wiki/Download_Old_Builds_5_1</li>
 <li>Install Vagrant. Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem. Download it from vagrantup.com.
 In order to access the news database you need to have VM and vagrant installed. First cd vagrant and run vagrant ssh and vagrant up</li>
 <li>Use psql -d news -f newsdata.sql</li>
 <li>Run psql, then use \c news to connect to news databse</li>
</ol>

<h2>FILES</h2>
<ul>
 <li>newsdata.py</li>
 <li>newsdata_output.txt</li>
</ul>

<h2>CREATE VIEW COMMANDS</h2>
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
