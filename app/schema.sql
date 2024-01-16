-- Entfernen bestehender Tabellen, falls vorhanden
DROP TABLE IF EXISTS BenutzerMaschinen;
DROP TABLE IF EXISTS Maschinendaten;
DROP TABLE IF EXISTS Maschinen;
DROP TABLE IF EXISTS users;  -- Hier wurde 'user' anstelle von 'Benutzer' verwendet


-- Erstellung der Tabelle 'user'
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,  -- Hier wird der Hash-Wert des Passworts gespeichert
  email VARCHAR(255)
);

-- Erstellung der Tabelle 'Maschinen'
CREATE TABLE Maschinen (
  Maschinen_ID INTEGER PRIMARY KEY,        --Eventuell noch gegen echten Key (KommissionsNr etc.) austauschen
  Maschinenname VARCHAR(255) NOT NULL,
  Maschinentyp VARCHAR(255) NOT NULL
);

--Erstellung der Tabelle 'Maschinendaten' (Hier werden die Daten der Maschine Abhängig der ID gespeichert)
CREATE TABLE Maschinendaten (
  MaschineData_ID SERIAL PRIMARY KEY
  Maschinen_ID INTEGER,
  Daten JSON
);

-- Erstellung der Tabelle 'BenutzerMaschinen'
CREATE TABLE BenutzerMaschinen (
  Verknuepfungs_ID SERIAL PRIMARY KEY,
  Benutzer_ID INT,
  Maschinen_ID INT,
  FOREIGN KEY (Benutzer_ID) REFERENCES users(id),
  FOREIGN KEY (Maschinen_ID) REFERENCES Maschinen(Maschinen_ID)
);
