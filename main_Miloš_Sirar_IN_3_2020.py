# -*- coding: utf-8 -*-

"""

Autor: Miloš Sirar IN 3/2020
Predmet: Metode i tehnike nauke o podacima
Kodni naziv: vreme_Šangaj
Naslov istraživanja: Eksplorativna analiza podataka o vremenskim prilikama (parametrima) i kvalitetu vazduha u Šangaju u periodu 2014-2021
Programski jezik: Python
Biblioteke: pandas, numpy, matplotlib, seaborn

Napomena:
Da bi program radio kako treba, potrebno je da se ćelije pokreću (izvršavaju) redom kako su i napisane

"""

#%% Biblioteke

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#%% Ucitavanje glavnog fajla shanghai.csv

podaci_vreme_sangaj = pd.read_csv("shanghai.csv")

#%% Prikazi oblik i tipove kolona

print("Oblik:", podaci_vreme_sangaj.shape)
print()
print("Tipovi kolona:")
print(podaci_vreme_sangaj.dtypes)

#%% Uklanjanje NULL i NA podataka ukoliko postoje

shape_podaci_vreme_sangaj_pre = podaci_vreme_sangaj.shape

podaci_vreme_sangaj.dropna(inplace=True)

if shape_podaci_vreme_sangaj_pre != podaci_vreme_sangaj.shape:
    print("Postojale su vrednosti koje nisu bile popunjene, one su sada izbacene.")
    print("Oblik posle uklanjanja NA vrednosti:", podaci_vreme_sangaj.shape)
    print("Tipovi posle uklanjanja NA vrednosti:")
    print(podaci_vreme_sangaj.dtypes)
    print()
    
#%% Promena naziva kolona na srpski jezik i uklanjanje kolona koje nece biti potrebne za istrazivanje

podaci_vreme_sangaj.rename(columns={
    "date_time" : "datum_merenja",
    "maxtempC" : "max_dnevna_temperatura",
    "mintempC" : "min_dnevna_temperatura",
    "totalSnow_cm" : "ukupno_snega_cm",
    "sunHour" : "broj_suncanih_sati",
    "uvIndex" : "uv_index",
    "moon_illumination" : "osvetljenost_meseca",
    "moonrise" : "vreme_izlaska_meseca",
    "moonset" : "vreme_zalaska_meseca",
    "sunrise" : "vreme_izlaska_sunca",
    "sunset" : "vreme_zalaska_sunca",
    "DewPointC" : "temperatura_tacke_rose",
    "FeelsLikeC" : "temperatura_po_osecaju",
    "HeatIndexC" : "temperatura_indeksa_toplote",
    "WindChillC" : "temperatura_hladjenja_vetrom",
    "WindGustKmph" : "udar_vetra_kmh",
    "cloudcover" : "oblacnost",
    "humidity" : "vlaznost_vazduha",
    "precipMM" : "padavine_mm",
    "pressure" : "atmosferski_pritisak",
    "tempC" : "temperatura",
    "visibility" : "vidljivost",
    "winddirDegree" : "pravac_vetra",
    "windspeedKmph" : "brzina_vetra_kmh",
    "location" : "lokacija"
    }, inplace=True)

print()
print("Prikaz nakon promene naziva kolona na srpski jezik:")
print(podaci_vreme_sangaj.dtypes)
print()

podaci_vreme_sangaj.drop(columns=[
    "ukupno_snega_cm",
    "broj_suncanih_sati",
    "uv_index",
    "osvetljenost_meseca",
    "vreme_izlaska_meseca",
    "vreme_zalaska_meseca",
    "vreme_izlaska_sunca",
    "vreme_zalaska_sunca",
    "temperatura_tacke_rose",
    "temperatura_po_osecaju",
    "temperatura_indeksa_toplote",
    "temperatura_hladjenja_vetrom",
    "udar_vetra_kmh",
    "vlaznost_vazduha",
    "atmosferski_pritisak",
    "temperatura",
    "lokacija"], inplace=True)

