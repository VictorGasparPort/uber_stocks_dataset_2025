-- Padroniza os nomes das colunas para facilitar queries e manter consistência em projetos com outros datasets.
ALTER TABLE uber_stocks RENAME COLUMN "Adj Close" TO adj_close;
ALTER TABLE uber_stocks RENAME COLUMN "Close" TO close;
ALTER TABLE uber_stocks RENAME COLUMN "Open" TO open;
ALTER TABLE uber_stocks RENAME COLUMN "High" TO high;
ALTER TABLE uber_stocks RENAME COLUMN "Low" TO low;
ALTER TABLE uber_stocks RENAME COLUMN "Volume" TO volume;
ALTER TABLE uber_stocks RENAME COLUMN "Date" TO date;
