# Treenipäiväkirja

Treenipäiväkirja-sovelluksessa käyttäjä voi kirjata tekemiään harjoituksia. Treenipäiväkirja tukee neljää lajia - juoksua, pyöräilyä, painonnostoa ja voimanostoa.

Kuhunkin harjoitukseen kirjataan kesto ja harjoituksen sisältämät harjoitteet. Kunkin harjoitteen voi kategorisoida tarkoituksensa mukaan. Harjoite- ja tarkoitusuniversumi vaihtelee lajista riippuen.

## Sovelluksen toiminnot

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään ja muokkaamaan urheiluun liittyviä käyttäjätietoja itsestään.
- Käyttäjä pystyy lisäämään suoritettuja harjoituksia. Tuettuja lajeja ovat painonnosto, voimanosto, juoksu ja pyöräily. Harjoitusten ja/tai liikkeiden kategorisointi näiden lajien sisällä on mahdollista. 
- Käyttäjä näkee muiden suoritetut harjoitukset.
- Käyttäjä voi hakea muiden suoritettuja harjoituksia lajilla tai harjoitteella.
- Käyttäjäsivulla on tilastointia, joka näyttää tilastoja käyttäjän suorittamista harjoituksista.
- Käyttäjä voi kommentoida toisten tekemiä harjoituksia.



## Näin saat käyntiin

- Asenna flask-kirjasto "pip install flask"
- Luo tietokannan tiedot ja lisää alkutiedot "sqlite3 database.db < schema.sql && sqlite3 database.db < init.sql"
- Käynnistä sovellus ajamalla "flask run"
- Kirjoita selaimeesi "Running on '...' " -ilmoituksen mukainen osoite.