print()
print("Prikaz nakon uklanjanja kolona koje nisu potrebne za ovo istrazivanje:")
print(podaci_vreme_sangaj.dtypes)
print()

#%% Promena tipa kolone datum_merenja u datetime64 zbog daljeg rada

podaci_vreme_sangaj["datum_merenja"] = pd.to_datetime(podaci_vreme_sangaj["datum_merenja"])
print("Datumi nakon promene:")
print(podaci_vreme_sangaj["datum_merenja"])
print()
print("Datum merenja je sada tipa:", podaci_vreme_sangaj.dtypes[0])
print()

#%% Dodavanje kolona godina, mesec, dan na osnovu datum_merenja radi lakseg rada

print(podaci_vreme_sangaj.dtypes)
print()

podaci_vreme_sangaj.insert(loc=1, column="godina_merenja", value=podaci_vreme_sangaj["datum_merenja"].dt.year)
podaci_vreme_sangaj.insert(loc=2, column="mesec_merenja", value=podaci_vreme_sangaj["datum_merenja"].dt.month)
podaci_vreme_sangaj.insert(loc=3, column="dan_merenja", value=podaci_vreme_sangaj["datum_merenja"].dt.day)

podaci_vreme_sangaj["mesec_merenja"] = podaci_vreme_sangaj["mesec_merenja"].replace(
    {
     1 : "januar",
     2 : "februar",
     3 : "mart",
     4 : "april",
     5 : "maj",
     6 : "jun",
     7 : "jul",
     8 : "avgust",
     9 : "septembar",
     10 : "oktobar",
     11 : "novembar",
     12 : "decembar"
     })

print(podaci_vreme_sangaj.dtypes)
print()

#%% Ucitavanje pomocnog fajla shanghai-air-quality.csv

podaci_kvalitet_vazduha_sangaj = pd.read_csv("shanghai-air-quality.csv")

#%% Prikazi oblik i tipove kolona

print("Oblik:", podaci_kvalitet_vazduha_sangaj.shape)
print()
print("Tipovi kolona:")
print(podaci_kvalitet_vazduha_sangaj.dtypes)

#%% Promena naziva kolona na srpski jezik

podaci_kvalitet_vazduha_sangaj.rename(columns={
    "date" : "datum_merenja",
    " pm25" : "PM25",
    " pm10" : "PM10",
    " o3" : "O3",
    " no2" : "NO2",
    " so2" : "SO2",
    " co" : "CO"
    }, inplace=True)

print()
print("Prikaz nakon promene naziva kolona na srpski jezik:")
print(podaci_kvalitet_vazduha_sangaj.dtypes)
print()

#%% Promena tipa kolone datum_merenja u datetime64 zbog daljeg rada

podaci_kvalitet_vazduha_sangaj["datum_merenja"] = pd.to_datetime(podaci_kvalitet_vazduha_sangaj["datum_merenja"])
print("Datumi nakon promene:")
print(podaci_kvalitet_vazduha_sangaj["datum_merenja"])
print()
print("Datum merenja je sada tipa:", podaci_kvalitet_vazduha_sangaj.dtypes[0])
print()

#%% Ovde ne uklanjam NULL i NA vrednosti, zato sto je moguce izracunati koeficijente i uz pomoc bar jednog obelezja, nego cu im dodeliti vrednost -1.0

podaci_kvalitet_vazduha_sangaj.replace(' ', -1.0, inplace=True)

#%% Promena tipova kolona na float

