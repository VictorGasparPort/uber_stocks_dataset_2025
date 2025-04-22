-- Consulta direta da média total do preço de abertura em todo o período.
SELECT ROUND(AVG(open), 2) AS media_abertura_geral
FROM uber_stocks;
