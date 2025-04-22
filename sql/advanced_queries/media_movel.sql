-- Gera uma média móvel de 7 dias para o preço de fechamento.
-- Essencial para análise de tendência com suavização.
SELECT 
    date,
    close,
    AVG(close) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS media_movel_7dias
FROM uber_stocks;
