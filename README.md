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





## Tietokannan toiminta suurella tietomäärällä

Testiä varten luodaan ```seed.py``` avulla tietokanta, jossa on seuraavat parametrit:
```
user_count = 10000
workout_count = 10**6
comment_count = 10**7
```
Koodi luo tietokannan, jossa on 10000 käyttäjää, 1 000 000 harjoitusta ja 10 000 000 kommenttia. 

Testit tehdään ensin skeemalla jota ei ole indeksoitu ja sitten skeemalla, joka on indeksoitu. 

Latausnopeuksia mitataan seuraavanlaisesti:

1. luodaan tunnus
2. kirjaudutaan sisään
3. Lisätään uusi harjoitus
4. mennään sivun 5 keskimmäiseen harjoitukseen. - workout740582
5. Kommentoidaan sivun 5 keskimmäistä harjoitusta
6. Käydään kommenttisivulla 2
7. Palataan kommenttisivulle 1
6. mennään sivun 5 keskimmäisen harjoituksen käyttäjään
7. Poistetaan aiemmin itse tehty harjoitus
8. haetaan hausta hakusanalla ```deadlift```.

Erityisesti selailuun liittyviä tuloksia vääristää hieman se, että "LIMIT" -lausekkeet olivat testatessa jo paikoillaan funktioissa.

### Ilman indeksejä

Koska datantestausharjoitus oli tiedossa, ei tietokantaa ole testejä tehdessä vielä indeksoitu. Tallennetaan tästä kopio nimellä ```schema_no_indexes.sql``` ja lisätään se gitignoreen.

```python3 seed.py``` luodaan testitietokanta

Tarkastetaan tietokannan koko:
```
❯ ls -lh database.db
-rw-r--r--@ 1 heikkinenmattis  staff   644M Dec 14 19:54 database.db
```

Testit:
```
❯ flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 2.22 s
127.0.0.1 - - [14/Dec/2025 20:00:23] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:23] "GET /static/style.css HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:27] "GET /register.html HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:27] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.33 s
127.0.0.1 - - [14/Dec/2025 20:00:37] "POST /create HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.33 s
127.0.0.1 - - [14/Dec/2025 20:00:44] "POST /login HTTP/1.1" 302 -
elapsed time: 2.21 s
127.0.0.1 - - [14/Dec/2025 20:00:46] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:46] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [14/Dec/2025 20:00:55] "GET /workouts.html HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:55] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:00:59] "POST /confirm_sport HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:00:59] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:01:02] "POST /add_workout HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:02] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [14/Dec/2025 20:01:24] "POST /add_workout HTTP/1.1" 302 -
elapsed time: 2.26 s
127.0.0.1 - - [14/Dec/2025 20:01:26] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:26] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 2.25 s
127.0.0.1 - - [14/Dec/2025 20:01:40] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:40] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 2.24 s
127.0.0.1 - - [14/Dec/2025 20:01:45] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:45] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 2.25 s
127.0.0.1 - - [14/Dec/2025 20:01:49] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:49] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 2.24 s
127.0.0.1 - - [14/Dec/2025 20:01:52] "GET /5 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:01:52] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.09 s
127.0.0.1 - - [14/Dec/2025 20:02:03] "GET /workouts/workout740582 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:02:03] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.09 s
127.0.0.1 - - [14/Dec/2025 20:02:12] "POST /add_comment HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:02:12] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.08 s
127.0.0.1 - - [14/Dec/2025 20:03:03] "GET /workouts/workout740582/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:03:03] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.08 s
127.0.0.1 - - [14/Dec/2025 20:03:07] "GET /workouts/workout740582/1 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:03:07] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.22 s
127.0.0.1 - - [14/Dec/2025 20:03:46] "GET /user/270 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:03:46] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 2.25 s
127.0.0.1 - - [14/Dec/2025 20:04:32] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:04:32] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.01 s
127.0.0.1 - - [14/Dec/2025 20:04:37] "GET /workouts/5b100f24-f703-4a13-a298-49b10766d814 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:04:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.08 s
127.0.0.1 - - [14/Dec/2025 20:04:38] "POST /delete_workout HTTP/1.1" 302 -
elapsed time: 2.21 s
127.0.0.1 - - [14/Dec/2025 20:04:40] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:04:41] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:04:45] "GET /find_workout HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:04:45] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.49 s
127.0.0.1 - - [14/Dec/2025 20:04:49] "GET /find_workout?query=deadlift&csrf_token=ecc679fc3885a4fbcbc35e144cd09864 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:04:49] "GET /static/style.css HTTP/1.1" 304 -
```

### Indeksien kanssa

Tässä vaiheessa edellinen tietokanta epähuomiossa poistettiin ja luotiin uusi testitietokanta, koska on jäänyt lihasmuistiin luoda kanta uusiksi aina, kun sinne muuttaa jotain.

Luodaan indeksit.

```
CREATE INDEX idx_workout_id ON workouts(workout_id);
CREATE INDEX idx_workout_user ON workouts(user_id);
CREATE INDEX idx_workout_user ON workouts(begin_time);
CREATE INDEX idx_users_id ON users(id);
CREATE INDEX idx_comments_workout ON comments(workout_id);
CREATE INDEX idx_comments_user ON comments(user_id);

```

```sqlite3 database.db < schema.sql```

```python3 seed.py```luodaan testitietokanta


