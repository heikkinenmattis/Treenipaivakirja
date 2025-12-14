# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta 

```
❯ venv/bin/pylint *.py
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:78:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:107:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:119:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:197:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:223:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:223:0: R0914: Too many local variables (19/15) (too-many-locals)
app.py:223:0: R0912: Too many branches (19/12) (too-many-branches)
app.py:223:0: R0915: Too many statements (62/50) (too-many-statements)
app.py:367:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:372:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:401:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:438:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:462:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:478:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:502:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:502:0: R0914: Too many local variables (23/15) (too-many-locals)
app.py:502:0: R0912: Too many branches (21/12) (too-many-branches)
app.py:502:0: R0915: Too many statements (75/50) (too-many-statements)
app.py:692:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:14:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:28:0: R0913: Too many arguments (10/5) (too-many-arguments)
users.py:28:0: R0917: Too many positional arguments (10/5) (too-many-positional-arguments)
users.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:74:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:112:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:127:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:142:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module workouts
workouts.py:1:0: C0114: Missing module docstring (missing-module-docstring)
workouts.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:28:0: R0913: Too many arguments (14/5) (too-many-arguments)
workouts.py:28:0: R0917: Too many positional arguments (14/5) (too-many-positional-arguments)
workouts.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:68:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:96:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:139:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:163:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:171:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:189:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:198:0: C0116: Missing function or method docstring (missing-function-docstring)
workouts.py:1:0: R0801: Similar lines in 2 files
==users:[77:87]
==workouts:[71:81]
                        w.workout_id,
                        w.user_id,
                        u.username,
                        s.sport_name,
                        datetime(w.begin_time) as begin_time,
                        datetime(w.end_time) as end_time,
                        case when s.sport_type = 'Strength' then sum(w.sets*w.reps*w.weight) else null end as total_kilograms,
                        case when s.sport_type = 'Endurance' then sum(w.kilometers) else null end as kilometers,
                        s.sport_type,
                        timediff(w.end_time, w.begin_time) as duration, (duplicate-code)
workouts.py:1:0: R0801: Similar lines in 2 files
==users:[90:95]
==workouts:[83:88]
                from workouts w
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercises e on w.exercise_id = e.exercise_id
                join exercise_purposes p on w.purpose_id = p.purpose_id (duplicate-code)

------------------------------------------------------------------
Your code has been rated at 8.57/10 (previous run: 8.53/10, +0.04)

```

Käydään läpi raportin sisältö ja perustellaan korjaamatta jättämiset.

## Docstring-ilmoitukset
Pylint ilmoittaa, mikäli moduuleista puuttuu dokumentointi ja kommentointi. Osa näistä ilmoituksista liittyy jo valmiiden kirjastojen dokumentoinnin puutteeseen. 

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)

```

Sovellusta kehitettäessä on päätetty, että funktioita tai moduuleita ei kommentoida ja pyritty siihen, että ne olisivat nimeltään tarpeeksi selittäviä.

## Vaarallinen oletusarvo

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Ilmoitus viittaa ```db.py``` moduulin funktioiden ```execute``` ja ```query``` parametreihin ```params```, joiden oletusarvoksi on asetettu tyhjä lista ```[]```. Tässä tapauksessa vaarallinen oletusarvo ei haittaa, koska sqlite3-kirjaston execute-metodi lukee listaa, eikä muuta sitä. Kuitenkin, jos listaa muokattaisiin funktion sisällä, jäisi muutos Pythonissa muistiin.


## Liikaa paikallisia muuttujia, liikaa haaroja ja liikaa ehtolauseita

```
app.py:223:0: R0914: Too many local variables (19/15) (too-many-locals)
app.py:223:0: R0912: Too many branches (19/12) (too-many-branches)
app.py:223:0: R0915: Too many statements (62/50) (too-many-statements)

app.py:502:0: R0914: Too many local variables (23/15) (too-many-locals)
app.py:502:0: R0912: Too many branches (21/12) (too-many-branches)
app.py:502:0: R0915: Too many statements (75/50) (too-many-statements)

```

Ilmoitukset viittaavat app.py -moduulin funktioihin add_workout() ja edit_workout(). Tämä on tarkoituksellinen suunnittelurike. Vaikka funktion tulisi tehdä vain yhtä asiaa, on tulkinnanvaraista, tehdäänkö tämä käyttäjän, vai ohjelman näkökulmasta. Käyttäjän näkökulmasta nämä funktiot tekevät yhden asian - lisäävät tai muokkaavat harjoituksen.

Kun kenttiä on useita, validaatioita on paljon ja alakategoriat riippuvat yläkategorioista, on luonnollista, että haarautumista syntyy. Funktioiden toiminnallisuudet voisi varmasti eriyttää pienemmän tason funktioille, mutta tämä voisi heikentää luettavuutta ja selkeyttä.

Kehittäjän päätöksellä näissä kahdessa funktiossa annetaan olla liikaa, mutta ei tarpeetonta määrää, paikallisia muuttujia, haaroja ja ehtolauseita.


## Liikaa argumentteja funktiolle

```
users.py:28:0: R0913: Too many arguments (10/5) (too-many-arguments)
workouts.py:28:0: R0913: Too many arguments (14/5) (too-many-arguments)

```

Nämä kaksi ilmoitusta viittaavat ```users.py``` ja ```workouts.py``` -moduulien funktioihin ```add_userdata()``` ja ```insert_workout()```. Kummassakin funktiossa tietoa syötetään yhteen tauluun, eikä olisi mitään mieltä alkaa pilkkomaan käyttäjätietojen syöttämistä ja treenin syöttämistä useammalle funktiolle.

Kehittäjän päätöksellä nämä funktiot saavat ottaa vastaan liikaa argumentteja.

## Liian samanlainen teksti kahdessa funktiossa

```
workouts.py:1:0: R0801: Similar lines in 2 files
==users:[77:87]
==workouts:[71:81]
                        w.workout_id,
                        w.user_id,
                        u.username,
                        s.sport_name,
                        datetime(w.begin_time) as begin_time,
                        datetime(w.end_time) as end_time,
                        case when s.sport_type = 'Strength' then sum(w.sets*w.reps*w.weight) else null end as total_kilograms,
                        case when s.sport_type = 'Endurance' then sum(w.kilometers) else null end as kilometers,
                        s.sport_type,
                        timediff(w.end_time, w.begin_time) as duration, (duplicate-code)
workouts.py:1:0: R0801: Similar lines in 2 files
==users:[90:95]
==workouts:[83:88]
                from workouts w
                join sports s on w.sport_id = s.sport_id
                join users u on w.user_id = u.id
                join exercises e on w.exercise_id = e.exercise_id
                join exercise_purposes p on w.purpose_id = p.purpose_id (duplicate-code)
```

Nämä ilmoitukset viittaavat toisteisuuteen kahdessa eri tiedostossa ```workouts.py``` ja ```users.py```. Tiedostojen funktiot ```get_workouts()``` ja ```fetch_user_workouts()``` ovat hyvin samanlaiset keskenään.

On kieltämättä totta, että nostaessa tietyn käyttäjän treeni ja nostaessa kaikki treenit kentät ja tietokantakyselyn rakenne on sama. Ainoaksi eroksi muodostuu täten käyttäjän harjoituksen hakevassa ```fetch_user_workouts()``` -funktiossa oleva ehto, joka rajaa palautettavat tietueet yhteen käyttäjään. 

Kehittäjän päätöksellä tämä virhe jätetään ohjelmaan, koska kehittäjä haluaa erotella harjoituksia ja käyttäjiä koskevat tietokantatoimenpiteet.