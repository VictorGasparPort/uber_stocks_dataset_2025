-- Retorna o preço de fechamento no último dia disponível de cada ano.
-- Usado para verificar evolução ano a ano.
SELECT 
    strftime('%Y', date) AS ano,
    MAX(date) AS ultima_data,
    (SELECT close FROM uber_stocks us2 WHERE us2.date = MAX(us1.date)) AS fechamento
FROM uber_stocks us1
GROUP BY ano;
