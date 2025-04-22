-- Criação de tabela auxiliar com a variação diária percentual entre o preço de abertura e fechamento.
-- Isso ajuda a entender a volatilidade diária das ações.
CREATE TABLE variacao_diaria_preco AS
SELECT
    Date,
    Open,
    Close,
    ROUND(((Close - Open) / Open) * 100, 2) AS variacao_percentual
FROM uber_stocks;
