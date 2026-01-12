SELECT DISTINCT name FROM people WHERE id IN
(SELECT person_id FROM stars WHERE movie_id IN
(SELECT movie_id FROM stars WHERE person_id =
(SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958)))
AND name != 'Kevin Bacon' ORDER BY name;

-- SELECT COUNT(DISTINCT name) FROM people WHERE id IN (SELECT person_id FROM stars WHERE movie_id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958))) AND name != 'Kevin Bacon' ORDER BY name;

-- Slightly slower alternative:
-- SELECT DISTINCT name FROM people JOIN stars ON people.id = stars.person_id
-- WHERE stars.movie_id IN
-- (SELECT movie_id FROM stars WHERE person_id =
-- (SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958))
-- AND name != 'Kevin Bacon' ORDER BY name;

-- SELECT COUNT(DISTINCT name) FROM people JOIN stars ON people.id = stars.person_id WHERE stars.movie_id IN (SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958)) AND name != 'Kevin Bacon' ORDER BY name;
