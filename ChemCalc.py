# ChemCalc_main.py (updated)
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from UserInterface import main_menu, eGFR_menu, eGFR_ped_menu, uacr_menu, uosm_menu, sosm_menu, ldl_menu, hdl_menu
import formulas

class ChemCalc:
    def __init__(self, root):
        self.root = root
        self.back_btn  = tb.Button(root, text="<", bootstyle="success", command=self.back_to_mainMenu)

        # pages
        self.page1 = Frame(root)
        self.page2 = Frame(root)
        self.page3 = Frame(root)
        self.page4 = Frame(root)
        self.page5 = Frame(root)
        self.page6 = Frame(root)
        self.page7 = Frame(root)
        self.page8 = Frame(root)

        self.show_page(self.page1)

        # create UI modules
        self.menu_ui = main_menu(self.page1)
        self.eGFR_ui = eGFR_menu(self.page2)
        self.eGFR_ped_ui = eGFR_ped_menu(self.page3)
        self.uacr_ui = uacr_menu(self.page4)
        self.uosm_ui = uosm_menu(self.page5)
        self.ldl_ui = ldl_menu(self.page6)
        self.hdl_ui = hdl_menu(self.page7)
        self.sosm_ui = sosm_menu(self.page8)

        # ASSIGN COMMANDS TO BUTTONS
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

    # ---------- navigation ----------
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

    # ---------- calculations ----------
    def calculate_egfr(self):
        try:
            creat_val = self.eGFR_ui.creatinine_var.get()
            age = self.eGFR_ui.age_var.get()
            height = self.eGFR_ui.height_var.get()
            weight = self.eGFR_ui.weight_var.get()
            gender = self.eGFR_ui.patient_gender.get()
            adjust_bsa = self.eGFR_ui.adjust_bsa_var.get()


            creat_unit = "µmol/L"
            try:
                # try to find attribute creatinine_field on eGFR_ui (we saved in UI for many entries)
                creat_field = getattr(self.eGFR_ui, "creatinine_field", None)
                if creat_field and getattr(creat_field, "unit_var", None):
                    creat_unit = creat_field.unit_var.get()
            except Exception:
                pass

            # call formula (CKD-EPI)
            egfr = formulas.egfr_ckdepi2021(creat_val, creat_unit, age=float(age), sex=gender.lower(), adjust_to_bsa= adjust_bsa, weight_kg=float(weight), height_cm=float(height))
            # Do NOT auto-adjust BSA; if you want absolute GFR, enable adjust_to_bsa=True and pass weight & height
            unit = "mL/min/1.73 m²" if adjust_bsa else "mL/min"


            # stage interpretation
            if egfr >= 90:
                stage, color, msg = "G1 (Normal)", "success", "Normal kidney function."
            elif egfr >= 60:
                stage, color, msg = "G2 (Mildly decreased)", "info", "Slightly reduced kidney function."
            elif egfr >= 45:
                stage, color, msg = "G3a (Mild–Moderate)", "warning", "Mild to moderate reduction in GFR."
            elif egfr >= 30:
                stage, color, msg = "G3b (Moderate–Severe)", "warning", "Moderate to severe kidney damage."
            elif egfr >= 15:
                stage, color, msg = "G4 (Severe)", "danger", "Severe kidney damage. Nephrology care required."
            else:
                stage, color, msg = "G5 (Kidney Failure)", "danger", "End-stage renal disease. Dialysis likely needed."
            
            scr_mgdl = formulas.creat_umoll_to_mgdl(float(creat_val))
            equation = (
            "Equation Used: CKD-EPI 2021\n"
            f"kappa = 0.7 if sex is female and 0.9 for male\n"
            f"alpha = -0.241 if sex is female and -0.302 for male\n"
            f"sex_factor = 1.012 if sex is female and 1.0 for male;\n"
            f" y = creatinine[{scr_mgdl:.2f}] / kappa\n"
            f"eGFR = 142 x (min(y, 1)^alpha) x (max(y, 1)^-1.200) x (0.9938^age[{age}]) x sex_factor\n"
            )
            if adjust_bsa:
                equation += (
                f"BSA Adjustment: BSA = 0.007184 × Height[{height}]^0.725 × Weight[{weight}]^0.425\n"
                f"Adjusted eGFR = eGFR × (BSA / 1.73) = {egfr:.1f} {unit}"

            )
            else: equation += ( f"eGFR = {egfr:.1f} {unit}")
            self.eGFR_ui.result.config(text=f"eGFR: {egfr:.1f} {unit}", bootstyle=color)
            self.eGFR_ui.interpret_text.config(text=f"{stage} => {msg}", bootstyle=color)
            self.eGFR_ui.equation_text.config(text=f"{equation}")

        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_pediatric_egfr(self):
        try:
            creat_val = self.eGFR_ped_ui.creatinine_var.get()
            age = float(self.eGFR_ped_ui.age_var.get())
            height = float(self.eGFR_ped_ui.height_var.get())
            gender = self.eGFR_ped_ui.patient_gender.get()

            creat_unit = "µmol/L"
            try:
                # try to find attribute creatinine_field on eGFR_ped_ui (we saved in UI for many entries)
                creat_field = getattr(self.eGFR_ped_ui, "creatinine_field", None)
                if creat_field and getattr(creat_field, "unit_var", None):
                    creat_unit = creat_field.unit_var.get()
            except Exception:
                pass

            #egfr = formulas.egfr_schwartz(height_cm=height, creat_value=creat_val, creat_unit=creat_unit)
            egfr = formulas.calc_pediatric_egfr(height=height, age_var=age, sex=gender.lower(), creat_value=creat_val, creat_unit=creat_unit)

            # interpretation (age-sensitive)
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

            scr_mgdl = formulas.creat_umoll_to_mgdl(float(creat_val))
            equation = (
                "\n\nEquation Used\n NB: creatinine is first converted to mg/dL and height to cm\n"
                f" if age is < 1 then k = 0.45,\n"
                f" if age is >=1 but < 13 then k = 0.55,\n"
                f" if age >= 13 and sex is male then k = 0.70\n"
                f" if age >= 13 and sex is female then k = 0.55\n"
                f"eGFR = k × Height[{height}] / Creatinine[{scr_mgdl:.2f}]\n"
                f"eGFR = {egfr:.1f} mL/min/1.73m²"
            )
            self.eGFR_ped_ui.result.config(text=f"eGFR: {egfr:.1f} mL/min/1.73m²", bootstyle=color)
            self.eGFR_ped_ui.interpret_text.config(text=f"{stage}\n{msg}", bootstyle=color)
            self.eGFR_ped_ui.equation_text.config(text=f"{equation}")

        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_urine_acr(self):
        try:
            # read albumin & creatinine and their units from fields (we saved albumin_field and creatinine_field on UI)
            alb_val = self.uacr_ui.albumin_var.get()
            alb_unit = getattr(self.uacr_ui, "albumin_field").unit_var.get() if getattr(self.uacr_ui, "albumin_field", None) else "mg/L"
            cr_val = self.uacr_ui.creatinine_var.get()
            cr_unit = getattr(self.uacr_ui, "creatinine_field").unit_var.get() if getattr(self.uacr_ui, "creatinine_field", None) else "mg/dL"

            acr = formulas.calc_uacr(alb_val, alb_unit, cr_val, cr_unit)
            # interpretation
            if acr < 30:
                category, color, message = "Normal", "success", "Normal albumin excretion."
            elif acr <= 300:
                category, color, message = "Microalbuminuria", "warning", "Early sign of kidney damage (moderately increased)."
            else:
                category, color, message = "Macroalbuminuria", "danger", "Severe kidney damage (overt nephropathy)."

            equation = (
                "\nEquation Used:\n NB: Creatinine and Albumin values\n are first converted to mg/dL\n"
                f"UACR = (Albumin[{alb_val}] / Creatinine[{cr_val} ])x1000\n"
                f"UACR = {acr:.2f} mg/g"
                "Final unit: mg/g"
            )
            self.uacr_ui.result.config(text=f"UACR: {acr:.2f} mg/g", bootstyle=color)
            self.uacr_ui.interpret_text.config(text=f"{category}\n{message}", bootstyle=color)
            self.uacr_ui.equation_text.config(text=f"{equation}")
        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_urine_osmolality(self):
        try:
            na = self.uosm_ui.sodium_var.get()
            k = self.uosm_ui.potassium_var.get()
            # urea & glucose read along with unit selections (we stored fields)
            urea_val = self.uosm_ui.urea_var.get()
            urea_unit = getattr(self.uosm_ui, "urea_field").unit_var.get() if getattr(self.uosm_ui, "urea_field", None) else "mmol/L"
            glucose_val = self.uosm_ui.glucose_var.get()
            glucose_unit = getattr(self.uosm_ui, "glucose_field").unit_var.get() if getattr(self.uosm_ui, "glucose_field", None) else "mmol/L"

            uosm = formulas.calc_urine_osm(na=float(na), k=float(k), urea_value=urea_val, urea_unit=urea_unit, glucose_value=glucose_val, glucose_unit=glucose_unit)
            # interpretation
            if uosm < 100:
                category = "Very Dilute Urine"
                color = "info"
                msg = "Possible diabetes insipidus or water intoxication."
            elif uosm <= 600:
                category = "Normal Range"
                color = "success"
                msg = "Typical urine concentration (normal hydration)."
            elif uosm <= 800:
                category = "Concentrated Urine"
                color = "warning"
                msg = "Suggests dehydration or increased ADH activity."
            else:
                category = "Highly Concentrated / Glycosuria"
                color = "danger"
                msg = "Strongly concentrated urine or solute load (e.g. high glucose)."

            equation = (
                "\n\nEquation Used:\n NB: Glucose and Urea values are first converted to md/dL\n"
                f"Uosm = 2(Na[{na}] + K[{k}]) + (Urea[{urea_val}] / 5.6)\n"
                f"     + (Glucose[{glucose_val}] / 18)\n"
                f"Uosm = {uosm:.1f} mOsm/kg"
            )
            self.uosm_ui.result.config(text=f"Uosm: {uosm:.1f} mOsm/kg", bootstyle=color)
            self.uosm_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)
            self.uosm_ui.equation_text.config(text=f"{equation}")
        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_serum_osmolarity(self):
        try:
            na = float(self.sosm_ui.sodium_var.get())
            k = float(self.sosm_ui.potassium_var.get())
            glucose_val = self.sosm_ui.glucose_var.get()
            glucose_unit = getattr(self.sosm_ui, "glucose_field").unit_var.get() if getattr(self.sosm_ui, "glucose_field", None) else "mmol/L"
            urea_val = self.sosm_ui.urea_var.get()
            urea_unit = getattr(self.sosm_ui, "urea_field").unit_var.get() if getattr(self.sosm_ui, "urea_field", None) else "mmol/L"

            osm = formulas.calc_serum_osm(na=na, k=k, glucose_value=glucose_val, glucose_unit=glucose_unit, urea_value=urea_val, urea_unit=urea_unit)
            # interpretation
            if osm < 275:
                interpretation = "Low Osmolarity (Hypoosmolar)"
                color = "info"
            elif osm <= 295:
                interpretation = "Normal Osmolarity"
                color = "success"
            else:
                interpretation = "High Osmolarity (Hyperosmolar)"
                color = "danger"

            equation = (
                "\n\nEquation Used:\n NB: Glucose and Urea values are first converted to md/dL\n"
                f"Serum Osm = 2(Na[{na}] + K[{k}] + (Glucose[{glucose_val}] / 18)\n" 
                f"             + (Urea[{urea_val}] / 5.6)\n"
                f"Serum Osm = {osm:.2f} mOsm/kg"
            )
            self.sosm_ui.result.config(text=f"{osm:.2f} mOsm/kg", bootstyle=color)
            self.sosm_ui.interpret_text.config(text=f"{interpretation}", bootstyle=color)
            self.sosm_ui.equation_text.config(text=f"{equation}")


        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_ldl(self):
        try:
            tc_val = self.ldl_ui.tc_var.get()
            tg_val = self.ldl_ui.tg_var.get()
            hdl_val = self.ldl_ui.hdl_var.get()
            non_hdl_val = formulas._to_float(tc_val)-formulas._to_float(hdl_val)

            tc_unit = getattr(self.ldl_ui, "tc_field").unit_var.get() if getattr(self.ldl_ui, "tc_field", None) else "mmol/L"
            tg_unit = getattr(self.ldl_ui, "tg_field").unit_var.get() if getattr(self.ldl_ui, "tg_field", None) else "mmol/L"
            hdl_unit = getattr(self.ldl_ui, "hdl_field").unit_var.get() if getattr(self.ldl_ui, "hdl_field", None) else "mmol/L"

            # read units; if field has unit_var, convert mg/dL accordingly. For simplicity here we assume mg/dL input default
            ldl = formulas.calc_ldl_sampson(tc_val, tc_unit, tg_val, tg_unit, hdl_val, hdl_unit)

            # Interpretation
            if ldl < 100:
                category = "Optimal"; color = "success"; msg = "Low risk of ASCVD."
            elif ldl < 130:
                category = "Near Optimal"; color = "info"; msg = "Acceptable for most individuals."
            elif ldl < 160:
                category = "Borderline High"; color = "warning"; msg = "Lifestyle modification recommended."
            elif ldl < 190:
                category = "High"; color = "danger"; msg = "Consider medication if persistent."
            else:
                category = "Very High"; color = "danger"; msg = "Aggressive lipid-lowering therapy advised."

            equation = (
                "\n\nEquation Used: Sampson Formula\n Values are first converted to mg/dL \n"
                f"non_hdl = TC[{tc_val}] + HDL[{hdl_val}] = {non_hdl_val}\n"
                f"LDL = (TC[{tc_val}]/0.948) - (HDL[{hdl_val}]/0.971) - [(TG[{tg_val}]/8.56)\n"
                f"      + (TG[{tg_val}] × non_hdl[{non_hdl_val}] / 2140.)\n"
                f"      - (TG[{tg_val}]² / 16,100)]-9.44\n"
                f"LDL = {ldl:.2f}{hdl_unit}"
            )
            self.ldl_ui.result.config(text=f"LDL: {ldl:.2f}{hdl_unit}", bootstyle=color)
            self.ldl_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)
            self.ldl_ui.equation_text.config(text=f"{equation}")
        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))

    def calculate_hdl_from_sampson(self):
        try:
            tc = self.hdl_ui.tc_var.get()
            tg = self.hdl_ui.tg_var.get()
            ldl = self.hdl_ui.ldl_var.get()


            tc_unit = getattr(self.hdl_ui, "tc_field").unit_var.get() if getattr(self.hdl_ui, "tc_field", None) else "mmol/L"
            tg_unit = getattr(self.hdl_ui, "tg_field").unit_var.get() if getattr(self.hdl_ui, "tg_field", None) else "mmol/L"
            ldl_unit = getattr(self.hdl_ui, "ldl_field").unit_var.get() if getattr(self.hdl_ui, "ldl_field", None) else "mmol/L"


            hdl = formulas.calc_hdl_from_sampson(tc_val=tc, tc_unit=tc_unit, tg_val=tg, tg_unit=tg_unit, ldl_val=ldl, ldl_unit=ldl_unit)
            # clamp unrealistic
            if hdl < 0:
                Messagebox.show_warning("Estimated HDL negative — value likely invalid. Direct measurement recommended.")
            # Interpretation
            if hdl < 40:
                category = "Low HDL (High Risk)"; color = "danger"; msg = "Low protective cholesterol — higher heart disease risk."
            elif hdl < 60:
                category = "Borderline HDL"; color = "warning"; msg = "Average protection."
            else:
                category = "Optimal HDL (Protective)"; color = "success"; msg = "Good HDL level."

            equation = (
                "\n\nEquation Used: Reverse Sampson Formula\n Values are first converted to mg/dL \n"
                f" numerator = (LDL[{ldl}] - (TC[{tc}] / 0.948) + (TG[{tg}] / 8.56)\n" 
                f"             + (TG[{tg}] * TG[{tg}] / 2140)" 
                f"             - (TG[{tg}] ** 2 / 16100) + 9.44)\n\n"
                f" denominator = (TG[{tg}] / 2140) - (1 / 0.971)\n"
                f" HDL = numerator / denominator"
            )
            self.hdl_ui.result.config(text=f"HDL: {hdl:.1f} mg/dL", bootstyle=color)
            self.hdl_ui.interpret_text.config(text=f"{category}\n{msg}", bootstyle=color)
            self.hdl_ui.equation_text.config(text=f"{equation}")
        except ValueError as e:
            Messagebox.show_error("Invalid input", str(e))


if __name__ == "__main__":
    root = Tk()
    root.title("ChemCalc by Sct Clinton Ohagwam v 2.1")
    root.geometry("720x840")
    app = ChemCalc(root)
    root.mainloop()
