DROP TABLE IF EXISTS Stars;
CREATE TABLE Stars (
  id     INTEGER,
  dist   NUMERIC,
  x      NUMERIC,
  y      NUMERIC,
  z      NUMERIC,
  ra     NUMERIC,
  dec    NUMERIC,
  mag    NUMERIC,
  con    varchar(5),
  lum    NUMERIC,
  proper VARCHAR(50),
  bf     VARCHAR(50),
  ci     VARCHAR(10)
);

\copy Stars from stars_trim_bf_ci.csv csv
