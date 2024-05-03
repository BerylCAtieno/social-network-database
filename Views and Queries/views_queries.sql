SET search_path TO social_network_db;


-- PART 2(a): View Creation

/*
The friendship relationship is stored as a directed relationship. To comfortably solve
queries regarding the friendship relationship, the relationships should be stored as
undirected. In this regard, you should create a view "pkp_symmetric" that contains
both directions.
*/

CREATE VIEW pkp_symmetric AS
SELECT personID_A AS personID_1, personID_B AS personID_2, creationDate
FROM person_knows_Person
UNION
SELECT personID_B AS personID_1, personID_A AS personID_2, creationDate
FROM person_knows_Person;

SELECT * FROM pkp_symmetric;

/*
Sample output

  personid_1   |   personid_2   |      creationdate
----------------+----------------+-------------------------
 12094627905567 | 13194139533352 | 2012-02-25 15:54:14.72
 10995116277851 | 10995116277857 | 2012-01-02 01:07:22.747
  7696581394461 | 10995116277826 | 2011-11-02 10:46:59.205
  2199023255625 | 16492674416689 | 2012-09-11 04:07:15.731
  2199023255628 |  7696581394474 | 2011-05-23 14:43:18.32

*/

--PART 2(b): Views and Queries

--1) In how many different European cities are there universities?

SELECT COUNT(DISTINCT uni.cityID)
FROM university as uni
JOIN city
    ON uni.cityid=city.cityID
JOIN country
    ON city.ispartof=country.countryID
JOIN continent 
    ON country.ispartof = continent.continentID
JOIN place 
    ON place.placeID = continent.continentID
WHERE place."name"='Europe';

-- Output: 249


-- 2) How many forum posts has the youngest person authored

SELECT person.firstname, person.lastname, COUNT(post.postid)
FROM post  
JOIN "message" ON post.postid = "message".messageid
JOIN person ON "message".creator = person.personid
WHERE person.birthday = (SELECT MAX(person.birthday)FROM person )
GROUP BY person.firstname, person.lastname;

/*
Output

  firstname | lastname | count
-----------+----------+-------
 Paul      | Becker   |   232
*/

-- 3) How many comments on posts are there from each country

SELECT  place.name , COUNT(COALESCE(post.postid, 0)) as comment_count 
FROM post 
JOIN "message" 
ON post.postid = "message".messageid
JOIN country
ON "message".countryid= country.countryid
join place on country.countryid=place.placeid
GROUP BY place.name 
ORDER BY comment_count;

/*
Output
         name          | kommentaranzahl
------------------------+-----------------
 Laos                   |               1
 Slovakia               |               1
 Kenya                  |               1
 El_Salvador            |               1
 South_Africa           |               1
 Philippines            |               1
 Peru                   |               1
 Norway                 |               1
 Swaziland              |               1
 Algeria                |               1
 Panama                 |               1
 Yemen                  |               1
*/

-- 4) From which cities do most users come

SELECT place."name", count(person.personid) AS "no_of_users" 
FROM person
JOIN city ON city.cityid = person.cityid
JOIN place ON place.placeid = city.cityid
GROUP BY place."name"
order by "no_of_users" DESC;


-- 5) Who is 'Hans Johansson' friends with?

SELECT personid, firstname, lastname
FROM pkp_symmetric
JOIN person ON pkp_symmetric.personid_2 = person.personid
where pkp_symmetric.personid_1 = (SELECT personid FROM person where firstname = 'Hans');

-- 6) Who are the "real" friends-of-a-friend of 'Hans Johansson'?

SELECT personid, firstname, lastname
FROM pkp_symmetric
JOIN person ON pkp_symmetric.personid_2 = person.personid
where pkp_symmetric.personid_1 in (SELECT person.personid
FROM pkp_symmetric
JOIN person ON pkp_symmetric.personid_2 = person.personid
where pkp_symmetric.personid_1 = (SELECT personid FROM person where firstname = 'Hans'))
AND person.personid not in (SELECT person.personid
FROM pkp_symmetric
JOIN person ON pkp_symmetric.personid_2 = person.personid
where pkp_symmetric.personid_1 = (SELECT personid FROM person where firstname = 'Hans'))
AND firstname != 'Hans';

-- 7) Which users are members in all forums where 'Mehmet Koksal' is also a member?

SELECT person.firstname, person.lastname
FROM (
SELECT personid, COUNT(DISTINCT forumid) AS num_forums
FROM forum_hasmember
WHERE forumid IN (SELECT forumid FROM forum_hasmember JOIN person ON forum_hasmember.personid = person.personid where person.firstname = 'Mehmet' and person.lastname = 'Koksal')
GROUP BY personid
) AS subquery
JOIN person ON subquery.personid = person.personid
WHERE num_forums = 3;


-- 8) Provide the percentage distribution of users by their origin from different continents.

SELECT place."name", 
    COUNT (person.personid)*100/(SELECT COUNT(person.personid)
                                FROM person) AS "percentage"
FROM person 
JOIN city ON city.cityid = person.cityid
JOIN country ON country.countryid = city.ispartof
JOIN continent ON continent.continentid = country.ispartof
JOIN place ON place.placeid = continentid
GROUP BY place."name";


-- 9) Which forums contain more posts than the average number of posts in forums

