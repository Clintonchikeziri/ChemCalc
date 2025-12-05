# region MODULE IMPORTATIONS
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from UserInterface import main_menu, eGFR_menu, eGFR_ped_menu, uacr_menu, uosm_menu, sosm_menu, ldl_menu, hdl_menu

# endregion


class ChemCalc:
    def __init__(self, root):
        self.root = root

        self.back_btn  = tb.Button(root, text="<", bootstyle="success", command=self.back_to_mainMenu)

        self.page1 = Frame(root)
        self.page2 = Frame(root)
        self.page3 = Frame(root)
        self.page4 = Frame(root)
        self.page5 = Frame(root)
        self.page6 = Frame(root)
        self.page7 = Frame(root)
        self.page8 = Frame(root)

        self.show_page(self.page1)

        self.menu_ui = main_menu(self.page1)
        self.eGFR_ui = eGFR_menu(self.page2)
        self.eGFR_ped_ui = eGFR_ped_menu(self.page3)
        self.uacr_ui = uacr_menu(self.page4)
        self.uosm_ui = uosm_menu(self.page5)
        self.ldl_ui = ldl_menu(self.page6)
        self.hdl_ui = hdl_menu(self.page7)
        self.sosm_ui = sosm_menu(self.page8)



        #ASSIGN COMMANDS TO BUTTONS
        self.menu_ui.eGFRBtn.config(command=self.show_eGFR)
        self.eGFR_ui.calcEGFRBtn.config(command=self.calculate_egfr)

        self.menu_ui.eGFR_pedBtn.config(command=self.show_eGFR_ped)
        self.eGFR_ped_ui.calcPedGFRBtn.config(command=self.calculate_pediatric_egfr)

        self.menu_ui.UACRBtn.config(command=self.show_uacr)
        self.uacr_ui.calcUACRBtn.config(command=self.calculate_urine_acr)

        self.menu_ui.uOsmBtn.config(command=self.show_uosm)
        self.uosm_ui.calcUOSMBtn.config(command=self.calculate_urine_osmolality)

        self.menu_ui.LDLBtn.config(command=self.show_ldl)
        self.ldl_ui.calcLDLBtn.config(command=self.calculate_ldl)

        self.menu_ui.HDLBtn.config(command=self.show_hdl)
        self.hdl_ui.calcHDLBtn.config(command=self.calculate_hdl_from_sampson)

        self.menu_ui.sOsmBtn.config(command=self.show_sosm)
        self.sosm_ui.calcSOSMBtn.config(command=self.calculate_serum_osmolarity)




    def show_page(self, page):
        for p in [self.page1, self.page2, self.page3, self.page4, self.page5, self.page6, self.page7, self.page8]:
            p.pack_forget()
        page.pack()
    
    def show_eGFR(self):
        self.show_page(self.page2)
        self.back_btn.place(x=10, y=10) 
      
    def show_eGFR_ped(self):
        self.show_page(self.page3)
        self.back_btn.place(x=10, y=10) 
    
    def show_uacr(self):
        self.show_page(self.page4)
        self.back_btn.place(x=10, y=10) 

    def show_uosm(self):
        self.show_page(self.page5)
        self.back_btn.place(x=10, y=10) 

    def show_sosm(self):
        self.show_page(self.page8)
        self.back_btn.place(x=10, y=10) 

    def show_ldl(self):
        self.show_page(self.page6)
        self.back_btn.place(x=10, y=10) 

    def show_hdl(self):
        self.show_page(self.page7)
        self.back_btn.place(x=10, y=10) 

    def back_to_mainMenu(self):
        self.show_page(self.page1)
        self.back_btn.place_forget()
    


    def calculate_egfr(self):
        try:
            creatinine = float(self.eGFR_ui.creatinine_var.get())
            age = float(self.eGFR_ui.age_var.get())
            height = float(self.eGFR_ui.height_var.get())
            weight = float(self.eGFR_ui.weight_var.get())

            gender = self.eGFR_ui.patient_gender.get()
            if not gender:
                Messagebox.show_warning("Please select gender.")
                return
            # CKD-EPI 2021 equation (standardized for adults)
            kappa = 0.7 if gender == "Female" else 0.9
            alpha = -0.241 if gender == "Female" else -0.302
            sex_factor = 1.012 if gender == "Female" else 1.0

            egfr = 142 * min(creatinine / kappa, 1)**alpha * max(creatinine / kappa, 1)**(-1.200) \
                * (0.9938**age) * sex_factor
            # Adjust for body surface area (optional)
            # BSA (Du Bois formula)
            bsa = 0.007184 * pow(weight, 0.425) * pow(height, 0.725)
            egfr_bsa = egfr * (bsa/1.73)

            self.eGFR_ui.result.config(text=f"EGFR: {egfr_bsa:.1f} mL/min")

            # Determine CKD stage
            if egfr_bsa >= 90:
                stage, color, msg = "G1 (Normal)", "success", "Normal kidney function."
            elif egfr_bsa >= 60:
                egfr_bsa, color, msg = "G2 (Mildly decreased)", "info", "Slightly reduced kidney function."
            elif egfr_bsa >= 45:
                stage, color, msg = "G3a (Mild–Moderate)", "warning", "Mild to moderate reduction in GFR."
            elif egfr_bsa >= 30:
                stage, color, msg = "G3b (Moderate–Severe)", "warning", "Moderate to severe kidney damage."
            elif egfr_bsa >= 15:
                stage, color, msg = "G4 (Severe)", "danger", "Severe kidney damage. Nephrology care required."
            else:
                stage, color, msg = "G5 (Kidney Failure)", "danger", "End-stage renal disease. Dialysis likely needed."

            self.eGFR_ui.interpret_text.config(text=f"{stage}\n{msg}", bootstyle=color)

        except ValueError:
            Messagebox.show_error("Please enter valid numeric values for all fields.")

    def calculate_pediatric_egfr(self):
        creatinine = float(self.eGFR_ped_ui.creatinine_var.get())
        age = float(self.eGFR_ped_ui.age_var.get())
        height = float(self.eGFR_ped_ui.height_var.get())

        gender = self.eGFR_ped_ui.patient_gender.get()
        if not gender:
            Messagebox.show_warning("Please select gender.")
            return
        if creatinine <= 0 or height <= 0:
            raise ValueError("Height and creatinine must be positive numbers.")

        # Determine constant k based on age and gender
        if age < 1:
            k = 0.45
        elif 1 <= age < 13:
            k = 0.55
        elif age >= 13 and gender.lower() == "male":
            k = 0.70
        elif age >= 13 and gender.lower() == "female":
            k = 0.55
        else:
            k = 0.55  # fallback

        egfr = (k * height) / creatinine
        self.eGFR_ped_ui.result.config(text=f"EGFR: {egfr:.1f} mL/min")
        
        # Determine interpretation based on eGFR value
        if egfr >= 90:
            stage, msg, color = "Normal", "Kidney function is normal for age.", "success"
        elif egfr >= 60:
            if age < 2:
                stage, msg, color = "Likely Normal (Infant Range)", "Slightly lower GFR may be normal under age 2.", "info"
            else:
                stage, msg, color = "Mildly Decreased", "Slightly reduced kidney function; monitor if persistent.", "info"
        elif egfr >= 45:
            stage, msg, color = "Mild–Moderate Decrease", "Possible CKD Stage 3a; evaluate underlying causes.", "warning"
        elif egfr >= 30:
            stage, msg, color = "Moderate–Severe Decrease", "CKD Stage 3b; nephrology assessment recommended.", "warning"
        elif egfr >= 15:
            stage, msg, color = "Severe Decrease", "Advanced CKD (Stage 4); close monitoring required.", "danger"
        else:
            stage, msg, color = "Kidney Failure", "End-stage kidney disease (Stage 5); dialysis likely indicated.", "danger"

        # Update labels
        self.eGFR_ped_ui.interpret_text.config(text=f"{stage}\n{msg}", bootstyle=color)

    def calculate_urine_acr(self):
        creatinine = float(self.uacr_ui.creatinine_var.get())
        albumin = float(self.uacr_ui.albumin_var.get())
        
        if albumin <= 0 or creatinine <= 0:
            raise ValueError("Albumin and creatinine values must be positive.")
        acr = (albumin / creatinine) * 1000  # convert to mg/g
        
        self.uacr_ui.result.config(text=f"UACR: {acr:.1f} mg/g")

        # Determine interpretation
        if acr < 30:
            category = "Normal"
            color = "success"
            message = "Normal albumin excretion."
        elif 30 <= acr <= 300:
            category = "Microalbuminuria"
            color = "warning"
            message = "Early sign of kidney damage (moderately increased)."
        else:
            category = "Macroalbuminuria"
            color = "danger"
            message = "Severe kidney damage (overt nephropathy)."

        # Update interpretation display
        self.uacr_ui.interpret_text.config(text=f"{category}\n{message}", bootstyle=color)

    def calculate_urine_osmolality(self):
        na = float(self.uosm_ui.sodium_var.get())
        k = float(self.uosm_ui.potassium_var.get())
        urea = float(self.uosm_ui.urea_var.get())
        glucose = float(self.uosm_ui.glucose_var.get())
    
        if any(val < 0 for val in [na, k, urea, glucose]):
            raise ValueError("All input values must be positive numbers.")

        uosm = (2 * (na + k)) + (urea / 5.6) + (glucose / 18)
        self.uosm_ui.result.config(text=f"Uosm: {uosm:.1f} mOsm/kg")

        # Interpretation logic
        if uosm < 100:
            category = "Very Dilute Urine"
            color = "info"
            msg = "Possible diabetes insipidus or water intoxication."
        elif 100 <= uosm <= 600:
            category = "Normal Range"
            color = "success"
            msg = "Typical urine concentration (normal hydration)."
        elif 600 < uosm <= 800:
            category = "Concentrated Urine"
            color = "warning"
            msg = "Suggests dehydration or increased ADH activity."
        else:
            category = "Highly Concentrated / Glycosuria"
            color = "danger"
            msg = "Strongly concentrated urine or solute load (e.g. high glucose)."

        # Update interpretation display
        self.uosm_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)

    def calculate_serum_osmolarity(self):
        """
        Calculates serum osmolarity (mOsm/kg) using UREA (mg/dL) instead of BUN.
        Formula: 2*(Na + K) + (Glucose / 18) + (Urea / 5.6)
        """
        try:
            na = float(self.sosm_ui.sodium_var.get())
            k = float(self.sosm_ui.potassium_var.get())
            urea = float(self.sosm_ui.urea_var.get())
            glucose = float(self.sosm_ui.glucose_var.get())

            osm = 2 * (na + k) + (glucose / 18) + (urea / 5.6)
            self.sosm_ui.result.config(text=f"{osm:.2f} mOsm/kg")
            # Interpretation logic
            if osm < 275:
                interpretation = "Low Osmolarity (Hypoosmolar)"
                color = "info"
            elif 275 <= osm <= 295:
                interpretation = "Normal Osmolarity"
                color = "success"
            else:
                interpretation = "High Osmolarity (Hyperosmolar)"
                color = "danger"
            # Update interpretation display
            self.sosm_ui.interpret_text.config(text=interpretation, bootstyle=color)

        except ValueError:
            Messagebox.show_error("Invalid Input", "Please enter valid numeric values for all fields.")

    def calculate_ldl(self):
        try:
            tc = float(self.ldl_ui.tc_var.get())
            tg = float(self.ldl_ui.tg_var.get())
            hdl = float(self.ldl_ui.hdl_var.get())

            if any(val <= 0 for val in [tc, hdl, tg]):
                Messagebox.show_error("Invalid Input", "All input values must be positive numbers.")
                return

            non_hdl = tc - hdl
            # Sampson formula
            ldl = tc - hdl - (tg / 6.85) + ((tg * non_hdl) / 2600)
            # Result label update
            self.ldl_ui.result.config(text=f"LDL: {ldl:.1f} mg/dL")
            # Interpretation
            if ldl < 100:
                category = "Optimal"
                color = "success"
                msg = "Low risk of atherosclerotic cardiovascular disease (ASCVD)."
            elif 100 <= ldl < 130:
                category = "Near Optimal"
                color = "info"
                msg = "Acceptable for most individuals."
            elif 130 <= ldl < 160:
                category = "Borderline High"
                color = "warning"
                msg = "Lifestyle modification recommended."
            elif 160 <= ldl < 190:
                category = "High"
                color = "danger"
                msg = "Consider medication if persistent."
            else:
                category = "Very High"
                color = "danger"
                msg = "Aggressive lipid-lowering therapy advised."

            self.ldl_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)

        except ValueError:
            Messagebox.show_error("Invalid Input", "Please enter valid numeric values for all fields.")

    def calculate_hdl_from_sampson(self):

        tc = float(self.hdl_ui.tc_var.get())
        tg = float(self.hdl_ui.tg_var.get())
        ldl = float(self.hdl_ui.ldl_var.get())

     
        if any(val <= 0 for val in [tc, tg, ldl]):
            raise ValueError("All input values must be positive numbers.")

        hdl = tc - ldl - (tg / 8.9) + ((tg * tc) / 2140) - ((tg ** 2) / 16100)
        self.hdl_ui.result.config(text=f"HDL: {hdl:.1f} mg/dL")

        # Determine HDL category
        if hdl < 40:
            category = "Low HDL (High Risk)"
            color = "danger"
            msg = "Low protective cholesterol — higher heart disease risk."
        elif 40 <= hdl < 60:
            category = "Borderline HDL"
            color = "warning"
            msg = "Average protection, consider improving diet and exercise."
        else:
            category = "Optimal HDL (Protective)"
            color = "success"
            msg = "Good HDL level — helps lower heart disease risk."

        self.hdl_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)
        



if __name__ == "__main__":
    root = Tk()
    root.title("ChemCalc by Sct Clinton Ohagwam")
    root.geometry("450x650")
    app = ChemCalc(root)
    root.mainloop()