podaci_kvalitet_vazduha_sangaj.PM25 = podaci_kvalitet_vazduha_sangaj.PM25.astype(float)
podaci_kvalitet_vazduha_sangaj.PM10 = podaci_kvalitet_vazduha_sangaj.PM10.astype(float)
podaci_kvalitet_vazduha_sangaj.O3 = podaci_kvalitet_vazduha_sangaj.O3.astype(float)
podaci_kvalitet_vazduha_sangaj.NO2 = podaci_kvalitet_vazduha_sangaj.NO2.astype(float)
podaci_kvalitet_vazduha_sangaj.SO2 = podaci_kvalitet_vazduha_sangaj.SO2.astype(float)
podaci_kvalitet_vazduha_sangaj.CO = podaci_kvalitet_vazduha_sangaj.CO.astype(float)

print()
print("Prikaz nakon promene tipova kolona na float:")
print(podaci_kvalitet_vazduha_sangaj.dtypes)
print()

#%% Spajanje glavnog skupa podataka sa dodatnim kolonama iz drugog fajla

podaci = pd.merge(podaci_vreme_sangaj, podaci_kvalitet_vazduha_sangaj, on="datum_merenja", how="left")

print(podaci.dtypes)
print(podaci.shape)

#%% Pronalazak nerelevatnih godina za istrazivanje i njihovo izbacivanje iz skupa podataka, Pregled broja uzoraka po godinama

broj_podataka_po_godinama = podaci.groupby(["godina_merenja"])["godina_merenja"].count()
print(broj_podataka_po_godinama)
print()

for godina in range(2014, 2022):
    if broj_podataka_po_godinama[godina] < 0.95 * 365:
        print("Podaci za {}. godinu ce biti izbaceni iz skupa podataka, jer nemaju dovoljan broj podataka za analizu.".format(godina))
        podaci.drop(podaci[podaci["godina_merenja"] == godina].index, inplace=True)

print()
broj_podataka_po_godinama = podaci.groupby(["godina_merenja"])["godina_merenja"].count()
print(broj_podataka_po_godinama)

#%% Dodavanje obelezja za AQI koji ce se izracunati, dodaju se sub_index, AQI i AQI_objasnjenje

# racuna se prvo svaki sub indeks posebno, a zatim se maksimalna vrednost sub indeksa uzima kao AQI

#%% funkcije za sub_indekse za kvalitet vazduha

def funkcija_PM25_sub_indeks(pm25):
    if pm25 <= 30:
        return pm25 * 50 / 30
    elif pm25 <= 60:
        return 50 + (pm25 - 30) * 50 / 30
    elif pm25 <= 90:
        return 100 + (pm25 - 60) * 100 / 30
    elif pm25 <= 120:
        return 200 + (pm25 - 90) * 100 / 30
    elif pm25 <= 250:
        return 300 + (pm25 - 120) * 100 / 130
    elif pm25 > 250:
        return 400 + (pm25 - 250) * 100 / 130
    else:
        return 0

def funkcija_PM10_sub_indeks(pm10):
    if pm10 <= 100:
        return pm10
    elif pm10 <= 250:
        return 100 + (pm10 - 100) * 100 / 150
    elif pm10 <= 350:
        return 200 + (pm10 - 250)
    elif pm10 <= 430:
        return 300 + (pm10 - 350) * 100 / 80
    elif pm10 > 430:
        return 400 + (pm10 - 430) * 100 / 80
    else:
        return 0

def funkcija_O3_sub_indeks(o3):
    if o3 <= 50:
        return o3 * 50 / 50
    elif o3 <= 100:
        return 50 + (o3 - 50) * 50 / 50
    elif o3 <= 168:
        return 100 + (o3 - 100) * 100 / 68
    elif o3 <= 208:
        return 200 + (o3 - 168) * 100 / 40
    elif o3 <= 748:
        return 300 + (o3 - 208) * 100 / 539
    elif o3 > 748:
        return 400 + (o3 - 400) * 100 / 539
    else:
        return 0

