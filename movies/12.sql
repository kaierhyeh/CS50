SELECT title FROM movies WHERE id IN
(SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Bradley Cooper')
INTERSECT SELECT movie_id FROM stars WHERE person_id = (SELECT id FROM people WHERE name = 'Jennifer Lawrence'));
-- (( ... ) INTERSECT (... )) causes a syntax error because:
-- 	SQLite expects the INTERSECT operator to appear directly between
-- 	two SELECT statements, not inside extra parentheses.


-- Slower alternative:
-- SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id
-- JOIN people ON stars.person_id = people.id
-- WHERE people.name IN ('Bradley Cooper', 'Jennifer Lawrence')
-- GROUP BY title HAVING COUNT(DISTINCT people.name) = 2;
