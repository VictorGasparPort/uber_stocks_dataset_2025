-- Criação de uma tabela auxiliar com o volume médio de ações negociadas por ano.
-- Útil para entender padrões de interesse do mercado ao longo dos anos.
CREATE TABLE volume_medio_anual AS
SELECT
    strftime('%Y', Date) AS ano,
    ROUND(AVG(Volume)) AS volume_medio
FROM uber_stocks
GROUP BY ano
ORDER BY ano;
