-- Cria um índice na coluna `Date` para acelerar buscas temporais, comuns em séries temporais.
CREATE INDEX idx_data ON uber_stocks(Date);
