-- Simula particionamento lógico dos dados por ano, para facilitar consultas específicas por período.
-- É feito por uma VIEW, mas em bancos com suporte, pode ser uma partição real.
CREATE VIEW uber_2023_dados AS
SELECT * FROM uber_stocks
WHERE strftime('%Y', date) = '2023';
