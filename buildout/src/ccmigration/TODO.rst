Note
====

Provincie
---------
Rinominare le seguenti provincie:
 * "Reggio Nell'Emilia" in "Reggio Emilia"
 * "Bolzano-Bozen" in "Bolzano"


Listino prezzi
--------------
Il listino prezzi *Rimessaggio Imbarcazioni* c'è due volte: una con un dettaglio
relativo al 2013-2014, uno senza.
Il primo "blocca" la creazione del secondo, perché hanno lo stesso nome, che
viene considerata chiave primaria.


Partner
-------
Nella sorgente esiste una relazione con un modello **Causale trasporto** che
nella destinazione manca.
Solo 5 partner hanno il campo valorizzato:

 * Alor Group piscine Srl
 * EKOTOURIST SAS
 * Jet Capsule Srl
 * MONTECOLINO S.p.a.
 * Saccone Salvatore Vito


La relazione con gli utenti per ora è forzata: ``user_id = 1``.
In effetti, solo per questi 28 partner è diverso da 1:

 * Altissimi Fabio
 * Bellini Francesco
 * Bello Roberto
 * CO.GE.MAN SRL
 * Dadusc Roberto
 * Daniele Coretti
 * Di Luzio Fabio
 * Di Roma Angelo
 * Fantastico Alan Ferri
 * Formicola Enzo
 * Gulfmarine Services
 * Guy Papillon
 * Joel Brakha
 * Lanari Fulvio
 * Lino Graziano
 * LO.DA. SRL
 * Malatesta Paolo
 * Mark Broich
 * Mohamed Abu Issa
 * N\xe1utica Man\xe9 Ferrari
 * Olivieri Vincenzo
 * Pierpaolo Supino
 * Salem Alsanbi
 * Sbardellati Aldo
 * Tommasini Mario
 * Total Game Srl
 * Venturoni Franco
 * Yanting Huang


La relazione ``res.partner.bank`` è valorizzata solo per 10 partner.
Dato che manca un valore richiesto (in particolare il numero di conto), è
meglio procedere manualmente una volta avuti i dati.
I partner coinvolti sono:

 * Autoricambi Maseco & C. Snc
 * Boening Italia Srl
 * COMPUTER POINT DI MARVULLI DONATO
 * Ecomet Sas di Cesare Stori & C.
 * Forniture Nautiche Italiane S.r.l.
 * HEDERA Società Cooperativa Sociale
 * LINKWIRELESS SRL
 * L.S. ADVANCED SOFTWARE SRL
 * LU.CI. SNC DI RIGHI LUCA & C.
 * Manca Dario

***************************************************
Procedura per migrazione modulo account:
ACCOUNT.MOVE
1. Si migrano le account.move che NON sono riferite da account.voucher o
   account.invoice
2. Per ciascuna move, migro le account.move.line relative
3. Eseguo il post di ciascuna account.move. Questa funzione esegue la
   validazione della account.move, genera un'account.analytic.line per ciascuna
   account.move.line valida. Inoltre se la account.move ha nome "/" genera un
   nuovo nome a partire dalla account.invoice se presente o dall'account.journal
   ed infine ne cambia lo stato in "posted".
4. POSSIBILE ERRORE: Effettua un ciclo sulle account.invoice (che a questo punto
   non dovrebbero essere ancora migrate) e cerca di associarle alle move.line
5. POSSIBILE ERRORE: Dovrebbe effettuare un ciclo per le associazioni con
   le reconcile_id?

ACCOUNT.INVOICE
6. Si migrano le account.invoice che non sono in stato 'cancel'
7. NON vengono migrate né le account.move né le account.move.line (che vengono
   invece associate al punto 4)
8. Si recupera lo stato della vecchia invoice: se era 'open' o 'paid', si invoca
   il metodo 'button_compute' che ricalcola le tasse e poi si invoca il wf
   'invoice_open' che porta la fattura in stato open. NOTA: nel commento c'è
   scritto anche che il workflow genera altre move.line, ma dal codice di odoo
   non mi sembra

ACCOUNT.VOUCHER
9. Si migrano i voucher
10. NON vengono migrate le move_id (create dal punto 12)
11. Per ciascuna account.voucher.line di credito o di debito, viene recuperata
    la relativa account.move.line. E' questa la fase in cui NON vengono quasi
    mai recuperati i valori corretti.
12. Viene invocato il workflow proforma_voucher che fa le seguenti cose:
    a. crea un account.move
    b. crea una account.move.line per ogni account.voucher.line (a questo punto
       a che serve il punto 11?)
    c. crea una writeoff line se serve (?)
    d. mette il voucher in stato 'posted'
    e. effettua il post della account.move generata al punto a.
    d. prova ad effettuare la riconciliazione


1. Migrare TUTTE account.move e account.move.line
2. Effettuare il post su tutte le move
4. Migrare le invoice
5. button_compute
6. Associare move e move.line
7. Forzare stato open
8. Migrare voucher
9. Forzare stato posted
10. Vedere questione reconcile
11. Forzare stato paid
