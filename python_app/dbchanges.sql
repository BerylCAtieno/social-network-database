
UPDATE place
SET type = CASE
    WHEN placeid IN (SELECT cityid FROM city) THEN 'city'
    WHEN placeid IN (SELECT countryid FROM country) THEN 'country'
    WHEN placeid IN (SELECT continentid FROM country) THEN 'continent'
    ELSE NULL 
END;

UPDATE organisation
SET type = CASE 
    WHEN organisationid IN (SELECT universityid FROM university) THEN  'university'
    WHEN organisationid IN (SELECT companyid FROM company) THEN  'company'
    ELSE NULL 
END;