def funkcija_NO2_sub_indeks(no2):
    if no2 <= 40:
        return no2 * 50 / 40
    elif no2 <= 80:
        return 50 + (no2 - 40) * 50 / 40
    elif no2 <= 180:
        return 100 + (no2 - 80) * 100 / 100
    elif no2 <= 280:
        return 200 + (no2 - 180) * 100 / 100
    elif no2 <= 400:
        return 300 + (no2 - 280) * 100 / 120
    elif no2 > 400:
        return 400 + (no2 - 400) * 100 / 120
    else:
        return 0

def funkcija_SO2_sub_indeks(so2):
    if so2 <= 40:
        return so2 * 50 / 40
    elif so2 <= 80:
        return 50 + (so2 - 40) * 50 / 40
    elif so2 <= 380:
        return 100 + (so2 - 80) * 100 / 300
    elif so2 <= 800:
        return 200 + (so2 - 380) * 100 / 420
    elif so2 <= 1600:
        return 300 + (so2 - 800) * 100 / 800
    elif so2 > 1600:
        return 400 + (so2 - 1600) * 100 / 800
    else:
        return 0

def funkcija_CO_sub_indeks(co):
    if co <= 1:
        return co * 50 / 1
    elif co <= 2:
        return 50 + (co - 1) * 50 / 1
    elif co <= 10:
        return 100 + (co - 2) * 100 / 8
    elif co <= 17:
        return 200 + (co - 10) * 100 / 7
    elif co <= 34:
        return 300 + (co - 17) * 100 / 17
    elif co > 34:
        return 400 + (co - 34) * 100 / 17
    else:
        return 0

#%% dodavanje novih kolona, odnosno izracunatih sub_indeksa

podaci.insert(loc=17, column="PM25_sub_index", value=podaci["PM25"].apply(lambda x : funkcija_PM25_sub_indeks(x)))
podaci.insert(loc=18, column="PM10_sub_index", value=podaci["PM10"].apply(lambda x : funkcija_PM10_sub_indeks(x)))
podaci.insert(loc=19, column="O3_sub_index", value=podaci["O3"].apply(lambda x : funkcija_O3_sub_indeks(x)))
podaci.insert(loc=20, column="NO2_sub_index", value=podaci["NO2"].apply(lambda x : funkcija_NO2_sub_indeks(x)))
podaci.insert(loc=21, column="SO2_sub_index", value=podaci["SO2"].apply(lambda x : funkcija_SO2_sub_indeks(x)))
podaci.insert(loc=22, column="CO_sub_index", value=podaci["CO"].apply(lambda x : funkcija_CO_sub_indeks(x)))

print(podaci.dtypes)
print()
print(podaci.head(10))

#%% funkcija AQI_objasnjenje na osnovu AQI vrednosti

def funkcija_AQI_objasnjenje(aqi):
    if aqi <= 50:
        return "Dobro"
    elif aqi <= 100:
        return "Umereno"
    elif aqi <= 150:
        return "Nezdravo za osetljive grupe"
    elif aqi <= 200:
        return "Nezdravo"
    elif aqi <= 300:
        return "Veoma nezdravo"
    elif aqi > 300:
        return "Veoma opasno"
    else:
        return np.NaN

#%% dodavanje novih kolona, AQI i AQI_objasnjenje

podaci.insert(loc=23, column="AQI", value=round(podaci[["PM25_sub_index", "PM10_sub_index", "O3_sub_index", "NO2_sub_index", "SO2_sub_index", "CO_sub_index"]].max(axis = 1)))
podaci.insert(loc=24, column="AQI_objasnjenje", value=podaci["AQI"].apply(lambda x : funkcija_AQI_objasnjenje(x)))

print(podaci.dtypes)
print()
print(podaci.head(10))

#%% Analiza 1 - Prosecna maksimalna temperatura po godinama za celu godinu

podaci_1 = podaci.loc[:, ["godina_merenja", "max_dnevna_temperatura"]].groupby(["godina_merenja"]).agg(np.mean)

print()
print("Prikaz prosecnih maksimalnih temperatura po godinama za celu godinu")
print()
print(podaci_1)

