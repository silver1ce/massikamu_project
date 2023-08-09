import datetime
import matplotlib.pyplot as plt
import tietokanta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.uix.popup import Popup

#ensimmäinen sivu, joka avautuu:
class MainWindow(Screen):
    def __init__(self, **kw):
        super(MainWindow, self).__init__(**kw)
        #luodaan layout pääsivulle
        self.layout = BoxLayout(orientation='vertical')
        
        #luodaan kategorian ja summan syöttömahdollisuudet
        self.category_input = TextInput(hint_text='Kategoria')
        self.amount_input = TextInput(hint_text='Summa')

        #luodaan buttonit, joilla voi lisätä tiedot ja siirtyä toiselle sivulle
        self.add_expense_button = Button(text='Lisää kulu', on_press=self.add_expense)

        #luodaan näytä-button
        self.show_button = Button(text='Näytä tiedot', on_press=self.switch_to_reportwindow)
       # self.remove_expense_button = Button(text='Remove Expense', on_press=self.remove_expense)
       
        #lisätään otsikko
        self.report_label = Label(text='MASSIKAMU', size_hint=(1, 0.8))
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kategorian ja summan syöttö, ja buttonit
        self.layout.add_widget(self.report_label)

        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(self.add_expense_button)
        #self.layout.add_widget(self.remove_expense_button)
        self.layout.add_widget(self.show_button)
        
        #lopuksi lisätään layout tähän mainwindowiin
        self.add_widget(self.layout)

    def add_expense(self, instance):

        #jos käyttäjä ei kirjoita mitään, ja yrittää painaa Lisää kulu-nappia,
        #mitään ei tapahdu
        if len(self.category_input.text) == 0:
            print("ei mitää ")
        #jos sen sijaan käyttäjä kirjoittaa jotakin kategoriakohtaan, kokeillaan 
        #seuraavaksi, onhan käyttäjä syöttänyt Summa-kohtaan jonkin luvun, joka on
        #muunnettavissa floatiksi. jos tämäkin onnistuu, tiedot lisätään tietokantaan
        #päivämäärä- ja aikatietojen kera
        elif len(self.category_input.text) > 0:
            category = self.category_input.text
            print("suurempi")
            try:
                amount = float(self.amount_input.text)
                expense = {
                "category": category,
                "amount": amount,
                "date": datetime.datetime.now()
                }
                tietokanta.expense_collection.insert_one(expense)
                #lisätään popup-ikkuna, joka kertoo, että tiedot on lisätty onnistuneesti
                lisattyPopup = Popup(title="Onnistui!", 
                content=Label(text="Tietosi on nyt lisätty."), 
                size_hint=(0.7, 0.2))
                lisattyPopup.open()

        #jos syötettä ei ole muunnettavissa floatiksi, syntyy ValueError:
            except ValueError:
                #luodaan popup-ikkuna, joka kertoo, että käyttäjä ei ole kirjoittanut oikein syötettä
                popup = Popup(title='Hups!',
                content=Label(text='Tarkista syötteesi. Summan kohdalle tulee kirjoittaa jokin luku.'),
                size_hint=(0.7, 0.2))
                popup.open()
            
            
            self.category_input.text = ''
            self.amount_input.text = ''
        
    def switch_to_reportwindow(self, instance):
        self.manager.current = 'reportwindow'

