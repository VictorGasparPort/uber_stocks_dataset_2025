-- Traz os dias onde o volume negociado foi maior que 150% da média anual daquele ano.
-- Ajuda a detectar dias de anomalias ou grandes movimentações.
SELECT 
    u.date,
    u.volume,
    v.volume_medio,
    ROUND((u.volume * 1.0 / v.volume_medio), 2) AS proporcao_volume
FROM uber_stocks u
JOIN volume_medio_anual v
  ON strftime('%Y', u.date) = v.ano
WHERE u.volume > 1.5 * v.volume_medio
ORDER BY proporcao_volume DESC;
