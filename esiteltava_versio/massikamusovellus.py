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
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton 
from kivymd.uix.textfield import MDTextField

#ensimmäinen sivu, joka avautuu:
class MainWindow(MDScreen):
    def __init__(self, **kw):
        super(MainWindow, self).__init__(**kw)
        #luodaan layout pääsivulle
        
        self.layout = BoxLayout(orientation='vertical')
        
        #luodaan kategorian ja summan syöttömahdollisuudet
        self.category_input = MDTextField(hint_text='Kategoria',pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.8,0.8))
        self.amount_input = MDTextField(hint_text='Summa',pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.8,0.8))

        #luodaan buttonit, joilla voi lisätä ja poistaa tiedot 
        self.add_expense_button = MDRectangleFlatButton(text='Lisää kulu', on_press=self.add_expense, pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.8,0.8))
        self.delete_expense_button = MDRectangleFlatButton(text='Poista viimeinen kulu', on_press=self.delete_last_expense,  pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.8,0.8))

        #luodaan näytä-button
        self.show_button = MDFillRoundFlatButton(text='Näytä tiedot', on_press=self.switch_to_reportwindow,  pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(1, 0.3))
       # self.remove_expense_button = Button(text='Remove Expense', on_press=self.remove_expense)
       
        #lisätään otsikko
        self.report_label = MDLabel(text='MASSIKAMU', size_hint=(1, 0.8),halign='center', theme_text_color= "Custom", text_color=( 0, 0, 1, 1),font_style='H2', font_size='48sp')
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kategorian ja summan syöttö, ja buttonit
        self.layout.add_widget(self.report_label)

        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(self.add_expense_button)
        self.layout.add_widget(self.delete_expense_button)
        #self.layout.add_widget(self.remove_expense_button)
        self.layout.add_widget(self.show_button)
        
        #lopuksi lisätään layout tähän mainwindowiin
        self.add_widget(self.layout)

    #yritys popupin tekoon, ei onnistunut vielä
    # def open_popup(self, instance):
    #     #lisätään popup-ikkuna, joka kertoo, että ei saatu yhteyttä tietokantaan
    #             lisattyPopup = Popup(title="Ei saatu yhteyttä tietokantaan...", 
    #             content=Label(text="Tarkista internetyhteytesi."), 
    #             size_hint=(0.7, 0.2))
    #             lisattyPopup.open()

    def add_expense(self, instance):

        #jos käyttäjä ei kirjoita mitään, ja yrittää painaa Lisää kulu-nappia,
        #mitään ei tapahdu
        if len(self.category_input.text) == 0:
            print("ei mitään.")
        #jos sen sijaan käyttäjä kirjoittaa jotakin kategoriakohtaan, kokeillaan 
        #seuraavaksi, onhan käyttäjä syöttänyt Summa-kohtaan jonkin luvun, joka on
        #muunnettavissa floatiksi. jos tämäkin onnistuu, tiedot lisätään tietokantaan
        #päivämäärä- ja aikatietojen kera
        elif len(self.category_input.text) > 0:
            category = self.category_input.text
            
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
    
    def delete_last_expense(self, instance):
        #tämä funktio vain kysyy varmistuksen poistolle. Popup widgettiin
        #ei saanut lisättyä kuin yhden buttonin, niin laitoin vain kylläbuttonin
        #tämä pitäisi korjata tulevaisuudessa
        self.varmistusPopup = Popup(title="Oletko varma, että haluat poistaa tämän?",  
        size_hint=(0.7, 0.2))
        kyllaButton = Button(text="Kyllä", on_press=self.delete_from_Mongo)
       # eiButton = Button(text="Ei", on_press=poisto1Popup.dismiss)
        self.varmistusPopup.add_widget(kyllaButton)
        #poisto1Popup.add_widget(eiButton)
        self.varmistusPopup.open()

    def delete_from_Mongo(self,instance):
        #jos käyttäjä on varmistanut poiston, tämä funktio poistaa tiedon tietokannasta
        #suljetaan varmistuspopup
        self.varmistusPopup.dismiss()
        #etsii viimeisen kulun ja sen id-numeron
        viimeinen = tietokanta.expense_collection.find_one(sort=[('_id', -1)])
        viimeinen_id = viimeinen['_id']
        #poistetaan tietokannasta viimeinen kulu
        tietokanta.expense_collection.delete_one({'_id': viimeinen_id})
        #lisätään popup-ikkuna, joka kertoo, että tiedot on poistettu onnistuneesti
        poistoPopup = Popup(title="Onnistui!", 
        content=Label(text="Viimeinen kulu on nyt poistettu."), 
        size_hint=(0.7, 0.2))
        
        poistoPopup.open()


    def switch_to_reportwindow(self, instance):
        self.manager.current = 'reportwindow'

