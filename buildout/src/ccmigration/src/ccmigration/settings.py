TAX_CODES = {
    '10%': '10%',
    '10% (I)': '10% (I)',
    '10% (credito)': '10% (credito)',
    '10% (credito) (I)': '19% (credito) (I)',
    '19% (credito)': '19% (credito)',
    '19% (credito) (I)': '19,6% (credito) (I)',
    '19,6% (credito)': '19,6% (credito)',
    '19,6% (credito) (I)': '19,6% (credito) (I)',
    '20%': '20%',
    '20% (I)': '20% (I)',
    '20% (credito)': '20% (credito)',
    '20% (credito) (I)': '20% (credito) (I)',
    '21%': '21%',
    '21% (I)': '21% (I)',
    '21% (credito)': '21% (credito)',
    '21% (credito) (I)': '21% (credito) (I)',
    '21% indetraibile 60% (I)': '21% indetraibile 60% (I)',
    '22%': '22%',
    '22% (I)': '22% (I)',
    '22% (credito)': '22% (credito)',
    '22% (credito) (I)': '22% (credito) (I)',
    '22% indetraibile 60% (I)': '22% indetraibile 60% (I)',
    '4%': '4%',
    '4% (I)': '4% (I)',
    '4% (credito)': '4% (credito)',
    '4% (credito) (I)': '4% (credito) (I)',
    '5,5% (credito)': '5,5% (credito)',
    '5,5% (credito) (I)': '5,5% (credito) (I)',
    '7% (credito)': '7% (credito)',
    '7% (credito) (I)': '7% (credito) (I)',
    'IVA Esente Art.26 a credito': 'Es. Art.26',
    'Esente art.26 a credito (I)': 'Es.Art.26(I)',
    'Esente art.10 a credito (I)': 'Esente art.10 a credito (I)',
    'Esente art.10 a credito': 'Esente art.10 a credito',
    'Esente art.9.1 a credito': 'Esente art.9.1 a credito',
    'Esente art.9.1 a credito (I)': 'Esente art.9.1 a credito (I)',
    'IVA a credito': 'IVA a credito',
    'IVA a credito 20% detraibile 50%': 'IVA a credito 20% detraibile 50%',
    'IVA a credito 20% detraibile 50% (imponibile)': 'IVA a credito 20% detraibile 50% (I)',
    'IVA a credito 21% detraibile 40%': 'IVA a credito 21% detraibile 40%',
    'IVA a credito 21% detraibile 50%': 'IVA a credito 21% detraibile 50%',
    'IVA a credito 21% detraibile 50% (imponibile)': 'IVA a credito 21% detraibile 50% (I)',
    'IVA a credito 22% detraibile 40%': 'IVA a credito 22% detraibile 40%',
    'IVA a credito 22% detraibile 50%': 'IVA a credito 22% detraibile 50%',
    'IVA a credito 22% detraibile 50% (imponibile)': 'IVA a credito 22% detraibile 50% (I)',
    'IVA a credito (imponibile)': 'IVA a credito (I)',
    'IVA a debito': 'IVA a debito',
    'IVA a debito (imponibile)': 'IVA a debito (I)',
    'IVA esente Art.15 (I)': 'IVA esente Art.15 a debito (imponibile)',
    'IVA esente Art.15': 'IVA esente Art.15',
    'IVA esente Art.15 a credito (I)': 'IVA esente Art.15 a credito (I)',
    'IVA esente Art.15 a credito': 'IVA esente Art.15 a credito',
    'IVA Esente Art. 74': 'IVA Esente Art. 74',
    'IVA Esente Art. 74 (I)': 'IVA Esente Art. 74 (I)',
    'Iva esente Art.8 (DPR 633/72)': 'IVA esente Art.8',
    'IVA esente Art.8 (DPR 633/72) (I)': 'IVA esente Art.8 (I)',
    'Iva esente Art.9 (DPR 633/72)': 'IVA esente Art.9',
    'IVA esente Art.9 (DPR 633/72) (I)': 'IVA esente Art.9 (I)',
}



ACCOUNT_MAPPING = {}

# In theory, with the fixed pdc this become useless
# ACCOUNT_MAPPING = {
#     u'ATTIVIT\xc1': "ATTIVITA'",
#     u'DISPONIBILIT\xc1 LIQUIDE': "DISPONIBILITA' LIQUIDE",
#     'Banca Nazionale del Lavoro': 'BANCA NAZIONALE DEL LAVORO',
#     'CONTO c/c PAYPAL': 'CONTO C/C PAYPAL',
#     'Banca Popolare di Fondi': 'BANCA POPOLARE DI FONDI',
#     'Banca Popolare di Fondi 100008685': 'BANCA POPOLARE DI FONDI',
#     'Utile di esercizio': 'UTILE DI ESERCIZIO',
#     u'PASSIVIT\xc1': "PASSIVITA'",
#     'Lasermar c/finanziamento soci': 'Lasermar C/FINANZIAMENTO SOCI',
#     'Se.ma.ter. c/finanzanziamento soci': 'SE.MA.TER. C/CONFERIMENTO',
#     'Casa Giovanni c/finanziamento soci': 'Casa Giovanni C/FINANZIAMENTO SOCI',
#     'Dettorre Patrizia c/finanziamento soci': 'DETTORRE PATRIZIA C/CONFERIMENTO',
#     'Casa Massimiliano c/finanziamento soci': 'Casa Massimiliano C/FINANZIAMENTO SOCI',
#     'Costi Produzione': 'Costi Produzione',
#     'Perdita di esercizio': 'PERDITA DI ESERCIZIO ',
#     u'INDENNIT\xc1 DI FINE RAPPORTO': "INDENNITA' DI FINE RAPPORTO",
#     'PEDAGGI AUTOSTRADALI E PARGHEGGI': 'PEDAGGI AUTOSTRADALI E PARCHEGGI',
#     'Fiera di Genova': 'FIERA DI GENOVA',
#     'Fiera di DUBAI': 'FIERA DI DUBAI',
#     'Fiera di Roma': 'FIERA DI ROMA',
#     'transitorio': 'TRASITORIO',
#     'Valore della produzione': 'VALORE DELLA PRODUZIONE',
#     'Dettorre Patrizia c/finanziamento soci': 'Dettorre Patrizia C/FINANZIAMENTO SOCI',
#     'CONTRIBUTI LAV. DIP. DM Inps': 'CONTRIBUTI LAVORATORI DIPENDENTI'
# }
