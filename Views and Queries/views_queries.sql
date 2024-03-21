SET search_path TO social_network_db;


/*
PART 2(a): VIEW CREATION

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

--PART 2(b): Queries on the database

--1) In how many different European cities are there universities?

SELECT COUNT(uni.uniid)
FROM university as uni 
JOIN city on uni.cityid=city.cityID
JOIN country on city.ispartof=country.countryID
JOIN continent on country.ispartof = continent.continentid
JOIN place on place.placeid = continent.continentid
WHERE place."name"='Europe';


/*


2) How many forum posts has the youngest person authored
(Output: Name, #Forum Posts)?
3) How many comments on posts are there from each country
(Output sorted ascending by comment count)? The list should also include countries
for which no post comments exist, i.e., the comment count = 0! (Coalesce function)
4) From which cities do most users come
(Output Name + Population)?
5) Who is 'Hans Johansson' friends with?
6) Who are the "real" friends-of-a-friend of 'Hans Johansson'?
"Echte" Freundesfreunde dürfen nicht gleichzeitig direkte Freunde von 'Hans
Johansson' sein. Sortieren Sie die Ausgabe alphabetisch nach dem Nachnamen.
7) Which users are members in all forums where 'Mehmet Koksal' is also a member
(Output Name)?
8) Provide the percentage distribution of users by their origin from different
continents.
9) Which forums contain more posts than the average number of posts in forums
(Output sorted alphabetically by forum title)?
10) Which persons are friends with the person who received the most likes on a
post?
Sort the output alphabetically by last name.
11) Which persons are directly or indirectly connected to 'Jun Hu' (id 94)
(friends)? Provide for each person the minimum distance to Jun.
12) Extend the query for Task 11 by also outputting the minimum path between the
users
in addition to the distance.
Note: The cardinality of the result set is larger, as there can be multiple minimal paths
between two persons.
*/