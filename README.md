# Aare
Aare on nutikas discordi juturobot mis räägib sulaselges eesti keeles. 
Aare on eelkõige mõeldud finantsteemadel arutama. 
Töö on veel pooleli ja Aare on alles alfa staadiumis.

## Kuidas Aare paigaldada?

### 1. Paigalda Python ja sõltuvused
Sul on vaja Python 3.10 või uuemat versiooni. Loo virtuaalne keskkond ja aktiveeri see.

Paigalda sõltuvused käsklusega:

    pip install -r requirements.txt

### 2. Loo Discordi bot
Mine aadressile [Discord Developer Portalisse](https://discord.com/developers/applications) ja loo uus rakendus.
Vali vasakult menüüst "Bot" ja vajuta "Add Bot". Pane Botile nimeks **Aare**, lisa elulugu ja pilt.

Vajuta "Copy" et kopeerida boti token. Jäta see kusagile korraks meelde.

Siis vali vasakult SETTINGS alajaotuses "Oauth2" leht "URL Generator". Linnuta "bot".

Bot Permissions alt vali kõik "TEXT PERMISSIONS" alt, "GENERAL PERMISSIONS" alt "Read Messages/View Channels".

Kopeeri alt Genereeritud URL ja ava see brauseris. Lisa bot soovitud serverisse.

### 3. Loo konfiguratsioonifail
Nimeta ümber ```.env.naide``` fail ```.env```-ks ja ava see tekstiredaktoris.
Kirjuta faili oma Discordi boti token ja [OpenAI API token](https://platform.openai.com/account/api-keys).
 Salvesta.

### 4. Käivita Aare
Käivita Aare käsklusega:

    python main.py

Ja nüüd ongi sul kratt nimega Aare, kes valmis sinuga Discordis juttu ajama ja aitama sul aardeid kokku ajada.