plt.figure(figsize=(10, 4))

plt.plot(podaci_1.index.get_level_values("godina_merenja"), podaci_1["max_dnevna_temperatura"], marker="o", mec="black", mfc="black", linewidth=2)
plt.title("Prosečna godišnja maksimalna temperatura [°C]")
plt.xlabel("godine")
plt.ylabel("prosečne maksimalne temperature [°C]")

plt.show()

#%% Analiza 2 - Prosecna minimalna temperatura po godinama za celu godinu

podaci_2 = podaci.loc[:, ["godina_merenja", "min_dnevna_temperatura"]].groupby(["godina_merenja"]).agg(np.mean)

print()
print("Prikaz prosečnih maksimalnih temperatura po godinama za celu godinu")
print()
print(podaci_2)

plt.figure(figsize=(10, 4))

plt.plot(podaci_2.index.get_level_values("godina_merenja"), podaci_2["min_dnevna_temperatura"], color="green", marker="o", mec="black", mfc="black", linewidth=2)
plt.title("Prosečna godišnja minimalna temperatura [°C]")
plt.xlabel("godine")
plt.ylabel("prosečne minimalne temperature [°C]")

plt.show()

#%% Analiza 3 - Prosecna maksimalna temperatura po godinama za svaki mesec

meseci = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]

for mesec in meseci:
    
    podaci_3 = podaci.loc[podaci["mesec_merenja"] == mesec, ["godina_merenja", "max_dnevna_temperatura"]].groupby(["godina_merenja"]).agg(np.mean)
    
    print()
    print("Prikaz prosečnih maksimalnih temperatura po godinama za mesec {}".format(mesec))
    print()
    print(podaci_3)

    plt.figure(figsize=(10, 4))

    plt.plot(podaci_3.index.get_level_values("godina_merenja"), podaci_3["max_dnevna_temperatura"], marker="o", mec="black", mfc="black", linewidth=2)
    plt.title("Prosečna maksimalna temperatura za mesec {} [°C]".format(mesec))
    plt.xlabel("godine")
    plt.ylabel("prosečne maksimalna temperature [°C]")
    
    plt.show()

#%% Analiza 4 - Prosecna minimalna temperatura po godinama za svaki mesec

meseci = ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"]

for mesec in meseci:
    
    podaci_4 = podaci.loc[podaci["mesec_merenja"] == mesec, ["godina_merenja", "min_dnevna_temperatura"]].groupby(["godina_merenja"]).agg(np.mean)

    print()
    print("Prikaz prosečnih minimalnih temperatura po godinama za mesec {}".format(mesec))
    print()
    print(podaci_4)

    plt.figure(figsize=(10, 4))

    plt.plot(podaci_4.index.get_level_values("godina_merenja"), podaci_4["min_dnevna_temperatura"], color="green", marker="o", mec="black", mfc="black", linewidth=2)
    plt.title("Prosečna minimalna temperatura za mesec {} [°C]".format(mesec))
    plt.xlabel("godine")
    plt.ylabel("prosečne minimalna temperature [°C]")
    
    plt.show()

#%% Analiza 5. - Prosecna maksimalna temperatura po mesecima za svaku godinu

godine = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
meseci_recnik = { "januar" : 1, "februar" : 2, "mart" : 3, "april" : 4, "maj" : 5, "jun" : 6, "jul" : 7, "avgust" : 8, "septembar" : 9, "oktobar" : 10, "novembar" : 11, "decembar" : 12 }

