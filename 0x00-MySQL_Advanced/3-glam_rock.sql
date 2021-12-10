-- select bands with Glam Rock as their style, ranked by longevity
SELECT band_name, IFNULL(split, 2021) - formed AS lifespan
FROM metal_bands
WHERE LOCATE('Glam rock', style)
ORDER BY lifespan DESC;
