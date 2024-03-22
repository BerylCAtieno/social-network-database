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

SELECT COUNT(uni.universityID)
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

-- Output: 1335


-- 2) How many forum posts has the youngest person authored

SELECT person.firstname, person.lastname, post.postid 
FROM post  
JOIN "message" ON post.postid = "message".messageid
JOIN person ON "message".creator = person.personid
WHERE person.birthday = (SELECT MAX(person.birthday)FROM person );

/*
Output

 firstname | lastname |    postid
-----------+----------+--------------
 Paul      | Becker   | 120259086700
 Paul      | Becker   |  94489288193
 Paul      | Becker   | 137438961155
 Paul      | Becker   | 111669157380
 Paul      | Becker   | 128849026587
*/

-- 3) How many comments on posts are there from each country

SELECT  place.name , COUNT(COALESCE(post.postid,0)) as comment_count 
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

SELECT place."name", sum(person.cityid) AS "Population" from person
JOIN city ON city.cityid = person.cityid
JOIN place ON place.placeid = city.cityid
GROUP BY place."name"
order by "Population" DESC
LIMIT 1;

/*
Output
   name      | Population
----------------+---------------
 Rahim_Yar_Khan |          1588
*/

-- 5) Who is 'Hans Johansson' friends with?

SELECT person.personid, person.firstname,person.lastname FROM person
WHERE person.personid IN (
    SELECT person_knows_person.personID_B FROM person 
    JOIN person_knows_person ON person_knows_person.personID_A = person.personid
    WHERE person.lastname = 'Johansson' And person.firstname = 'Hans');

/*
Output

    personid    |    firstname     |  lastname
----------------+------------------+------------
  7696581394474 | Ali              | Achiou
  5497558138940 | Paul             | Becker
 12094627905628 | Abdoulaye Khouma | Dia
 12094627905567 | Otto             | Richter
  8796093022217 | Alim             | Guliyev
  9895604650000 | Jan              | Zakrzewski
 12094627905563 | Wojciech         | Ciesla
 12094627905550 | Hossein          | Forouhar
 10995116277764 | Bryn             | Davies
(9 rows)
*/

-- 6) Who are the "real" friends-of-a-friend of 'Hans Johansson'?

SELECT  DISTINCT person.personid,person.firstname,person.lastname 
FROM person 
WHERE person.personid IN (
    SELECT person_knows_person.personID_B FROM person
    JOIN person_knows_person ON person_knows_person.personID_A = person.personid
        WHERE person.personid in (
            SELECT person_knows_person.personID_B  FROM person 
            JOIN person_knows_person ON person_knows_person.personID_A = person.personid
            WHERE person.lastname = 'Johansson' And person.firstname = 'Hans'
        )
) 
AND person.personid not in (
	SELECT person_knows_person.personID_B  FROM person 
	JOIN person_knows_person ON person_knows_person.personID_A = person.personid
	WHERE person.lastname = 'Johansson' And person.firstname = 'Hans'
) ORDER BY person.lastname;

/*
Output

    personid    |  firstname  |  lastname
----------------+-------------+------------
  8796093022253 | Ali         | Abouba
 10995116277811 | Oleg        | Bazayev
  7696581394490 | Amy         | Chen
 16492674416674 | Roberto     | Diaz
  6597069766688 | Miguel      | Gonzalez
 16492674416738 | Wei         | Hu
 12094627905580 | Alexei      | Kahnovich
 13194139533342 | Joakim      | Larsson
  8796093022251 | Chen        | Li
 10995116277826 | Jie         | Li
 10995116277851 | Chong       | Liu
  9895604650074 | Cam         | Loan
  9895604650002 | Neil        | Murray
 13194139533352 | Celso       | Oliveira
 14293651161168 | Abdul Jamil | Qureshi
 15393162788920 | Otto        | Redl
 17592186044483 | Francisco   | Reyes
 15393162788948 | Anatoly     | Shevchenko
  9895604650036 | Akira       | Yamamoto
 15393162788888 | Jie         | Yang
 14293651161162 | Li          | Zhang
 16492674416689 | Lin         | Zhang
(22 rows)
*/

-- 7) Which users are members in all forums where 'Mehmet Koksal' is also a member?

DROP TABLE IF EXISTS forumIdtemp;
CREATE TABLE forumIdtemp (
	id serial PRIMARY KEY,
	forumID BIGINT 
);

