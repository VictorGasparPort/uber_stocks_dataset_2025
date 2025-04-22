-- Consulta que retorna os 5 dias com maior diferença entre high e low, indicando maior volatilidade.
SELECT 
    date,
    high,
    low,
    ROUND(high - low, 2) AS variacao_absoluta
FROM uber_stocks
ORDER BY variacao_absoluta DESC
LIMIT 5;
