# UserInterface.py  (updated)
from tkinter import *
import ttkbootstrap as tb
from ttkbootstrap.constants import *
# keep Messagebox usage from ttkbootstrap dialogs in main script

class NumpadPopup:
    WIDTH = 260
    HEIGHT = 180

    def __init__(self, parent, target_entry, on_close_callback=None):
        self.parent = parent
        self.target_entry = target_entry
        self.on_close_callback = on_close_callback

        self.top = tb.Toplevel(parent)
        self.top.title("Numpad")
        self.top.resizable(False, False)
        self.top.attributes("-topmost", True)
        self.top.transient(parent)
        self.top.configure(padx=10, pady=10)

        self.top.focus_force()
        self.top.bind("<FocusOut>", self._on_focus_out)

        self.create_numpad()
        self.position_popup_near_entry()
        self.top.protocol("WM_DELETE_WINDOW", self.close_popup)

    def position_popup_near_entry(self):
        self.parent.update_idletasks()
        self.target_entry.update_idletasks()

        entry_x = self.target_entry.winfo_rootx()
        entry_y = self.target_entry.winfo_rooty()
        entry_height = self.target_entry.winfo_height()

        popup_x = entry_x
        popup_y = entry_y + entry_height + 5

        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()

        if popup_x + self.WIDTH > screen_w:
            popup_x = max(0, screen_w - self.WIDTH - 10)
        if popup_y + self.HEIGHT > screen_h:
            popup_y = max(0, entry_y - self.HEIGHT - 5)

        self.top.geometry(f"{self.WIDTH}x{self.HEIGHT}+{popup_x}+{popup_y}")

    def create_numpad(self):
        frame = tb.Frame(self.top)
        frame.pack(fill=BOTH, expand=True)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2),
            ('0', 3, 1), ('.', 3, 0), ('⌫', 3, 2)
        ]

        for (text, row, col) in buttons:
            tb.Button(
                frame,
                text=text,
                width=6,
                bootstyle="primary",
                command=lambda t=text: self.on_button_click(t)
            ).grid(row=row, column=col, padx=4, pady=4)

    def on_button_click(self, char):
        if char == '⌫':
            current = self.target_entry.get()
            if current:
                self.target_entry.delete(len(current) - 1)
        else:
            self.target_entry.insert(END, char)
            self.top.focus_force()

    def _on_focus_out(self, event):
        new_focus = self.top.focus_get()
        if not new_focus or new_focus.winfo_toplevel() != self.top:
            self.close_popup()

    def close_popup(self):
        if self.on_close_callback:
            try:
                self.on_close_callback()
            except Exception:
                pass
        try:
            self.top.destroy()
        except Exception:
            pass

class CreateEntryField:
    """
    Creates label + entry field and optional unit radio buttons.
    units: list of unit strings (e.g., ["µmol/L","mg/dL"])
    default_unit: string from the list (default first)
    """
    def __init__(self, parent, label_text, variable=None, units=None, default_unit=None):
        self.parent = parent
        self.label_text = label_text
        if isinstance(variable, (StringVar, IntVar, DoubleVar, BooleanVar)):
            self.variable = variable
        else:
            self.variable = StringVar(value=str(variable) if variable is not None else "")
        # unit variable (if units provided)
        self.unit_var = None
        self.units = units
        self.default_unit = default_unit if default_unit is not None else (units[0] if units else None)
        self.create_field()

    def create_field(self):
        frame = tb.Frame(self.parent, padding='6 6 6 6')
        frame.pack(pady=4, anchor="w", fill="x")
        label = tb.Label(frame, text=f"{self.label_text}:", font=("Arial", 12))
        label.pack(side="left")
        entry = tb.Entry(frame, textvariable=self.variable, bootstyle="success",
                         font=("Helvetica", 14), foreground="green", width=16)
        entry.pack(side="left", padx=(8,8))
        entry.field_name = self.label_text

        # unit radios
        if self.units:
            self.unit_var = StringVar(value=self.default_unit)
            ub = tb.Frame(frame)
            ub.pack(side="left", padx=6)
            for u in self.units:
                # use ttkbootstrap Radiobutton
                rb = tb.Radiobutton(ub, text=u, value=u, variable=self.unit_var, bootstyle="info")
                rb.pack(pady=2, padx=4)

        entry.bind("<Button-1>", lambda e, target=entry: self.open_numpad(target))

    def open_numpad(self, entry):
        root = self.parent.winfo_toplevel()
        existing = getattr(root, "current_popup", None)
        if existing:
            try:
                existing.close_popup()
            except Exception:
                pass
            root.current_popup = None

        def _on_close():
            try:
                root.current_popup = None
            except Exception:
                pass
            try:
                root.focus_force()
            except Exception:
                pass

        root.current_popup = NumpadPopup(root, entry, on_close_callback=_on_close)


