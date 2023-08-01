import datetime
import matplotlib.pyplot as plt
import tietokanta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

class MainWindow(Screen, BoxLayout):
    def __init__(self, **kw):
        super(MainWindow, self).__init__(**kw)
        self.layout = BoxLayout(orientation='vertical')
        
        self.category_input = TextInput(hint_text='Category')
        self.amount_input = TextInput(hint_text='Amount')
        self.add_expense_button = Button(text='Add Expense', on_press=self.add_expense)
        self.remove_expense_button = Button(text='Remove Expense', on_press=self.remove_expense)
        self.generate_report_button = Button(text='Generate Report', on_press=self.generate_report)
        self.report_label = Label(text='', size_hint=(1, 0.8))
        
        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(self.add_expense_button)
        self.layout.add_widget(self.remove_expense_button)
        self.layout.add_widget(self.generate_report_button)
        self.layout.add_widget(self.report_label)

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

#yritys tehdä poistamisominaisuus, ei toimi vielä. Täytyy tarkastaa, miten sieltä poistettiinkaan
    def remove_expense(self, instance):
        category = self.category_input.text
        amount = float(self.amount_input.text)
        
        expense = {
            "category": category,
            "amount": amount
        }
        tietokanta.expense_collection.remove(expense)
        
        self.category_input.text = ''
        self.amount_input.text = ''
    
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
        plt.xlabel('Category')
        plt.ylabel('Amount')
        plt.title('Monthly Expense Report')
        plt.xticks(rotation='vertical')
        plt.tight_layout()
        plt.savefig('report.png')  # Save the chart as an image
        plt.close()  # Close the figure
        
        self.report_label.text = 'Monthly Expense Report'
        self.report_label.canvas.ask_update()  # Update the label to show the new text
        self.report_label.canvas.load_image('report.png')  # Load and display the chart image

class ReportWindow(Screen):
    def __init__(self, **kw):
        super(ReportWindow, self).__init__(**kw)
        self.button = Button(text="go")
   


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)
        # self.screen_manager = ScreenManager()

        # self.mainWindow = MainWindow()
        # screen = Screen(name='MainWindow')
        # screen.add_widget(self.mainWindow)
        # self.screen_manager.add_widget(screen)

        # self.reportWindow = ReportWindow()
        # screen = Screen(name='Report')
        # screen.add_widget(self.reportWindow)
        # self.screen_manager.add_widget(screen)

       


#yritettiin käyttää screenmanageria ja saada uusi sivu käyttöön. ei toimi vielä, näyttää vain mustaa ruutua


class MassiKamuApp(App):
    def build(self):
        screen_manager = WindowManager(transition=FadeTransition())
        screen_manager.add_widget(MainWindow(name='mainwindow'))
        screen_manager.add_widget(ReportWindow(name='report'))
       
        return screen_manager
    
   
    
