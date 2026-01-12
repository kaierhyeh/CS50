-- Starring Chadwick Boseman and ordered by rating:
-- 	Need to JOIN movies, stars and ratings.
SELECT DISTINCT title FROM movies JOIN stars ON movies.id = stars.movie_id
JOIN ratings ON movies.id = ratings.movie_id
WHERE stars.person_id = (SELECT id FROM people WHERE name = 'Chadwick Boseman')
ORDER BY ratings.rating DESC LIMIT 5;
-- Need DISTINCT cuz the person_id starred twice in some movies.
-- 	Check with:
-- 	```
-- 	SELECT movie_id, person_id, COUNT() FROM stars GROUP BY movie_id, person_id HAVING COUNT() > 1 LIMIT 5;
-- 	```

-- Check if a movie appears twice in ratings:
-- 	```
-- 	SELECT movie_id, COUNT(*) FROM ratings GROUP BY movie_id HAVING COUNT(*) > 1;
-- 	```

-- Alternative, very slow:
-- SELECT DISTINCT title, rating FROM movies JOIN stars ON movies.id = stars.movie_id
-- JOIN people ON stars.person_id = people.id
-- JOIN ratings ON movies.id = ratings.movie_id
-- WHERE people.name = 'Chadwick Boseman' ORDER BY ratings.rating DESC LIMIT 5;


-- Using a subquery in the ORDER BY that references another table (ratings) and tries to look up the rating for each movie_id.
-- While that can sometimes work, it’s messy and slow — and in SQLite it often behaves unpredictably or inefficiently.

-- The better way is to join the tables instead of using a nested SELECT in ORDER BY.
-- The following won't work:
-- SELECT title FROM movies WHERE id AS movie_id IN
-- (SELECT movie_id FROM stars WHERE person_id =
-- (SELECT id FROM people WHERE name = 'Chadwick Boseman')) ORDER BY
-- (SELECT rating FROM ratings WHERE movie_id = movies.movie_id) DESC;
