-- Verifica quantos dias de negociação existem por ano.
-- Útil para verificar consistência e qualidade do dataset.
SELECT 
    strftime('%Y', date) AS ano,
    COUNT(*) AS total_dias_negociados
FROM uber_stocks
GROUP BY ano
ORDER BY ano;