SELECT forum.title, COUNT(post.postid) AS post_count
FROM forum 
JOIN post ON forum.forumid=post.forumid
GROUP BY forum.title
HAVING COUNT(post.postid) > (
	(SELECT COUNT(post.postid)FROM post )/(SELECT COUNT (forum.forumid) FROM forum)
) ORDER BY forum.title ;


-- 10) Which persons are friends with the person who received the most likes on a post?
--     Sort the output alphabetically by last name.

WITH MostLikedPerson AS (
    SELECT p.personID, p.firstName, p.lastName
    FROM person p
    JOIN (
        SELECT m.creator AS personID
        FROM "message" m
        JOIN (
            SELECT messageID, COUNT(*) AS likes_count
            FROM person_likes_Message
            GROUP BY messageID
            ORDER BY likes_count DESC
            LIMIT 1
        ) AS top_post_likes ON m.messageID = top_post_likes.messageID
    ) AS top_likes_person ON p.personID = top_likes_person.personID
),
FriendsOfMostLiked AS (
    SELECT DISTINCT fk.personID_2 AS friendID
    FROM pkp_symmetric fk
    JOIN MostLikedPerson mlp ON fk.personID_1 = mlp.personID
)
SELECT p.personID, p.firstName, p.lastName
FROM person p
JOIN FriendsOfMostLiked fm ON p.personID = fm.friendID
ORDER BY p.lastName;


-- 11) Which persons are directly or indirectly connected to 'Jun Hu' (id 94) (friends)? 
--     Provide for each person the minimum distance to Jun

WITH RECURSIVE DirectFriends AS (
  SELECT personID_B AS personID, 1 AS distance
  FROM person_knows_Person
  WHERE personID_A = 94
  UNION ALL
  SELECT kp.personID_B, df.distance + 1
  FROM DirectFriends df
  JOIN person_knows_Person kp ON df.personID = kp.personID_A
)
SELECT p.personID, p.firstName, p.lastName, df.distance
FROM DirectFriends df
JOIN person p ON df.personID = p.personID;


-- 12) Extend the query for Task 11 by also outputting the minimum path between the users in addition to the distance.

WITH RECURSIVE DirectFriends AS (
  SELECT personID_B AS personID, 1 AS distance, ARRAY[personID_B] AS path
  FROM person_knows_Person
  WHERE personID_A = 94
  UNION ALL
  SELECT kp.personID_B, df.distance + 1, df.path || kp.personID_B
  FROM DirectFriends df
  JOIN person_knows_Person kp ON df.personID = kp.personID_A
)
SELECT p.personID, p.firstName, p.lastName, df.distance, df.path
FROM DirectFriends df
JOIN person p ON df.personID = p.personID;

/*
Output

    personid    |    firstname     |  lastname  | distance |                                                    path                                                    ----------------+------------------+------------+----------+------------------------------------------------------------------------------------------------------------  8796093022217 | Alim             | Guliyev    |        1 | {8796093022217}
  3298534883365 | Wei              | Wei        |        1 | {3298534883365}
  8796093022251 | Chen             | Li         |        1 | {8796093022251}
  2199023255625 | Cheng            | Chen       |        1 | {2199023255625}
 10995116277851 | Chong            | Liu        |        1 | {10995116277851}
             96 | Anson            | Chen       |        1 | {96}
  9895604649984 | Yang             | Li         |        2 | {2199023255625,9895604649984}
  8796093022217 | Alim             | Guliyev    |        2 | {2199023255625,8796093022217}
 15393162788888 | Jie              | Yang       |        2 | {2199023255625,15393162788888}
  9895604650020 | Yang             | Liu        |        2 | {2199023255625,9895604650020}
*/


--PART 2(C): Changes in the Generated Database

/*
A mechanism should be implemented to document the termination of an employment relationship. 
The corresponding entry in `person_workAt_company` should be deleted using an SQL statement. 
To be able to trace the data manipulation, the deletion process should be logged in a separate table. 
Additionally, it should be noted when the employment relationship was terminated (based on the deletion
timestamp). 
The logging should be done automatically when an employee ends their
employment at a company (deletion in `person_workAt_company`). 
Formulate a delete statement that shows that your mechanism works.

*/

DROP TABLE IF EXISTS Former_employees_table;
CREATE TABLE Former_employees_table (
	employeeID BIGINT ,
	companyID INT,
	firstname VARCHAR(55),
	lastname VARCHAR(55),
	expirationOfContract DATE,
	PRIMARY KEY (employeeID,companyID)
);

CREATE OR REPLACE FUNCTION insert_log_entry()
RETURNS trigger AS $$
BEGIN
INSERT INTO Former_employees_table(employeeID,companyID,expirationOfContract,firstname,lastname)
SELECT workAT.personID,companyID,now(),person.firstname,person.lastname FROM workAT  JOIN 
person on OLD.personID=person.personID
WHERE workAT.companyID=OLD.companyID;
RETURN NEW;
END;
$$ LANGUAGE 'plpgsql';

DROP TRIGGER IF EXISTS Former_employee ON workAt;

CREATE TRIGGER Former_employee
AFTER DELETE ON workAt
FOR EACH ROW
EXECUTE PROCEDURE insert_log_entry();
END;

SELECT * FROM workAt; 
DELETE FROM workAt 
WHERE workAt.personid=12094627905604 AND workAt.companyid=897 ;
SELECT * FROM Former_employees_table;