class main_menu:
    def __init__(self, page):
        self.page = page

        # Title
        title = tb.Label(page, text="ChemCalc v2.1", font=("Helvetica", 28), bootstyle="default,inverse" )
        title.pack(pady=(20, 10))

        # Author
        author = tb.Label(page, text="by Sct Clinton Ohagwam", font=("Helvetica", 22), bootstyle="default,inverse" )
        author.pack(pady=(0, 20))

        # ===== Grid container for buttons =====
        grid_frame = tb.Frame(page)
        grid_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Configure 2 columns × 4 rows
        for col in range(2): grid_frame.columnconfigure(col, weight=1)
        for row in range(4): grid_frame.rowconfigure(row, weight=1)
        btn_opts = { "bootstyle": "success", "width": 20 }

        # Buttons
        self.eGFRBtn = tb.Button(grid_frame, text="eGFR", **btn_opts)
        self.eGFR_pedBtn = tb.Button(grid_frame, text="eGFR pediatric", **btn_opts)
        self.UACRBtn = tb.Button(grid_frame, text="UACR", **btn_opts)
        self.uOsmBtn = tb.Button(grid_frame, text="Urine Osmolarity", **btn_opts)
        self.sOsmBtn = tb.Button(grid_frame, text="Serum Osmolarity", **btn_opts)
        self.LDLBtn = tb.Button(grid_frame, text="LDL", **btn_opts)
        self.HDLBtn = tb.Button(grid_frame, text="HDL", **btn_opts)

        # Place buttons (2 × 4 grid)
        self.eGFRBtn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.eGFR_pedBtn.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.UACRBtn.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.uOsmBtn.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.sOsmBtn.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.LDLBtn.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.HDLBtn.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")


class eGFR_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="eGFR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        self.discription = tb.Label(page, text="CKD-EPI creatinine equation (2021)", font=("Helvetica", 14), bootstyle="default")
        self.discription.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        # gender
        gender_frame = tb.Frame(frame_1)
        gender_frame.pack(pady=5, anchor="w")
        self.patient_gender = StringVar(value="")
        tb.Label(gender_frame, text="Gender:", font=("Helvetica", 12)).pack(side="left")
        tb.Radiobutton(gender_frame, text="Male", value="Male", variable=self.patient_gender, bootstyle="secondary").pack(side="left", padx=6)
        tb.Radiobutton(gender_frame, text="Female", value="Female", variable=self.patient_gender, bootstyle="secondary").pack(side="left", padx=6)

        # entries with units (SI defaults)
        self.creatinine_var = StringVar(value="")
        self.age_var = StringVar(value="")
        self.height_var = StringVar(value="")
        self.weight_var = StringVar(value="")

        # creatinine: default SI µmol/L, alt mg/dL
        CreateEntryField(frame_1, "Creatinine", self.creatinine_var, units=["µmol/L","mg/dL"], default_unit="µmol/L")
        CreateEntryField(frame_1, "Age (years)", self.age_var, units=None)

        # Normalize to BSA
       
        self.adjust_bsa_var = BooleanVar(value=True)
        self.adjust_bsa_chk = tb.Checkbutton( frame_1, text="Adjust to BSA", variable=self.adjust_bsa_var, 
            bootstyle="success-round-toggle", command=self.toggle_bsa_inputs)
        self.adjust_bsa_chk.pack(pady=5)

        self.BSA_frame = tb.Frame(frame_1)
        CreateEntryField(self.BSA_frame, "Height", self.height_var, units=["cm","m"], default_unit="cm")
        CreateEntryField(self.BSA_frame, "Weight", self.weight_var, units=["kg","lb"], default_unit="kg")

        self.calcEGFRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcEGFRBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

        self.toggle_bsa_inputs()


    def toggle_bsa_inputs(self):
        if self.adjust_bsa_var.get():
            self.BSA_frame.pack(pady=6, fill="x")
        else:
            self.BSA_frame.pack_forget()