for godina in godine:
    
    podaci_5 = podaci.loc[podaci["godina_merenja"] == godina, ["mesec_merenja", "max_dnevna_temperatura"]].groupby(["mesec_merenja"]).agg(np.mean)
    podaci_5.sort_values("mesec_merenja", key = lambda x : x.apply (lambda x : meseci_recnik[x]), inplace=True)
    
    print()
    print("Prikaz prosečnih maksimalnih temperatura po mesecima za godinu {}.".format(godina))
    print()
    print(podaci_5)

    plt.figure(figsize=(12, 6))

    plt.plot(podaci_5.index.get_level_values("mesec_merenja"), podaci_5["max_dnevna_temperatura"], marker="o", mec="black", mfc="black", linewidth=2)
    plt.title("Prosečna maksimalna temperatura po mesecima za {}. godinu [°C]".format(godina))
    plt.xlabel("meseci")
    plt.ylabel("prosečne maksimalna temperature [°C]")
    
    plt.show()

#%% Analiza 6. - Prosecna minimalna temperatura po mesecima za svaku godinu

godine = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
meseci_recnik = { "januar" : 1, "februar" : 2, "mart" : 3, "april" : 4, "maj" : 5, "jun" : 6, "jul" : 7, "avgust" : 8, "septembar" : 9, "oktobar" : 10, "novembar" : 11, "decembar" : 12 }

for godina in godine:
    
    podaci_6 = podaci.loc[podaci["godina_merenja"] == godina, ["mesec_merenja", "min_dnevna_temperatura"]].groupby(["mesec_merenja"]).agg(np.mean)
    
    podaci_6.sort_values('mesec_merenja', key = lambda x : x.apply (lambda x : meseci_recnik[x]), inplace=True)
    
    print()
    print("Prikaz prosečnih minimalnih temperatura po mesecima za godinu {}.".format(godina))
    print()
    print(podaci_6)

    plt.figure(figsize=(12, 6))

    plt.plot(podaci_6.index.get_level_values("mesec_merenja"), podaci_6["min_dnevna_temperatura"], color="green", marker="o", mec="black", mfc="black", linewidth=2)
    plt.title("Prosečna minimalna temperatura po mesecima za {}. godinu [°C]".format(godina))
    plt.xlabel("meseci")
    plt.ylabel("prosečne minimalna temperature [°C]")
    
    plt.show()


#%% Analiza 7. - Maksimalne temperature u avgustu

godine = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

for godina in godine:
    podaci_7 = podaci.loc[(podaci["godina_merenja"] == godina) & (podaci["mesec_merenja"] == "avgust"), ["dan_merenja", "max_dnevna_temperatura"]]

    print()
    print("Prikaz maksimalnih temperatura za mesec avgust za godinu {}.".format(godina))
    print()
    print(podaci_7)
    
    plt.figure(figsize=(10, 4))
    
    plt.bar(podaci_7["dan_merenja"], podaci_7["max_dnevna_temperatura"])
    plt.title("Temperatura za mesec avgust {}. godine [°C]".format(godina))
    plt.xlabel("dani")
    plt.ylabel("temperature [°C]")
    plt.xticks(np.arange(1, 32))
    plt.xlim(0, 32)
    plt.yticks(np.arange(0, 41, 2))
    
    plt.show()

#%% Analiza 8. - Maksimalne temperature u septembru

godine = [2014, 2015, 2016, 2017, 2018, 2019, 2020]

for godina in godine:
    podaci_8 = podaci.loc[(podaci["godina_merenja"] == godina) & (podaci["mesec_merenja"] == "septembar"), ["dan_merenja", "max_dnevna_temperatura"]]

    print()
    print("Prikaz maksimalnih temperatura za mesecima septembar za godinu {}.".format(godina))
    print()
    print(podaci_8)
    
    plt.figure(figsize=(10, 4))
    
    plt.bar(podaci_8["dan_merenja"], podaci_8["max_dnevna_temperatura"], color="green")
    plt.title("Temperatura za mesec septembar {}. godine [°C]".format(godina))
    plt.xlabel("dani")
    plt.ylabel("temperature [°C]")
    plt.xticks(np.arange(1, 32))
    plt.xlim(0, 31)
    plt.yticks(np.arange(0, 41, 2))
    
    plt.show()

