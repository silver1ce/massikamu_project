import datetime
import pymongo
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["MassiKamu"]
expenses_collection = db["expenses"]


class MassiKamuApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.category_input = TextInput(hint_text='Category')
        self.amount_input = TextInput(hint_text='Amount')
        self.add_expense_button = Button(text='Add Expense', on_press=self.add_expense)
        self.generate_report_button = Button(text='Generate Report', on_press=self.generate_report)
        self.report_label = Label(text='', size_hint=(1, 0.8))
        
        self.layout.add_widget(self.category_input)
        self.layout.add_widget(self.amount_input)
        self.layout.add_widget(self.add_expense_button)
        self.layout.add_widget(self.generate_report_button)
        self.layout.add_widget(self.report_label)
        
        return self.layout
    
    def add_expense(self, instance):
        category = self.category_input.text
        amount = float(self.amount_input.text)
        
        expense = {
            "category": category,
            "amount": amount,
            "date": datetime.datetime.now()
        }
        expenses_collection.insert_one(expense)
        
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
        result = list(expenses_collection.aggregate(pipeline))
    
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


if __name__ == '__main__':
    MassiKamuApp().run()

# Close the MongoDB connection
client.close()
