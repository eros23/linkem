# Linkem - Bug nell'Infrastruttura di Rete

## Descrizione Vulnerabilità
Linkem S.p.A. è una società italiana che opera nel settore delle telecomunicazioni, in particolare nel mercato della 
connessione a banda larga in modalità wireless. Dispone di una rete 4,5G Advanced.

I suoi apparati radio permettono di connettere i clienti ad internet tramite una rete NAT.
Scannerizzando la loro rete WLAN tramite un semplice scan scritto in python, abbiamo visto che tutti i clienti 
erano raggiungibili.

Applicando qualche modifica, per la pagina dedicata a Linkem, siamo riusciti ad entrare in molte antenne. Per
questo motivo abbiamo deciso di prendere il SID e la password della WIFI per dimostrare come la vulnerabilità
permettava di modificare tutte le impostazioni del modem.


Nel nostro caso abbiamo dato come comando:

`python scan.py 10.82.0.0/16`

Un malintenzionato poteva prendere il controllo delle antenne che non avevano cambiato la password di default e
dirottare il traffico internet, rubare password, e violare tutta la privacy dei clienti.


## Video

Dimostrazione su:

https://youtu.be/R3QDcI6RMgY

## Antenne Violate

Una parte del Dump dei dati può essere trovato qui:

https://github.com/eros23/linkem/blob/master/passwd_linkem.txt

## Come hackerare le antenne linkem con la password di default

Curioso? Vai [linkem wifi hacked](https://github.com/eros23/linkem-wifi-hacked)