#%% Analiza 9. - Ukupna kolicina padavina mm kroz godine

podaci_9 = podaci.loc[:, ["godina_merenja", "padavine_mm"]].groupby("godina_merenja").agg(np.sum)


print()
print("Prikaz ukupne količine padavina mm")
print()
print(podaci_9)
    
plt.figure(figsize=(10, 4))
    
plt.bar(podaci_9.index.get_level_values("godina_merenja"), podaci_9["padavine_mm"])
plt.title("Godišnje količine padavina [mm]")
plt.xlabel("godine")
plt.ylabel("količina padavina [mm]")
    
plt.show()

#%% Analiza 10. - Prosecna vidljivost kroz godine

podaci_10 = podaci.loc[:, ["godina_merenja", "vidljivost"]].groupby("godina_merenja").agg(np.mean)

print()
print("Prikaz prosečne vidljivosti")
print()
print(podaci_10)
    
plt.figure(figsize=(10, 4))
    
plt.bar(podaci_10.index.get_level_values("godina_merenja"), podaci_10["vidljivost"])
plt.title("Prosečna vidljivost tokom godina [1-10]")
plt.xlabel("godine")
plt.ylabel("vidljivost [1-10]")
    
plt.show()

#%% Analiza 11. - Broj dana kada je vidljivost ispod 6

podaci_11 = podaci.loc[(podaci["vidljivost"] <= 5), :]

print()
print("Prikaz podataka kod kojih vidljivost ispod 6")
print()
print(podaci_11)

# podaci_11.to_csv("podaci_11.csv", index=False)

#%% Funkcija za prikaz kakva je jacina i smer korelacije

def funkcija_jacina_i_smer_korelacije(r):
    jacina_i_smer = ""
    if np.abs(r) < 0.3:
        jacina_i_smer += "nema linearne korelacije"
        return jacina_i_smer
    elif np.abs(r) < 0.7:
        jacina_i_smer += "slaba"
    elif np.abs(r) < 0.9:
        jacina_i_smer += "jaka"
    elif np.abs(r) < 1:
        jacina_i_smer += "veoma jaka"
    else:
        return "greska"
        
    if r < 0:
        jacina_i_smer += " negativna"
    else:
        jacina_i_smer += " pozitivna"
        
    return jacina_i_smer + " linearna korelacija"

#%% Analiza 11. nastavak - korelacija izmedju vidljivosti i oblacnosti

podaci_11 = podaci.loc[:, :]

r1 = np.corrcoef(podaci_11["vidljivost"], podaci_11["oblacnost"])
r1 = r1[0][1]
print()
print("Koeficijent korelacije r:", r1.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r1))
sns.regplot(x=podaci_11["vidljivost"], y=podaci_11["oblacnost"])

#%% Analiza 12.- Prikaz AQI - indeks kvaliteta vazduha po objasnjenjima

podaci_12 = podaci.loc[:, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_12.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja")
print()
print(podaci_12.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_12)
ax.xaxis.set_tick_params(rotation=90)

#%% Analiza 13. - Prikaz kvaliteta vazduha po godinama

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2014, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2014. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2015, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2015. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2016, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2016. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2017, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2017. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2018, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2018. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2019, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2019. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% 

podaci_13 = podaci.loc[podaci["godina_merenja"] == 2020, ["AQI_objasnjenje"]]

AQI_objasnjenje_recnik = { "Veoma opasno" : 1, "Veoma nezdravo" : 2, "Nezdravo" : 3, "Nezdravo za osetljive grupe" : 4, "Umereno" : 5, "Dobro" : 6 }

podaci_13.sort_values('AQI_objasnjenje', key = lambda x : x.apply (lambda x : AQI_objasnjenje_recnik[x]), inplace=True)

print()
print("Prikaz AQI objašnjenja za 2020. godinu")
print()
print(podaci_13.value_counts())

sns.set(style="darkgrid")
ax = sns.countplot(y="AQI_objasnjenje", data=podaci_13)
ax.xaxis.set_tick_params(rotation=90)

#%% Analiza 14. - Provera korelacije, tj. zavisnosti izmedju neke varijable i AQI 

# menjaju se ovde godine iz komentara za koju želim da proveravam korelaciju

# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2014, :]
# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2015, :]
# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2016, :]
# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2017, :]
# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2018, :]
# podaci_14 = podaci.loc[podaci["godina_merenja"] == 2019, :]
podaci_14 = podaci.loc[podaci["godina_merenja"] == 2020, :]
# podaci_14 = podaci.loc[:, :]

#%% Korelacija između maksimalne dnevne temperature i AQI

r1 = np.corrcoef(podaci_14["max_dnevna_temperatura"], podaci_14["AQI"])
r1 = r1[0][1]
print()
print("Koeficijent korelacije r:", r1.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r1))
sns.regplot(x=podaci_14["max_dnevna_temperatura"], y=podaci_14["AQI"])

