
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import tietokanta # tähän voi vaihtaa sitten sen meidän yhteisen tietokannan
import pandas as pd

class Kaaviot:
    def __init__(self):
        self.db = tietokanta.db
        self.df = pd.DataFrame((self.db.taloudenhallinta.find()))
        #näihin voi vaihtaa ne nimikkeet, jotka olemme valinneet:
        self.nimi = ["nimi"]
        self.summa = ["summa"]
        self.paivamaara = ["paivamaara"]
        #pandas muutti jostain syystä Mongosin Double-numeron objektiksi, joten muutin sen tässä floatiksi:
        self.df[self.summa] = self.df[self.summa].astype(float)
        #print(self.df.dtypes)
        #self.df.dtypes

    def create_hist(self):
        self.df.hist(column=self.paivamaara)
        self.df.hist(column=self.summa)


    def create_grafic_date_and_sum(self):
        plt.figure(figsize=(40, 6))
        sns.barplot(x = "paivamaara", y = "summa", data=self.df)
        #kuinka paljon rahaa on käytetty tiettyyn kellonaikaan. tämä pitää vielä vaihtaa päiväkohtaiseksi,
        #eli tietojen tallennuksen yhteydessä otetaan ylös vain tietty päivämäärä
        #tässä kaikki ostot, eli pitää vielä filtteröidä kuukausien mukaan

        graafi1 = "graafi.png"
        plt.savefig(graafi1)

    
    def create_grafic_name_and_sum(self):  
        plt.figure(figsize=(40, 6))
        sns.barplot(x = "nimi", y = "summa", data=self.df)
        #kuinka paljon rahaa on käytetty tiettyyn kauppaan

        graafi2 = "graafi2.png"
        plt.savefig(graafi2)
