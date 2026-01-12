SELECT title, rating FROM movies JOIN ratings ON movies.id = ratings.movie_id WHERE year = 2010 ORDER BY rating DESC, title;
-- JOIN defaults to INNER JOIN, which keeps only rows that exist in both tables, excluding any movie that doesn’t have a rating.
