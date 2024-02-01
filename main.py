import pickle
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
import csv

# Using 'width' as an alternative to 'inch'
width = 1.5 * 72  # 1.5 inches in points (72 points per inch)

class MoneyTracker:
    def __init__(self):
        self.balance = 0
        self.transactions = []
        self.load_data()

    def add_income(self, amount, description, category):
        self.balance += amount
        self.transactions.append((datetime.now(), amount, description, category, 'Income', self.balance))
        print(f"Income of ₹{amount} added. New balance: ₹{self.balance}")
        self.save_data()

    def add_expense(self, amount, description, category):
        if amount > self.balance:
            print("Error: Insufficient funds.")
        else:
            self.balance -= amount
            self.transactions.append((datetime.now(), amount, description, category, 'Expense', self.balance))
            print(f"Expense of ₹{amount} added. New balance: ₹{self.balance}")
            self.save_data()

    def view_transactions(self):
        print("\n--- Transactions ---")
        categories = set()
        for trans in self.transactions:
            date, amount, description, category, trans_type, balance = trans
            print(f"{trans_type} - {date.strftime('%Y-%m-%d %H:%M:%S')}: ₹{amount} - {description} ({category}) - Balance: ₹{balance}")
            categories.add(category)

        print("\n--- Categories ---")
        for category in categories:
            category_total = sum(trans[1] for trans in self.transactions if trans[3] == category)
            print(f"{category}: ₹{category_total}")

        print(f"\nCurrent Balance: ₹{self.balance}")
        print("--------------------\n")

    def save_data(self):
        with open('money_tracker_data.pkl', 'wb') as file:
            pickle.dump((self.balance, self.transactions), file)

    def load_data(self):
        try:
            with open('money_tracker_data.pkl', 'rb') as file:
                self.balance, self.transactions = pickle.load(file)
        except FileNotFoundError:
            pass

    def export_to_csv(self, csv_filename='transaction_history.csv'):
        with open(csv_filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Date/Time', 'Amount', 'Description', 'Category', 'Type', 'Available Balance'])

            for trans in self.transactions:
                csv_writer.writerow(trans[1:])  # Exclude the ID

        print(f"Transaction history exported to CSV: {csv_filename}")

    def export_to_pdf(self, pdf_filename='money_tracker.pdf'):
        try:
            doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

            # Table data
            table_data = [['Date/Time', 'Transaction', 'Category', 'Available Balance', 'Description']]
            for trans in self.transactions:
                date, amount, description, category, trans_type, balance = trans
                if trans_type == 'Income':
                    color = colors.green
                elif trans_type == 'Expense':
                    color = colors.red
                else:
                    color = colors.black

                table_data.append([date.strftime('%Y-%m-%d %H:%M:%S'), f"₹{amount}", category, f"₹{balance}", description])

            # Create table
            table = Table(table_data, colWidths=[width * 1, width * 0.7, width * 0.6, width * 1 , width * 0.8], hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), color),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            # Build PDF document
            elements = [table]
            doc.build(elements)

            print(f"Data exported to {pdf_filename}")
        except Exception as e:
            print(f"Error exporting to PDF: {e}")


def main():
    tracker = MoneyTracker()

    while True:
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. Export to CSV")
        print("5. Export to PDF")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            amount = float(input("Enter income amount: "))
            description = input("Enter income description: ")
            category = input("Enter income category: ")
            tracker.add_income(amount, description, category)
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            description = input("Enter expense description: ")
            category = input("Enter expense category: ")
            tracker.add_expense(amount, description, category)
        elif choice == '3':
            tracker.view_transactions()
        elif choice == '4':
            tracker.export_to_csv()
        elif choice == '5':
            tracker.export_to_pdf()
        elif choice == '6':
            exit_choice = input("Are you sure you want to exit? (y/n): ")
            if exit_choice.lower() == 'y':
                print("Exiting money tracker. Goodbye!")
                break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
