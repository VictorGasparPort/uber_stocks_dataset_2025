-- Criação de uma tabela auxiliar que armazena a média mensal dos preços de fechamento.
-- Isso é útil para análises de tendência ao longo do tempo em nível de mês, suavizando variações diárias.
CREATE TABLE media_mensal_fechamento AS
SELECT
    strftime('%Y-%m', Date) AS ano_mes,
    AVG(Close) AS media_fechamento
FROM uber_stocks
GROUP BY ano_mes
ORDER BY ano_mes;
