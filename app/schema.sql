-- Entfernen bestehender Tabellen, falls vorhanden
DROP TABLE IF EXISTS BenutzerMaschinen;
DROP TABLE IF EXISTS Maschinen;
DROP TABLE IF EXISTS user;  -- Hier wurde 'user' anstelle von 'Benutzer' verwendet

-- Erstellung der Tabelle 'user'
CREATE TABLE user (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,  -- Hier wird der Hash-Wert des Passworts gespeichert
  email VARCHAR(255)
);

-- Erstellung der Tabelle 'Maschinen'
CREATE TABLE Maschinen (
  Maschinen_ID SERIAL PRIMARY KEY,
  Maschinenname VARCHAR(255) NOT NULL,
  Maschinentyp VARCHAR(255) NOT NULL
  -- Hier kommen die weiteren Daten hin, die abgespeichert werden sollen
);

-- Erstellung der Tabelle 'BenutzerMaschinen'
CREATE TABLE BenutzerMaschinen (
  Verknuepfungs_ID SERIAL PRIMARY KEY,
  Benutzer_ID INT,
  Maschinen_ID INT,
  FOREIGN KEY (Benutzer_ID) REFERENCES user(id),
  FOREIGN KEY (Maschinen_ID) REFERENCES Maschinen(Maschinen_ID)
);
