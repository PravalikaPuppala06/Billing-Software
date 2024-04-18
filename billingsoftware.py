import tkinter as tk
from tkinter import messagebox
import csv

class BillingSoftware:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")
        self.setup_ui()
        self.item_details = []
        self.bill_number = 1  # Initialize bill number

    def setup_ui(self):
        # heading
        heading_label = tk.Label(self.root, text="Billing Software", font=("Arial", 24, "bold"), fg="blue")
        heading_label.grid(row=0, column=0, columnspan=10, pady=(20, 10))

        # Firm Details heading
        firm_label = tk.Label(self.root, text="Firm Details", font=("Arial", 16, "bold"))
        firm_label.grid(row=1, column=0, columnspan=10)

        # Labels for firm fields
        firm_labels = ["Firm Name", "Address", "Contact"]
        for i, label_text in enumerate(firm_labels):
            tk.Label(self.root, text=label_text).grid(row=i + 2, column=0, padx=5, pady=5, sticky='w')

        # Entry fields for firm fields
        self.firm_name_entry = tk.Entry(self.root)
        self.firm_name_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        self.contact_entry = tk.Entry(self.root)
        self.contact_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Customer Details heading
        customer_label = tk.Label(self.root, text="Customer Details", font=("Arial", 16, "bold"))
        customer_label.grid(row=5, column=0, columnspan=10)

        # Labels for customer fields
        customer_labels = ["Customer Name", "Phone Number", "Bill Number"]
        for i, label_text in enumerate(customer_labels):
            tk.Label(self.root, text=label_text).grid(row=i + 6, column=0, padx=5, pady=5, sticky='w')

        # Entry fields for customer fields
        self.customer_name_entry = tk.Entry(self.root)
        self.customer_name_entry.grid(row=6, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        self.phone_number_entry = tk.Entry(self.root)
        self.phone_number_entry.grid(row=7, column=1, columnspan=3, padx=5, pady=5, sticky='ew')
        self.bill_number_entry = tk.Entry(self.root)
        self.bill_number_entry.grid(row=8, column=1, columnspan=3, padx=5, pady=5, sticky="ew")

        # Item Details heading
        item_label = tk.Label(self.root, text="Item Details", font=("Arial", 16, "bold"))
        item_label.grid(row=9, column=0, columnspan=10)

        # Labels for item details fields
        labels = ["Sr. No", "Item/Participates", "Item Code", "Quantity", "Price", "Taxes",
                  "Total without Taxes", "Bill Total (with GST)"]
        for i, label_text in enumerate(labels):
            tk.Label(self.root, text=label_text).grid(row=10, column=i, padx=5, pady=5)

        # Entry fields for item details fields
        self.entry_fields = {}
        for i in range(len(labels)):
            self.entry_fields[i] = tk.Entry(self.root)
            self.entry_fields[i].grid(row=11, column=i, padx=5, pady=5)

            # Make Total without Taxes and Bill Total entry fields read-only
            if i in (6, 7):
                self.entry_fields[i].config(state='readonly')

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=12, column=0, columnspan=10, pady=10)

        self.calculate_total_button = tk.Button(button_frame, text="Calculate Total", command=self.calculate_total)
        self.calculate_total_button.pack(side="left", padx=10)

        self.add_item_button = tk.Button(button_frame, text="Add Item", command=self.add_item)
        self.add_item_button.pack(side="left", padx=10)

        self.generate_bill_button = tk.Button(button_frame, text="Generate Bill", command=self.generate_bill)
        self.generate_bill_button.pack(side="left", padx=10)

        self.print_button = tk.Button(button_frame, text="Print", command=self.print_details)
        self.print_button.pack(side="left", padx=10)

    def calculate_total(self):
        if self.check_fields_filled():
            try:
                total_without_taxes = float(self.entry_fields[4].get()) * float(self.entry_fields[3].get())
                total_taxes = float(self.entry_fields[5].get())
                bill_total = total_without_taxes + total_taxes

                self.entry_fields[6].config(state='normal')  # Enable Total without Taxes field
                self.entry_fields[6].delete(0, tk.END)
                self.entry_fields[6].insert(tk.END, str(total_without_taxes))
                self.entry_fields[6].config(state='readonly')  # Make Total without Taxes field read-only again

                self.entry_fields[7].config(state='normal')  # Enable Bill Total field
                self.entry_fields[7].delete(0, tk.END)
                self.entry_fields[7].insert(tk.END, str(bill_total))
                self.entry_fields[7].config(state='readonly')  # Make Bill Total field read-only again
            except ValueError:
                messagebox.showerror("Error", "Please fill the required fields.")

    def add_item(self):
        if self.check_fields_filled():
            item_detail = [field.get() for field in self.entry_fields.values()]
            self.item_details.append(item_detail)
            messagebox.showinfo("Success", "Item details added successfully. Enter another item.")

            # For Store customer details
            self.customer_details = {
                "Customer Name": self.customer_name_entry.get(),
                "Phone Number": self.phone_number_entry.get(),
                "Bill Number": self.bill_number_entry.get()
            }

            # For Store firm details
            self.firm_details = {
                "Firm Name": self.firm_name_entry.get(),
                "Address": self.address_entry.get(),
                "Contact": self.contact_entry.get()
            }

            # Clear all entry fields
            for field in self.entry_fields.values():
                field.delete(0, tk.END)

            # Clear customer details fields
            self.customer_name_entry.delete(0, tk.END)
            self.phone_number_entry.delete(0, tk.END)
            self.bill_number_entry.delete(0, tk.END)

            # Clear firm details fields
            self.firm_name_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.contact_entry.delete(0, tk.END)

            # Clear total without taxes and bill total fields
            for field in (self.entry_fields[6], self.entry_fields[7]):
                field.config(state='normal')
                field.delete(0, tk.END)
                field.config(state='readonly')

    def generate_bill(self):
        if self.item_details:
            # Prepare bill information
            bill_info = (
                f"Firm Details:\n"
                f"Firm Name: {self.firm_details['Firm Name']}\n"
                f"Address: {self.firm_details['Address']}\n"
                f"Contact: {self.firm_details['Contact']}\n\n"
                f"Customer Details:\n"
                f"Customer Name: {self.customer_details['Customer Name']}\n"
                f"Phone Number: {self.customer_details['Phone Number']}\n"
                f"Bill Number: {self.customer_details['Bill Number']}\n\n"
                "Item Details:\n"
            )
            for item in self.item_details:
                bill_info += f"Item/Participates: {item[1]}, Quantity: {item[3]}, Price: {item[4]}, Taxes: {item[5]}, Total without Taxes: {item[6]}, Bill Total (with GST): {item[7]}\n"

            # Show bill information
            messagebox.showinfo("Bill Information", bill_info)

            # Write to daily sales report CSV file
            with open("daily_sales_report.csv", mode="a", newline="") as file:
                writer = csv.writer(file)

                # Write header if file is empty
                if file.tell() == 0:
                    header = ["Firm Name", "Address", "Contact",
                              "Customer Name", "Phone Number", "Bill Number",
                              "Item/Participates", "Item Code", "Quantity",
                              "Price", "Taxes", "Total without Taxes", "Bill Total (with GST)"]
                    writer.writerow(header)

                # Write firm details, customer details, and item details to CSV
                for item in self.item_details:
                    row = [self.firm_details["Firm Name"],
                           self.firm_details["Address"],
                           self.firm_details["Contact"],
                           self.customer_details["Customer Name"],
                           self.customer_details["Phone Number"],
                           self.customer_details["Bill Number"]] + item
                    writer.writerow(row)
        else:
            messagebox.showwarning("No Items", "No item details to generate bill.")

    def print_details(self):
        if self.item_details:
            # Prepare Print information
            print_info = (
                f"Firm Details:\n"
                f"Firm Name: {self.firm_details['Firm Name']}\n"
                f"Address: {self.firm_details['Address']}\n"
                f"Contact: {self.firm_details['Contact']}\n\n"
                f"Customer Details:\n"
                f"Customer Name: {self.customer_details['Customer Name']}\n"
                f"Phone Number: {self.customer_details['Phone Number']}\n"
                f"Bill Number: {self.customer_details['Bill Number']}\n\n"
                "Item Details:\n"
            )
            for item in self.item_details:
                print_info += f"Item/Participates: {item[1]}, Quantity: {item[3]}, Price: {item[4]}, Taxes: {item[5]}, Total without Taxes: {item[6]}, Bill Total (with GST): {item[7]}\n"

            # Show Print information
            messagebox.showinfo("Print Details", print_info)

            # Write to daily sales report CSV file
            with open("daily_sales_report.csv", mode="a", newline="") as file:
                writer = csv.writer(file)

                # Write header if file is empty
                if file.tell() == 0:
                    header = ["Firm Name", "Address", "Contact",
                              "Customer Name", "Phone Number", "Bill Number",
                              "Item/Participates", "Item Code", "Quantity",
                              "Price", "Taxes", "Total without Taxes", "Bill Total (with GST)"]
                    writer.writerow(header)

                # Write firm details, customer details, and item details to CSV
                for item in self.item_details:
                    row = [self.firm_details["Firm Name"],
                           self.firm_details["Address"],
                           self.firm_details["Contact"],
                           self.customer_details["Customer Name"],
                           self.customer_details["Phone Number"],
                           self.customer_details["Bill Number"]] + item
                    writer.writerow(row)
        else:
            messagebox.showwarning("No Items", "No item details to print.")

    def check_fields_filled(self):
        # Check if any required field is empty
        required_fields = (
            (self.firm_name_entry, "Firm Name"),
            (self.address_entry, "Address"),
            (self.contact_entry, "Contact"),
            (self.customer_name_entry, "Customer Name"),
            (self.phone_number_entry, "Phone Number"),
            (self.bill_number_entry, "Bill Number")
        )
        for field, field_name in required_fields:
            if not field.get():
                messagebox.showerror("Error", f"Please fill the {field_name} field.")
                return False

        # Check if firm name field contains alphabets
        firm_name = self.firm_name_entry.get()
        if not firm_name.isalpha():
            messagebox.showerror("Error", "Firm Name field should contain only alphabets.")
            return False

        # Check if contact field contains exactly 10 digits
        firm_contact = self.contact_entry.get()
        if not firm_contact.isdigit() or len(firm_contact) != 10:
            messagebox.showerror("Error", "Contact field should contain only 10 digits.")
            return False

        # Check if customer name field contains alphabets
        customer_name = self.customer_name_entry.get()
        if not customer_name.isalpha():
            messagebox.showerror("Error", "Customer name field should contain only alphabets.")
            return False

        # Check if phone number field contains 10 digits
        customer_contact = self.phone_number_entry.get()
        if not customer_contact.isdigit() or len(customer_contact) != 10:
            messagebox.showerror("Error", "Phone number field should contain 10 digits.")
            return False

        # Check if item details fields are filled and contain only numeric or decimal values
        item_fields = [self.entry_fields[i].get() for i in range(1, 6)]  # Get values from item details fields
        for field_value in item_fields:
            if not field_value:
                messagebox.showerror("Error", "Please fill all the fields in Item Details.")
                return False
            try:
                float(field_value)  # Check if the value can be converted to float
            except ValueError:
                messagebox.showerror("Error", "Item Details fields should contain only numeric or decimal values.")
                return False

        return True

def main():
    root = tk.Tk()
    app = BillingSoftware(root)
    root.mainloop()

if __name__ == "__main__":
    main()