INSERT INTO forumIdtemp(forumID) (
	SELECT forum_hasmember.forumid 
	FROM forum_hasmember
	WHERE forum_hasmember.personid =(
		SELECT person.personid FROM person WHERE person.firstname='Mehmet' AND person.lastname='Koksal'
	)
);

SELECT person.firstname,person.lastname
FROM person 
JOIN forum_hasmember ON forum_hasmember.personid = person.personid
WHERE forum_hasmember.forumid=(
    SELECT forumIdtemp.forumID 
    FROM forumIdtemp 
    WHERE forumIdtemp.id=1)
INTERSECT
SELECT person.firstname,person.lastname
FROM person JOIN forum_hasmember ON forum_hasmember.personid = person.personid
WHERE forum_hasmember.forumid=(
    SELECT forumIdtemp.forumID 
    FROM forumIdtemp 
    WHERE forumIdtemp.id=2)
 INTERSECT
 SELECT person.firstname,person.lastname
 FROM person JOIN forum_hasmember on forum_hasmember.personid = person.personid
 WHERE forum_hasmember.forumid=(
    SELECT forumIdtemp.forumID 
    FROM forumIdtemp 
    WHERE forumIdtemp.id=3);

/*
Output

 firstname | lastname
-----------+----------
 Mehmet    | Koksal
 Miguel    | Gonzalez
 Chen      | Yang
 Paul      | Becker
(4 rows)
*/

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

/*
Output

     name      | percentage
---------------+--------
 North_America |      9
 South_America |      4
 Africa        |     11
 Asia          |     50
 Europe        |     25
(5 rows)
*/

-- 9) Which forums contain more posts than the average number of posts in forums

SELECT forum.title, COUNT(post.postid) AS post_count
FROM forum 
JOIN post ON forum.forumid=post.forumid
GROUP BY forum.title
HAVING COUNT(post.postid) > (
	(SELECT COUNT(post.postid)FROM post )/(SELECT COUNT (forum.forumid) FROM forum)
) ORDER BY forum.title ;

/*
Output

                 title                   | post_count
------------------------------------------+--------
 Album 0 of Abdul Haris Tobing            |     17
 Album 0 of Alejandro Rodriguez           |     20
 Album 0 of Ali Abouba                    |     13
 Album 0 of Amy Chen                      |     19
 Album 0 of Celso Oliveira                |     20
 Album 0 of Djelaludin Zaland             |     15
 Album 0 of Eric Mettacara                |     13
 Album 0 of Fritz Engel                   |     13
 Album 0 of Hao Li                        |     16
 Album 0 of Jie Li                        |     11
*/

-- 10) Which persons are friends with the person who received the most likes on a post?
--     Sort the output alphabetically by last name.

SELECT  person.firstname, person.lastname 
FROM person
WHERE person.personid in (
	SELECT person_knows_person.personID_B FROM person
	JOIN person_knows_person ON person_knows_person.personID_A = person.personid
	WHERE person.personid =(
		SELECT creator FROM "message" Where "message".messageid=(
			SELECT messageid FROM(
				SELECT messageid, Count(person_likes_message.personid) AS likes  FROM person_likes_message
				join post on person_likes_message.messageid=post.postid 
				GROUP BY messageid
				ORDER BY likes DESC LIMIT 1
			) AS variabel
		)
	)
)
ORDER BY person.lastname;

/*
Output

 firstname | lastname
-----------+-----------
 Ali       | Abouba
 Bryn      | Davies
 Hossein   | Forouhar
 Wei       | Hu
 Alexei    | Kahnovich
 Joakim    | Larsson
 Jie       | Li
 Akira     | Yamamoto
 Li        | Zhang
 Lin       | Zhang
(10 rows)
*/

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

/*
Output

   personid    |    firstname     |  lastname  | distance
----------------+------------------+------------+----------
  8796093022217 | Alim             | Guliyev    |        1
  3298534883365 | Wei              | Wei        |        1
  8796093022251 | Chen             | Li         |        1
  2199023255625 | Cheng            | Chen       |        1
 10995116277851 | Chong            | Liu        |        1
             96 | Anson            | Chen       |        1
  9895604649984 | Yang             | Li         |        2
  8796093022217 | Alim             | Guliyev    |        2
 15393162788888 | Jie              | Yang       |        2
  9895604650020 | Yang             | Liu        |        2
 16492674416689 | Lin              | Zhang      |        2
*/

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