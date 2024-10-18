SELECT title
FROM movies
WHERE id IN (
    SELECT movie_id
    FROM stars
    JOIN people AS p1 ON stars.person_id = p1.id
    WHERE p1.name = 'Bradley Cooper'
)
AND id IN (
    SELECT movie_id
    FROM stars
    JOIN people AS p2 ON stars.person_id = p2.id
    WHERE p2.name = 'Jennifer Lawrence'
);
