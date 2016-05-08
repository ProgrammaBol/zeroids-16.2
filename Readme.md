Cosa e' Zeroids
===============

Questo e' un progetto realizzato in collaborazione con i partecipanti
al laboratorio "Programmare un videogioco da Zero"

Dipendenze
=========
Zeroids ha bisogno di due cose per funzionare
- python 2.7
- pygame 1.9.1


Come si lancia
=======
basta eseguire il file zeroids.py con python


Come si gioca
========

- Bottone del mouse - salta intro
- Spazio - spara
- n - passa al livello successivo
- p - metti in pausa il gioco

Descrizione dei file
=============
- assets contiene i file statici (immagini, suoni, ..)
- core contiene il codice sorgente
  - sigla contiene il codice e i file dell'intro
  - colorlog codice per il logging colorato
  - ufo, turret, asteroids contentono il codice dei nemici
  - players contiene il codice dell'astronave principale
  - main.py contiene il loop principale
  - datastractures contiene il codice per la gestione degli eventi e per l'oggetto globale delle informazioni generali
  - sprites contiene il codice di base degli sprite e il generatore di sprite
  - exceptions contiene gli errori personalizzati
  - gamecontroller contiene il coordinatore delle fasi di gioco e il codice di gestione delle collisioni
  - texts contiene il generatore di test
  - weapons contiene il codice di gestione delle armi
  - sounds contiene il generatore di suoni



Licenza
========

Il codice e' distribuito con licenza GPL v3.0
