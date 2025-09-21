# Treenipäiväkirja

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään ja muokkaamaan urheiluun liittyviä käyttäjätietoja itsestään.
- Käyttäjä pystyy lisäämään suoritettuja harjoituksia. Tuettuja lajeja ovat painonnosto, voimanosto, juoksu ja pyöräily. Harjoitusten ja/tai liikkeiden kategorisointi näiden lajien sisällä on mahdollista.
- Käyttäjä näkee muiden suoritetut harjoitukset.
- Käyttäjä voi hakea muiden suoritettuja harjoituksia kategorialla tai hakusanalla.
- Sovelluksessa on tilastosivut, jotka näyttävät tilastoja käyttäjän suorittamista harjoituksista.
- Käyttäjä voi kommentoida toisten tekemiä harjoituksia.



## Näin saat käyntiin

- Asenna flask-kirjasto "pip install flask"
- Luo tietokannan tiedot ja lisää alkutiedot "sqlite3 database.db < schema.sql && sqlite3 database.db < init.sql"
-Käynnistä sovellus ajamalla "flask run"
