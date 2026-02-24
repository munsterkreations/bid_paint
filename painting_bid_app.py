import tkinter as tk
from tkinter import messagebox, filedialog
import json

class PaintingBidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Residential Painting Bid Calculator")
        self.root.geometry("600x800")

        # Default values from the document
        self.paint_coverage_per_gallon = 400  # sq ft per gallon
        self.waste_factor = 1.20  # 20% waste
        self.labor_rate_sqft_per_hour = 120  # sq ft per hour
        self.hourly_wage = 25.0  # example hourly wage, including benefits
        self.sundries_percentage = 0.25  # 25% for sundries
        self.overhead_percentage = 0.10  # 10% overhead
        self.profit_margin = 0.40  # 40% average of 30-50%
        self.paint_price_per_gallon = 50.0  # example price
        self.primer_price_per_gallon = 40.0  # example
        self.coats = 2  # default coats

        # Project data
        self.project = {
            "walls_sqft": 0.0,
            "ceilings_sqft": 0.0,
            "trim_length": 0.0,
            "doors_count": 0,
            "windows_count": 0,
            "challenges": "",
            "scope_included": "",
            "scope_excluded": "",
            "paint_brand": "Sherwin-Williams Emerald",
            "payment_terms": "50% deposit, 50% on completion",
            "warranty": "1-year warranty on workmanship"
        }

        # UI Frames
        self.create_input_frame()
        self.create_calculation_frame()
        self.create_proposal_frame()

    def create_input_frame(self):
        input_frame = tk.LabelFrame(self.root, text="1. Site Visit & Scope Definition")
        input_frame.pack(pady=10, padx=10, fill="x")

        # Measurements
        tk.Label(input_frame, text="Total Walls Sq Ft (after subtracting doors/windows):").grid(row=0, column=0, sticky="w")
        self.walls_sqft_entry = tk.Entry(input_frame)
        self.walls_sqft_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Total Ceilings Sq Ft:").grid(row=1, column=0, sticky="w")
        self.ceilings_sqft_entry = tk.Entry(input_frame)
        self.ceilings_sqft_entry.grid(row=1, column=1)

        tk.Label(input_frame, text="Trim Length (linear ft):").grid(row=2, column=0, sticky="w")
        self.trim_length_entry = tk.Entry(input_frame)
        self.trim_length_entry.grid(row=2, column=1)

        tk.Label(input_frame, text="Number of Doors:").grid(row=3, column=0, sticky="w")
        self.doors_count_entry = tk.Entry(input_frame)
        self.doors_count_entry.grid(row=3, column=1)

        tk.Label(input_frame, text="Number of Windows:").grid(row=4, column=0, sticky="w")
        self.windows_count_entry = tk.Entry(input_frame)
        self.windows_count_entry.grid(row=4, column=1)

        # Challenges and Scope
        tk.Label(input_frame, text="Challenges (e.g., high ceilings):").grid(row=5, column=0, sticky="w")
        self.challenges_entry = tk.Entry(input_frame, width=50)
        self.challenges_entry.grid(row=5, column=1)

        tk.Label(input_frame, text="Scope Included:").grid(row=6, column=0, sticky="w")
        self.scope_included_entry = tk.Entry(input_frame, width=50)
        self.scope_included_entry.grid(row=6, column=1)

        tk.Label(input_frame, text="Scope Excluded:").grid(row=7, column=0, sticky="w")
        self.scope_excluded_entry = tk.Entry(input_frame, width=50)
        self.scope_excluded_entry.grid(row=7, column=1)

        # Defaults
        tk.Label(input_frame, text="Paint Brand:").grid(row=8, column=0, sticky="w")
        self.paint_brand_entry = tk.Entry(input_frame)
        self.paint_brand_entry.insert(0, self.project["paint_brand"])
        self.paint_brand_entry.grid(row=8, column=1)

        tk.Label(input_frame, text="Number of Coats:").grid(row=9, column=0, sticky="w")
        self.coats_entry = tk.Entry(input_frame)
        self.coats_entry.insert(0, str(self.coats))
        self.coats_entry.grid(row=9, column=1)

    def create_calculation_frame(self):
        calc_frame = tk.LabelFrame(self.root, text="2-3. Calculate Costs & Apply Markup")
        calc_frame.pack(pady=10, padx=10, fill="x")

        # Rates
        tk.Label(calc_frame, text="Paint Price per Gallon:").grid(row=0, column=0, sticky="w")
        self.paint_price_entry = tk.Entry(calc_frame)
        self.paint_price_entry.insert(0, str(self.paint_price_per_gallon))
        self.paint_price_entry.grid(row=0, column=1)

        tk.Label(calc_frame, text="Primer Price per Gallon:").grid(row=1, column=0, sticky="w")
        self.primer_price_entry = tk.Entry(calc_frame)
        self.primer_price_entry.insert(0, str(self.primer_price_per_gallon))
        self.primer_price_entry.grid(row=1, column=1)

        tk.Label(calc_frame, text="Labor Rate (sq ft/hour):").grid(row=2, column=0, sticky="w")
        self.labor_rate_entry = tk.Entry(calc_frame)
        self.labor_rate_entry.insert(0, str(self.labor_rate_sqft_per_hour))
        self.labor_rate_entry.grid(row=2, column=1)

        tk.Label(calc_frame, text="Hourly Wage (incl. benefits):").grid(row=3, column=0, sticky="w")
        self.hourly_wage_entry = tk.Entry(calc_frame)
        self.hourly_wage_entry.insert(0, str(self.hourly_wage))
        self.hourly_wage_entry.grid(row=3, column=1)

        tk.Label(calc_frame, text="Overhead %:").grid(row=4, column=0, sticky="w")
        self.overhead_entry = tk.Entry(calc_frame)
        self.overhead_entry.insert(0, str(self.overhead_percentage * 100))
        self.overhead_entry.grid(row=4, column=1)

        tk.Label(calc_frame, text="Profit Margin %:").grid(row=5, column=0, sticky="w")
        self.profit_entry = tk.Entry(calc_frame)
        self.profit_entry.insert(0, str(self.profit_margin * 100))
        self.profit_entry.grid(row=5, column=1)

        # Calculate Button
        calc_button = tk.Button(calc_frame, text="Calculate Bid", command=self.calculate_bid)
        calc_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Results
        self.results_text = tk.Text(calc_frame, height=10, width=50)
        self.results_text.grid(row=7, column=0, columnspan=2)

    def create_proposal_frame(self):
        proposal_frame = tk.LabelFrame(self.root, text="4. Create Professional Proposal")
        proposal_frame.pack(pady=10, padx=10, fill="x")

        tk.Label(proposal_frame, text="Payment Terms:").grid(row=0, column=0, sticky="w")
        self.payment_terms_entry = tk.Entry(proposal_frame, width=50)
        self.payment_terms_entry.insert(0, self.project["payment_terms"])
        self.payment_terms_entry.grid(row=0, column=1)

        tk.Label(proposal_frame, text="Warranty:").grid(row=1, column=0, sticky="w")
        self.warranty_entry = tk.Entry(proposal_frame, width=50)
        self.warranty_entry.insert(0, self.project["warranty"])
        self.warranty_entry.grid(row=1, column=1)

        generate_button = tk.Button(proposal_frame, text="Generate Proposal", command=self.generate_proposal)
        generate_button.grid(row=2, column=0, columnspan=2, pady=10)

        save_button = tk.Button(proposal_frame, text="Save Project Data", command=self.save_project)
        save_button.grid(row=3, column=0, pady=5)

        load_button = tk.Button(proposal_frame, text="Load Project Data", command=self.load_project)
        load_button.grid(row=3, column=1, pady=5)

    def calculate_bid(self):
        try:
            # Gather inputs
            self.project["walls_sqft"] = float(self.walls_sqft_entry.get() or 0)
            self.project["ceilings_sqft"] = float(self.ceilings_sqft_entry.get() or 0)
            self.project["trim_length"] = float(self.trim_length_entry.get() or 0)
            self.project["doors_count"] = int(self.doors_count_entry.get() or 0)
            self.project["windows_count"] = int(self.windows_count_entry.get() or 0)
            self.project["challenges"] = self.challenges_entry.get()
            self.project["scope_included"] = self.scope_included_entry.get()
            self.project["scope_excluded"] = self.scope_excluded_entry.get()
            self.project["paint_brand"] = self.paint_brand_entry.get()

            self.coats = int(self.coats_entry.get() or 2)
            self.paint_price_per_gallon = float(self.paint_price_entry.get())
            self.primer_price_per_gallon = float(self.primer_price_entry.get())
            self.labor_rate_sqft_per_hour = float(self.labor_rate_entry.get())
            self.hourly_wage = float(self.hourly_wage_entry.get())
            self.overhead_percentage = float(self.overhead_entry.get()) / 100
            self.profit_margin = float(self.profit_entry.get()) / 100

            # Total paintable area (walls + ceilings, assuming trim separate)
            total_sqft = self.project["walls_sqft"] + self.project["ceilings_sqft"]

            # Materials: Paint and Primer (assuming 1 coat primer)
            paint_gallons = (total_sqft * self.coats / self.paint_coverage_per_gallon) * self.waste_factor
            primer_gallons = (total_sqft / self.paint_coverage_per_gallon) * self.waste_factor  # 1 coat primer
            materials_cost = (paint_gallons * self.paint_price_per_gallon) + (primer_gallons * self.primer_price_per_gallon)
            sundries_cost = materials_cost * self.sundries_percentage
            total_materials = materials_cost + sundries_cost

            # Labor: For painting area + extras for doors/windows/trim
            hours_for_area = total_sqft / self.labor_rate_sqft_per_hour
            hours_for_doors = self.project["doors_count"] * 0.5  # example 0.5 hours per door
            hours_for_windows = self.project["windows_count"] * 0.3  # example 0.3 hours per window
            hours_for_trim = self.project["trim_length"] / 50  # example 50 ft per hour
            total_hours = hours_for_area + hours_for_doors + hours_for_windows + hours_for_trim
            labor_cost = total_hours * self.hourly_wage

            # Overhead
            subtotal = total_materials + labor_cost
            overhead = subtotal * self.overhead_percentage

            # Total Cost
            total_cost = subtotal + overhead

            # Bid Price with Profit
            bid_price = total_cost * (1 + self.profit_margin)

            # Display Results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Materials Cost: ${total_materials:.2f}\n")
            self.results_text.insert(tk.END, f"Labor Cost: ${labor_cost:.2f} ({total_hours:.2f} hours)\n")
            self.results_text.insert(tk.END, f"Overhead: ${overhead:.2f}\n")
            self.results_text.insert(tk.END, f"Total Cost: ${total_cost:.2f}\n")
            self.results_text.insert(tk.END, f"Bid Price (with {self.profit_margin*100}% margin): ${bid_price:.2f}\n")

            self.project["bid_price"] = bid_price
            self.project["total_cost"] = total_cost
            self.project["labor_cost"] = labor_cost
            self.project["materials_cost"] = total_materials
            self.project["overhead"] = overhead
            self.project["total_hours"] = total_hours

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")

    def generate_proposal(self):
        if "bid_price" not in self.project:
            messagebox.showwarning("Warning", "Please calculate the bid first.")
            return

        self.project["payment_terms"] = self.payment_terms_entry.get()
        self.project["warranty"] = self.warranty_entry.get()

        proposal = f"""
Professional Painting Proposal

Scope of Work:
Included: {self.project["scope_included"]}
Excluded: {self.project["scope_excluded"]}
Challenges Noted: {self.project["challenges"]}

Details:
- Painting {self.project["walls_sqft"]:.2f} sq ft walls and {self.project["ceilings_sqft"]:.2f} sq ft ceilings with {self.coats} coats of {self.project["paint_brand"]}.
- {self.project["trim_length"]:.2f} linear ft of trim.
- {self.project["doors_count"]} doors and {self.project["windows_count"]} windows.

Total Bid Price: ${self.project["bid_price"]:.2f}

Payment Terms: {self.project["payment_terms"]}
Warranty: {self.project["warranty"]}
Value: We use high-quality materials and provide professional experience.

Thank you for considering us!
"""

        proposal_window = tk.Toplevel(self.root)
        proposal_window.title("Generated Proposal")
        text = tk.Text(proposal_window, wrap="word", width=60, height=20)
        text.insert(tk.END, proposal)
        text.pack(pady=10, padx=10)

        save_button = tk.Button(proposal_window, text="Save Proposal to File", command=lambda: self.save_proposal(proposal))
        save_button.pack(pady=10)

    def save_proposal(self, proposal):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(proposal)
            messagebox.showinfo("Success", "Proposal saved successfully.")

    def save_project(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.project, f)
            messagebox.showinfo("Success", "Project data saved successfully.")

    def load_project(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                self.project = json.load(f)
            # Update UI
            self.walls_sqft_entry.delete(0, tk.END)
            self.walls_sqft_entry.insert(0, str(self.project.get("walls_sqft", 0)))
            self.ceilings_sqft_entry.delete(0, tk.END)
            self.ceilings_sqft_entry.insert(0, str(self.project.get("ceilings_sqft", 0)))
            self.trim_length_entry.delete(0, tk.END)
            self.trim_length_entry.insert(0, str(self.project.get("trim_length", 0)))
            self.doors_count_entry.delete(0, tk.END)
            self.doors_count_entry.insert(0, str(self.project.get("doors_count", 0)))
            self.windows_count_entry.delete(0, tk.END)
            self.windows_count_entry.insert(0, str(self.project.get("windows_count", 0)))
            self.challenges_entry.delete(0, tk.END)
            self.challenges_entry.insert(0, self.project.get("challenges", ""))
            self.scope_included_entry.delete(0, tk.END)
            self.scope_included_entry.insert(0, self.project.get("scope_included", ""))
            self.scope_excluded_entry.delete(0, tk.END)
            self.scope_excluded_entry.insert(0, self.project.get("scope_excluded", ""))
            self.paint_brand_entry.delete(0, tk.END)
            self.paint_brand_entry.insert(0, self.project.get("paint_brand", ""))
            self.payment_terms_entry.delete(0, tk.END)
            self.payment_terms_entry.insert(0, self.project.get("payment_terms", ""))
            self.warranty_entry.delete(0, tk.END)
            self.warranty_entry.insert(0, self.project.get("warranty", ""))
            messagebox.showinfo("Success", "Project data loaded successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintingBidApp(root)
    root.mainloop()