class eGFR_ped_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="Pediatric GFR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        gender_frame = tb.Frame(frame_1)
        gender_frame.pack(pady=5, anchor="w")
        self.patient_gender = StringVar(value="")
        tb.Label(gender_frame, text="Gender:", font=("Helvetica", 12)).pack(side="left")
        tb.Radiobutton(gender_frame, text="Male", value="Male", variable=self.patient_gender, bootstyle="secondary").pack(side="left", padx=6)
        tb.Radiobutton(gender_frame, text="Female", value="Female", variable=self.patient_gender, bootstyle="secondary").pack(side="left", padx=6)

        self.creatinine_var = StringVar(value="")
        self.height_var = StringVar(value="")
        self.age_var = StringVar(value="")

        CreateEntryField(frame_1, "Creatinine", self.creatinine_var, units=["µmol/L","mg/dL"], default_unit="µmol/L")
        CreateEntryField(frame_1, "Age (years)", self.age_var, units=None)
        CreateEntryField(frame_1, "Height (cm)", self.height_var, units=["cm","m"], default_unit="cm")

        self.calcPedGFRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcPedGFRBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

class uacr_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="UACR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        # default SI albumin mg/L; creatinine default mg/dL
        self.albumin_var = StringVar(value="")
        self.albumin_field = CreateEntryField(frame_1, "Albumin (urine)", self.albumin_var, units=["mg/dL","mg/L"], default_unit="mg/dL")
        
        self.creatinine_var = StringVar(value="")
        self.creatinine_field = CreateEntryField( frame_1, "Creatinine(urine)", self.creatinine_var, units=["µmol/L", "mg/dL", "mg/L"], default_unit="µmol/L")

        self.calcUACRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcUACRBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

class uosm_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="Urine Osmolarity", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        self.sodium_var = StringVar(value="")
        self.sodium_field = CreateEntryField(frame_1, "Sodium", self.sodium_var, units=["mmol/L"], default_unit="mmol/L")
        self.potassium_var = StringVar(value="")
        self.potassium_field = CreateEntryField(frame_1, "Potassium", self.potassium_var, units=["mmol/L"], default_unit="mmol/L")
        self.urea_var = StringVar(value="")
        self.urea_field = CreateEntryField(frame_1, "Urea (urine)", self.urea_var, units=["mg/dL","mmol/L"], default_unit="mmol/L")
        self.glucose_var = StringVar(value="")
        self.glucose_field = CreateEntryField(frame_1, "Glucose (urine)", self.glucose_var, units=["mg/dL","mmol/L"], default_unit="mmol/L")

        self.calcUOSMBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcUOSMBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

class sosm_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="Serum Osmolarity", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        self.sodium_var = StringVar(value="")
        self.sodium_field = CreateEntryField(frame_1, "Sodium", self.sodium_var, units=["mmol/L"], default_unit="mmol/L")
        self.potassium_var = StringVar(value="")
        self.potassium_field = CreateEntryField(frame_1, "Potassium", self.potassium_var, units=["mmol/L"], default_unit="mmol/L")
        self.urea_var = StringVar(value="")
        self.urea_field = CreateEntryField(frame_1, "Urea (serum)", self.urea_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")
        self.glucose_var = StringVar(value="")
        self.glucose_field = CreateEntryField(frame_1, "Glucose (serum)", self.glucose_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")

        self.calcSOSMBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcSOSMBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

class ldl_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text=f"LDL Cholesterol", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        self.discription = tb.Label(page, text=f"Sampson Formula", font=("Helvetica", 14), bootstyle="default")
        self.discription.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        self.tc_var = StringVar(value="")
        self.tg_var = StringVar(value="")
        self.hdl_var = StringVar(value="")
        self.tc_field = CreateEntryField(frame_1, "Total Cholesterol", self.tc_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")
        self.tg_field = CreateEntryField(frame_1, "Triglyceride", self.tg_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")
        self.hdl_field = CreateEntryField(frame_1, "HDL", self.hdl_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")

        self.calcLDLBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcLDLBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)

class hdl_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text=f"HDL Cholesterol", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        frame_1 = tb.Frame(page, bootstyle="primary", padding='6 6 6 6')
        frame_1.pack(pady=20, fill="x")

        self.tc_var  = StringVar(value="")
        self.tg_var  = StringVar(value="")
        self.ldl_var = StringVar(value="")

        self.tc_field = CreateEntryField(frame_1, "Total Cholesterol", self.tc_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")
        self.tg_field = CreateEntryField(frame_1, "Triglyceride", self.tg_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")
        self.ldl_field = CreateEntryField(frame_1, "LDL", self.ldl_var, units=["mmol/L","mg/dL"], default_unit="mmol/L")

        self.calcHDLBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcHDLBtn.pack(pady=6)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=3)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=3)
        self.equation_text = tb.Label(page,text="Awaiting calculation...", font=("Helvetica", 14),bootstyle="default")
        self.equation_text.pack(pady=5)