#Toinen sivu, joka avautuu, jos painetaan Näytä tiedot -nappia:
class ReportWindow(Screen):
    def __init__(self, **kw):
        super(ReportWindow, self).__init__(**kw)
        #luodaan seuraavan sivun layout
        self.layout2 = BoxLayout(orientation='vertical')

        #otsikko seuraavalle sivulle
        self.label2 = Label(text='Massikamutietosi', size_hint=(1, 0.1))
        
        #luodaan toimintobuttonit
        self.all_the_information_button = Button(text="Näytä kaikki tiedot", on_press=self.generate_information, size_hint=(1, 0.4))
        self.generate_report_button = Button(text='Luo raportti', on_press=self.generate_report, size_hint=(1, 0.4))
        
        
        #luodaan navigointibutton
        self.button2 = Button(text="Takaisin etusivulle", on_press=self.switch_to_mainwindow, size_hint=(1, 0.1))
        
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kuva ja buttonit
        self.layout2.add_widget(self.label2)
        self.layout2.add_widget(self.all_the_information_button)
        self.layout2.add_widget(self.generate_report_button)
        self.layout2.add_widget(self.button2)

        #lopuksi lisätään layout tähän reportwindowiin
        self.add_widget(self.layout2)

        #self.layout2.add_widget(Button(text="Siirry Screen 1:een", on_press=self.switch_to_screen1))

    def switch_to_mainwindow(self, instance):
        self.manager.current = 'mainwindow'
    
    def switch_to_imagewindow(self):
        self.manager.current = 'imagewindow'
 
    def switch_to_informationwindow(self):
        self.manager.current = 'informationwindow'
    
    def generate_report(self, instance):
        current_date = datetime.date.today()
        first_day_of_month = datetime.datetime(current_date.year, current_date.month, 1)

        pipeline = [
            {
                "$match": {
                    "date": {"$gte": first_day_of_month}
                }
            },
            {
                "$group": {
                    "_id": "$category",
                    "total_amount": {"$sum": "$amount"}
                }
            }
        ]
        result = list(tietokanta.expense_collection.aggregate(pipeline))
        
        categories = []
        amounts = []
    
        for row in result:
            categories.append(row["_id"])
            amounts.append(row["total_amount"])

        # Generate bar chart
        plt.bar(categories, amounts)
        plt.xlabel('Kategoria')
        plt.ylabel('Summa')
        plt.title('Kuukausiraportti')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        #tämä tallentaa vain kerran tämän raportin, eikä uudestaan, kun nappia painetaan
        #tästä syystä raportti ei päivity, kun lisätään uusia ostoksia
        plt.savefig('report.png')  # Save the chart as an image
        
        plt.close()  # Close the figure
        
        
        # self.report_label.text = 'Monthly Expense Report'
        # self.report_label.canvas.ask_update()  # Update the label to show the new text
        # self.report_label.canvas.load_image('report.png')  # Load and display the chart image

       # self.add_widget(Button(text="Siirry Screen 2:een", on_press=self.switch_to_screen2))

        #lopuksi vaihdetaan seuraavalle sivulle
        self.switch_to_imagewindow()

    def generate_information(self, instance):
        #luodaan lista kaikista tiedoista
    
        data = tietokanta.expense_collection.find()
        tiedot = []
        ekarivi = []
        ekarivi.append("Kategoria")
        ekarivi.append("Summa")
        ekarivi.append("Päivämäärä")
        tiedot.append(ekarivi)
        
        for row in data: 
            rivi = []
            rivi.append(row["category"])
            rivi.append(row["amount"] )
            rivi.append(row["date"])
           # rivi = [(f'{row["category"]}        {row["amount"]}         {row["date"]}')]
            print(rivi)
            tiedot.append(rivi)
        print(tiedot)   
        # Luodaan matplotlib-kuva
        fig, ax = plt.subplots()
        ax.axis('off')  # Poista x- ja y-akselit
        ax.table(cellText=tiedot,
        colLabels=None,
        cellLoc='center',
        loc='center')

        # Tallennetaan kuva PNG-tiedostona
        plt.savefig('taulukko.png', bbox_inches='tight')
        plt.close()  # Suljetaan kuvaikkuna
        
        #lopuksi vaihdetaan seuraavalle sivulle
        self.switch_to_informationwindow()
    
#kolmas sivu, joka avautuu, jos painetaan Luo raportti-nappia
class ImageWindow(Screen):
    def __init__(self, **kw):
        super(ImageWindow, self).__init__(**kw)
        #luodaan seuraavan sivun layout
        self.layout3 = BoxLayout(orientation='vertical')

        #otsikko seuraavalle sivulle
        self.label3 = Label(text='Kuukausiraportti', size_hint=(1, 0.1))

        #luodaan image
        #tällä hetkellä näkyy vain juuri sovelluksen avaushetkellä ollut tilanne, eikä kuva päivity 
        #kun lisätään kuluja
        self.image = Image(source="report.png", size_hint=(1, 0.8))
        #luodaan button
        self.button3 = Button(text="Takaisin", on_press=self.switch_to_reportwindow, size_hint=(1, 0.1))
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kuva ja button
        self.layout3.add_widget(self.label3)
        self.layout3.add_widget(self.image)
        self.layout3.add_widget(self.button3)

        #lopuksi lisätään layout tähän reportwindowiin
        self.add_widget(self.layout3)

    def switch_to_reportwindow(self, instance):
        self.manager.current = 'reportwindow'

#neljäs sivu, joka avautuu, jos painetaan Näytä kaikki tiedot -nappia
class InformationWindow(Screen):
    def __init__(self, **kw):
        super(InformationWindow, self).__init__(**kw)
        #luodaan seuraavan sivun layout
        self.layout4 = BoxLayout(orientation='vertical')

        #otsikko seuraavalle sivulle
        self.label4 = Label(text='Kaikki tietosi', size_hint=(1, 0.1))

        #luodaan image
        #tällä hetkellä näkyy vain juuri sovelluksen avaushetkellä ollut tilanne, eikä kuva päivity 
        #kun lisätään kuluja
        self.image2 = Image(source="taulukko.png", size_hint=(1, 0.8))

        #lisätään layoutiin nämä edelliset otsikko, image
        self.layout4.add_widget(self.label4)
        self.layout4.add_widget(self.image2)

        
            
        
        #luodaan navigointibutton
        self.button4 = Button(text="Takaisin", on_press=self.switch_to_reportwindow, size_hint=(1, 0.1))
        
         #lisätään layoutiin nämä edelliset navigointibutton
        self.layout4.add_widget(self.button4)

        #lopuksi lisätään layout tähän reportwindowiin
        self.add_widget(self.layout4)

    def switch_to_reportwindow(self, instance):
        self.manager.current = 'reportwindow'

            
#Screenmanagerluokan luonti
#class WindowManager(ScreenManager):
    #pass


class MassiKamuApp(App):
    def build(self):
        # lisätään sivut screenmanageriin
        window_manager = ScreenManager(transition=FadeTransition())
        window_manager.add_widget(MainWindow(name='mainwindow'))
        window_manager.add_widget(ReportWindow(name='reportwindow'))
        window_manager.add_widget(ImageWindow(name='imagewindow'))
        window_manager.add_widget(InformationWindow(name='informationwindow'))
        return window_manager
    
    
    
