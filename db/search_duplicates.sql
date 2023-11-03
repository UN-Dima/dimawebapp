SELECT
    hermes_cod, COUNT(*)
FROM
    projects_project
GROUP BY
    hermes_cod
HAVING 
    COUNT(*) > 1