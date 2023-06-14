SELECT
    hermes_code, COUNT(*)
FROM
    projects_project
GROUP BY
    hermes_code
HAVING 
    COUNT(*) > 1