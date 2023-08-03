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
       # self.remove_expense_button = Button(text='Remove Expense', on_press=self.remove_expense)
        self.generate_report_button = Button(text='Luo raportti', on_press=self.generate_report)
        
        #lisätään otsikko
        self.report_label = Label(text='MASSIKAMU', size_hint=(1, 0.8))
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kategorian ja summan syöttö, ja buttonit
        self.layout.add_widget(self.report_label)

        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(self.add_expense_button)
        #self.layout.add_widget(self.remove_expense_button)
        self.layout.add_widget(self.generate_report_button)
        
        #lopuksi lisätään layout tähän mainwindowiin
        self.add_widget(self.layout)

    def add_expense(self, instance):
        category = self.category_input.text
        amount = float(self.amount_input.text)
        
        expense = {
            "category": category,
            "amount": amount,
            "date": datetime.datetime.now()
        }
        tietokanta.expense_collection.insert_one(expense)
        
        self.category_input.text = ''
        self.amount_input.text = ''

# #yritys tehdä poistamisominaisuus, ei toimi vielä. Täytyy tarkastaa, miten sieltä poistettiinkaan
#     def remove_expense(self, instance):
#         category = self.category_input.text
#         amount = float(self.amount_input.text)
        
#         expense = {
#             "category": category,
#             "amount": amount
#         }
#         tietokanta.expense_collection.remove(expense)
        
#         self.category_input.text = ''
#         self.amount_input.text = ''
 

    def generate_report(self, instance):
        laskuri = 0
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
        plt.savefig('report' + str(laskuri) + '.png')  # Save the chart as an image
        
        laskuri += 1
        print("saved")
        plt.close()  # Close the figure
        
        
        # self.report_label.text = 'Monthly Expense Report'
        # self.report_label.canvas.ask_update()  # Update the label to show the new text
        # self.report_label.canvas.load_image('report.png')  # Load and display the chart image

       # self.add_widget(Button(text="Siirry Screen 2:een", on_press=self.switch_to_screen2))

        #lopuksi vaihdetaan seuraavalle sivulle
        
        self.switch_to_reportwindow()
        
    def switch_to_reportwindow(self):
        self.manager.current = 'reportwindow'

class ReportWindow(Screen):
    def __init__(self, **kw):
        super(ReportWindow, self).__init__(**kw)
        #luodaan seuraavan sivun layout
        self.layout2 = BoxLayout(orientation='vertical')

        #otsikko seuraavalle sivulle
        self.label2 = Label(text='Kuukausiraportti', size_hint=(1, 0.2))
        
        #luodaan image
        #tällä hetkellä näkyy vain juuri sovelluksen avaushetkellä ollut tilanne, eikä kuva päivity 
        #kun lisätään kuluja
        self.image = Image(source="report.png", size_hint=(1, 0.8))
        
        #luodaan button
        self.button2 = Button(text="Takaisin etusivulle", on_press=self.switch_to_mainwindow, size_hint=(1, 0.1))
     
        
        #lisätään layoutiin nämä edelliset widgetit, eli otsikko, kuva ja button
        self.layout2.add_widget(self.label2)
        self.layout2.add_widget(self.image)
        self.layout2.add_widget(self.button2)
        
        #lopuksi lisätään layout tähän reportwindowiin
        self.add_widget(self.layout2)

        #self.layout2.add_widget(Button(text="Siirry Screen 1:een", on_press=self.switch_to_screen1))

    def switch_to_mainwindow(self, instance):
        self.manager.current = 'mainwindow'

    

class WindowManager(ScreenManager):
    pass


class MassiKamuApp(App):
    def build(self):
        # lisätään sivut screenmanageriin
        window_manager = WindowManager(transition=FadeTransition())
        window_manager.add_widget(MainWindow(name='mainwindow'))
        window_manager.add_widget(ReportWindow(name='reportwindow'))
       
        return window_manager
    
    
    