Tarkastetaan tietokannan koko:
```
-rw-r--r--@ 1 heikkinenmattis  staff   1.0G Dec 14 20:31 database.db
```

Testit:
```
❯ flask run
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
elapsed time: 1.9 s
127.0.0.1 - - [14/Dec/2025 20:52:20] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:20] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:52:21] "GET /register.html HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:21] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.34 s
127.0.0.1 - - [14/Dec/2025 20:52:35] "POST /create HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:35] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.32 s
127.0.0.1 - - [14/Dec/2025 20:52:42] "POST /login HTTP/1.1" 302 -
elapsed time: 1.87 s
127.0.0.1 - - [14/Dec/2025 20:52:44] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:44] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [14/Dec/2025 20:52:51] "GET /workouts.html HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:51] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:52:54] "POST /confirm_sport HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:54] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:52:56] "POST /add_workout HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:52:56] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.02 s
127.0.0.1 - - [14/Dec/2025 20:53:19] "POST /add_workout HTTP/1.1" 302 -
elapsed time: 1.89 s
127.0.0.1 - - [14/Dec/2025 20:53:21] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:21] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.9 s
127.0.0.1 - - [14/Dec/2025 20:53:33] "GET /2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:33] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.9 s
127.0.0.1 - - [14/Dec/2025 20:53:37] "GET /3 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.89 s
127.0.0.1 - - [14/Dec/2025 20:53:40] "GET /4 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:40] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.91 s
127.0.0.1 - - [14/Dec/2025 20:53:45] "GET /5 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:45] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [14/Dec/2025 20:53:58] "GET /workouts/workout834531 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:53:58] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:07] "POST /add_comment HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:07] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:09] "GET /workouts/workout834531/2 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:09] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:11] "GET /workouts/workout834531/1 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:11] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.03 s
127.0.0.1 - - [14/Dec/2025 20:54:22] "GET /user/6605 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:22] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 1.9 s
127.0.0.1 - - [14/Dec/2025 20:54:33] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:33] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:37] "GET /workouts/378e8db0-11f8-4971-b8bd-eaecd2a0fc50 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:37] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:43] "POST /delete_workout HTTP/1.1" 302 -
elapsed time: 1.89 s
127.0.0.1 - - [14/Dec/2025 20:54:45] "GET / HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:45] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.01 s
127.0.0.1 - - [14/Dec/2025 20:54:47] "GET /find_workout HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:47] "GET /static/style.css HTTP/1.1" 304 -
elapsed time: 0.53 s
127.0.0.1 - - [14/Dec/2025 20:54:52] "GET /find_workout?query=deadlift&csrf_token=2e4dd5dd171723bff4d6a2d762020c43 HTTP/1.1" 200 -
elapsed time: 0.0 s
127.0.0.1 - - [14/Dec/2025 20:54:52] "GET /static/style.css HTTP/1.1" 304 -
^C%      

```
## Johtopäätökset

Indeksien kanssa tietokanta on n. 50% suurempi. Osassa toiminnoista on havaittavissa selkeää nopeutumista, mutta esimerkiksi etusivu on edelleen käyttömukavuusnäkökulmasta hieman hidas. 

Merkittävimmät parannukset esiintyvät käyttäjäsivuilla ja kommenttisivulla.
- Käyttäjäsivu ilman indeksejä: ```0.22s```
- Käyttäjäsivu indeksien kanssa: ```0.03s```
- Kommenttisivu ilman indeksejä: ```1.08s```
- Kommenttisivu indeksien kanssa: ```0.01s```


Käyttäjäsivun parannukseen on kaksi syytä. Toinen on käyttäjätaulun indeksointi ```idx_users_id``` ja toinen on harjoitustaulun käyttäjätiedon indeksointi ```idx_workout_user```. Ilman näitä ohjelma joutuisi skannaamaan jokaisen käyttäjän läpi, tai käyttäjätaulun tapauksessa jokaisen suorituksen.

Myös kommenttisivuilla on indeksoitu todennäköisimmät liittävät kentät, eli käyttäjätunnus ja harjoitustunnus.

Performanssin heikkous etusivua ladattaessa johtuu mitä todennäköisimmin tiedon järjestämisestä. Järjestysperusteena on aikaleima ja indeksi on luotu suoraan tekstiin. Tämä aiheuttaa sen, että merkittävää parannusta järjestämisestä ei tule.


  
## Tulosten yhteenveto
| Toiminto | Ilman indeksejä (s) | Indeksien kanssa (s) |
|----------|---------------------|----------------------|
| Etusivu (/) | 2.26 | 1.90 |
| Tunnuksen luonti | 0.33 | 0.34 |
| Kirjautuminen | 0.32 | 0.32 |
| Uuden harjoituksen luonti | 0.01 | 0.01 |
| GET /2 | 2.25 | 1.90 |
| GET /3 | 2.25 | 1.90 |
| GET /4 | 2.28 | 1.89 |
| GET /5 | 2.25 | 1.91 |
| harjoitus sivulta 5 | 1.09 | 0.03 |
| harjoitus sivulta 5/kommenttisivu2 | 1.08 | 0.01 |
| harjoitus sivulta 5/kommenttisivu1 | 1.08 | 0.01 |
| harjoituksen käyttäjä | 0.22 | 0.03 |
| oman harjoituksen hakeminen | 1.01 | 0.01 |
| /delete_workout | 0.08 | 0.01 |
| ?query=sisältö | 0.49 | 0.53 |