#Toinen sivu, joka avautuu, jos painetaan Näytä tiedot -nappia:
class ReportWindow(Screen):
    def __init__(self, **kw):
        super(ReportWindow, self).__init__(**kw)
        #luodaan seuraavan sivun layout
        self.layout2 = BoxLayout(orientation='vertical')

        #otsikko seuraavalle sivulle
        self.label2 = MDLabel(text='Massikamutietosi', size_hint=(1, 0.1), halign='center', theme_text_color= "Custom", text_color=( 0, 0, 1, 1))

        
        #luodaan toimintobuttonit
        self.all_the_information_button = MDRectangleFlatButton(text="Taulukko", on_press=self.generate_information, pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.5,0.5))

        self.generate_report_button = MDRectangleFlatButton(text='Diagrammi', on_press=self.generate_report,pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(0.5,0.5))
        
        
        #luodaan navigointibutton
        self.button2 = MDFillRoundFlatButton(text="Takaisin etusivulle", on_press=self.switch_to_mainwindow,pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint=(1, 0.1))

        
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
    
    def current_month_in_Finnish(self):
        #tarkastetaan, mikä kuukausi nyt on, ja käännetään sanakirjan avulla se suomeksi
        current_date = datetime.date.today()
        current_month = current_date.strftime("%B")
        kuukaudet_suomeksi =  {"January" : "tammikuu", "February":"Helmikuu", "March": "Maaliskuu", "Abril":"Huhtikuu", "May": "Toukokuu", "June":"Kesäkuu", "July":"Heinäkuu", "August" : "Elokuu", "September": "Syyskuu", "October":"Lokakuu", "November":"Marraskuu", "December":"Joulukuu"}
        kuukausi = kuukaudet_suomeksi[current_month]
        return kuukausi
    
    def query_this_month(self):
        
        # käynnissä olevan kuukauden tiedot
        current_date = datetime.datetime.today()
        first_day_of_month = datetime.datetime(current_date.year, current_date.month, 1)
        #haetaan tietokannasta vain tämän kuukauden tiedot
        query = {"date": {"$gte": first_day_of_month, "$lte": current_date}}
        kuukausi = tietokanta.expense_collection.find(query)
        return kuukausi

    def total_costs(self):
        # käynnissä olevan kuukauden kulut 
        kuukausi = ReportWindow.query_this_month(self)
        yhteensa = 0
        for row in kuukausi:
            #print(row)
            yhteensa += float(row["amount"])
        return yhteensa
            
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
        lista = []

        for row in result:
            rivi = []
            rivi.append(row["_id"])
            rivi.append(row["total_amount"])
            lista.append(rivi)

        #järjestetään tiedot aakkosjärjestykseen
        lista = sorted(lista)

        for row in lista:
            categories.append(row[0])
            amounts.append(row[1])

        # Generate bar chart
        plt.bar(categories, amounts)
        plt.xlabel('Kategoria')
        plt.ylabel('Summa')
        plt.title(self.current_month_in_Finnish() + " yhteensä: " + str(self.total_costs()) + " euroa" )
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
        #luodaan lista kaikista tämän kuun tiedoista
        kuukausi = self.query_this_month()
        data = tietokanta.expense_collection.find()
        tiedot = []
        ekarivi = []
        ekarivi.append("Kategoria")
        ekarivi.append("Summa")
        ekarivi.append("Päivämäärä")
        tiedot.append(ekarivi)
        
        for row in kuukausi: 
            rivi = []
            rivi.append(row["category"])
            rivi.append(row["amount"] )
            rivi.append(row["date"])
            tiedot.append(rivi)
        #kulut aakkosjärjestykseen
        tiedot = sorted(tiedot)
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
        self.label3 = MDLabel(text='Kuukausiraportti', size_hint=(1, 0.1), halign='center', theme_text_color= "Custom", text_color=( 0, 0, 1, 1))

        #luodaan image
        #tällä hetkellä näkyy vain juuri sovelluksen avaushetkellä ollut tilanne, eikä kuva päivity 
        #kun lisätään kuluja
        
        self.image = Image(source="report.png", size_hint=(1, 1))
        
        #luodaan button
        self.button3 = MDFillRoundFlatButton(text="Takaisin", on_press=self.switch_to_reportwindow, size_hint=(1, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})
       
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
        kuukausi = ReportWindow.current_month_in_Finnish(self)
        kulut_yhteensa = ReportWindow.total_costs(self)
        #otsikko seuraavalle sivulle
        self.label4 = MDLabel(text= kuukausi +"n kaikki kulut yhteensä: " + str(kulut_yhteensa) + " euroa", size_hint=(1, 0.1), halign='center')

        #luodaan image
        #tällä hetkellä näkyy vain juuri sovelluksen avaushetkellä ollut tilanne, eikä kuva päivity 
        #kun lisätään kuluja
        self.image2 = Image(source="taulukko.png", size_hint=(1, 1))

        #lisätään layoutiin nämä edelliset otsikko, image
        self.layout4.add_widget(self.label4)
        self.layout4.add_widget(self.image2)

        
            
        
        #luodaan navigointibutton
        self.button4 = MDFillRoundFlatButton(text="Takaisin", on_press=self.switch_to_reportwindow, size_hint=(1, 0.1), pos_hint={"center_x": 0.5, "center_y": 0.5})

         #lisätään layoutiin nämä edelliset navigointibutton
        self.layout4.add_widget(self.button4)

        #lopuksi lisätään layout tähän reportwindowiin
        self.add_widget(self.layout4)

    def switch_to_reportwindow(self, instance):
        self.manager.current = 'reportwindow'



class MassiKamuApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        # lisätään sivut screenmanageriin
        window_manager = ScreenManager(transition=FadeTransition())
        window_manager.add_widget(MainWindow(name='mainwindow'))
        window_manager.add_widget(ReportWindow(name='reportwindow'))
        window_manager.add_widget(ImageWindow(name='imagewindow'))
        window_manager.add_widget(InformationWindow(name='informationwindow'))
        return window_manager
    
    
    