#%% Korelacija između minimalne dnevne temperature i AQI

r2 = np.corrcoef(podaci_14["min_dnevna_temperatura"], podaci_14["AQI"])
r2 = r2[0][1]
print()
print("Koeficijent korelacije r:", r2.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r2))
sns.regplot(x=podaci_14["min_dnevna_temperatura"], y=podaci_14["AQI"])

#%% Korelacija između padavina mm i AQI

r3 = np.corrcoef(podaci_14["padavine_mm"], podaci_14["AQI"])
r3 = r3[0][1]
print()
print("Koeficijent korelacije r:", r3.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r3))
sns.regplot(x=podaci_14["padavine_mm"], y=podaci_14["AQI"])

#%% Korelacija između vidljivosti i AQI

r4 = np.corrcoef(podaci_14["vidljivost"], podaci_14["AQI"])
r4 = r4[0][1]
print()
print("Koeficijent korelacije r:", r4.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r4))
sns.regplot(x=podaci_14["vidljivost"], y=podaci_14["AQI"])

#%% Korelacija između brzine vetra km/h i AQI

r5 = np.corrcoef(podaci_14["brzina_vetra_kmh"], podaci_14["AQI"])
r5 = r5[0][1]
print()
print("Koeficijent korelacije r:", r5.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r5))
sns.regplot(x=podaci_14["brzina_vetra_kmh"], y=podaci_14["AQI"])

#%% Korelacija između oblačnosti i AQI

r6 = np.corrcoef(podaci_14["oblacnost"], podaci_14["AQI"])
r6 = r6[0][1]
print()
print("Koeficijent korelacije r:", r6.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r6))
sns.regplot(x=podaci_14["oblacnost"], y=podaci_14["AQI"])

#%% Korelacija između pravca vetra i AQI

r7 = np.corrcoef(podaci_14["pravac_vetra"], podaci_14["AQI"])
r7 = r7[0][1]
print()
print("Koeficijent korelacije r:", r7.round(2))
print()
print("Korelacija između maksimalne dnevne temperature i AQI je:", funkcija_jacina_i_smer_korelacije(r7))
sns.regplot(x=podaci_14["pravac_vetra"], y=podaci_14["AQI"])

#%% Deskriptivna statistika

# Potrebno pokrenuti zakomentarisanu opciju, a zakomentarisati opciju ispod nje da bi se videle sve kolone

# pd.set_option('display.max_columns', None)
pd.reset_option('display.max_columns')

print()
print("Deskriptivna statistika")
print()

print(podaci.loc[:, [
    "max_dnevna_temperatura",
    "min_dnevna_temperatura",
    "oblacnost",
    "padavine_mm",
    "vidljivost",
    "pravac_vetra",
    "brzina_vetra_kmh",
    "PM25",
    "PM10",
    "O3",
    "NO2",
    "SO2",
    "CO",
    "AQI"
    ]].describe().round(2))

