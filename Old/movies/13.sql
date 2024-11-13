SELECT name FROM people WHERE id IN(
    SELECT person_id FROM stars WHERE movie_id IN(
        SELECT id FROM movies
        JOIN stars ON id = movie_id
        WHERE person_id = (
            SELECT id FROM people WHERE name = 'Kevin Bacon' AND birth = 1958)
    )
) AND name != 'Kevin Bacon';
