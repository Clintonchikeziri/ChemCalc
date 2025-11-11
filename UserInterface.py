from tkinter import *
import ttkbootstrap as tb

class NumpadPopup:
    WIDTH = 260
    HEIGHT = 180

    def __init__(self, parent, target_entry, on_close_callback=None):
        self.parent = parent
        self.target_entry = target_entry
        self.on_close_callback = on_close_callback

        # Create a Toplevel popup using ttkbootstrap styling
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

        # --- Define numpad buttons ---
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
                # delete last char
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
    """Creates entry fields; uses root.current_popup to ensure a single popup across the whole app."""
    def __init__(self, parent, label_text, variable=None):
        self.parent = parent
        self.label_text = label_text

        # Accept a tk Variable or a plain initial value; ensure self.variable is a StringVar
        if isinstance(variable, (StringVar, IntVar, DoubleVar, BooleanVar)):
            self.variable = variable
        else:
            # convert plain value into StringVar so it's safe to pass as textvariable
            self.variable = StringVar(value=str(variable) if variable is not None else "")

        self.create_field()

    def create_field(self):
        frame = tb.Frame(self.parent, padding='10 10 10 10', width=500)
        frame.pack(pady=5, anchor="w")
        label = tb.Label(frame, text=f"{self.label_text}:", font=("Arial", 12))
        label.pack(side="left")
        entry = tb.Entry(frame, textvariable=self.variable, bootstyle="success",
                         font=("Helvetica", 16), foreground="green", width=15)
        entry.pack(side="left")
        entry.field_name = self.label_text  # store label name for messagebox

        # Open numpad on mouse click (Button-1) instead of FocusIn to avoid reopen bug
        entry.bind("<Button-1>", lambda e, target=entry: self.open_numpad(target))

    def open_numpad(self, entry):
        """Open a single app-wide popup attached to the top-level root."""
        root = self.parent.winfo_toplevel()
        # close any existing popup on the root
        existing = getattr(root, "current_popup", None)
        if existing:
            try:
                existing.close_popup()
            except Exception:
                pass
            root.current_popup = None

        # create new popup and store it on the root so all CreateEntryField instances share it
        def _on_close():
            # clear the root reference when popup closes
            try:
                root.current_popup = None
            except Exception:
                pass
            # ensure focus goes back to root to avoid immediate reopen
            try:
                root.focus_force()
            except Exception:
                pass

        root.current_popup = NumpadPopup(root, entry, on_close_callback=_on_close)

class main_menu :
    def __init__(self, page):
        self.page = page

        title = tb.Label(page, text="ChemCalc", font=("Helvetica", 28), bootstyle="default,inverse")
        title.pack(pady=20)

        author = tb.Label(page, text="by Sct Clinton Ohagwam", font=("Helvetica", 22), bootstyle="default,inverse")
        author.pack(pady=20)

        self.eGFRBtn = tb.Button(page, text="eGFR", bootstyle="success")
        self.eGFRBtn.pack(pady=20)

        self.eGFR_pedBtn = tb.Button(page, text="eGFR pediatric", bootstyle="success")
        self.eGFR_pedBtn.pack(pady=20)

        self.UACRBtn = tb.Button(page, text="UACR", bootstyle="success")
        self.UACRBtn.pack(pady=20)

        self.uOsmBtn = tb.Button(page, text="Urine Osmolarity", bootstyle="success")
        self.uOsmBtn.pack(pady=20)

        self.sOsmBtn = tb.Button(page, text="Serum Osmolarity", bootstyle="success")
        self.sOsmBtn.pack(pady=20)

        self.LDLBtn = tb.Button(page, text="LDL", bootstyle="success")
        self.LDLBtn.pack(pady=20)

        self.HDLBtn = tb.Button(page, text="HDL", bootstyle="success")
        self.HDLBtn.pack(pady=20)

class eGFR_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text="eGFR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        # RadioButton for gender selection
        gender_frame = tb.Frame(frame_1, padding='10 10 10 10', width=500)
        gender_frame.pack(pady=5)
        self.genderLabel = tb.Label(gender_frame, text="Gender : ",
           wraplength=150, font=("Helvetica", 14), bootstyle="default")
        self.genderLabel.pack(side="left")
        self.patient_gender = StringVar(value="")      # use a StringVar
        self.male = Radiobutton(gender_frame, variable=self.patient_gender, font=("Helvetica", 14),
            text="Male", value="Male")
        self.male.pack(side="left")
        self.female = Radiobutton(gender_frame, variable=self.patient_gender, font=("Helvetica", 14),
            text="Female", value="Female")
        self.female.pack(side="left")

        self.creatinine_var = StringVar(value="")
        self.age_var = StringVar(value="")
        self.height_var = StringVar(value="")
        self.weight_var = StringVar(value="")
        CreateEntryField(frame_1, "Creatinine (mg/dl)", self.creatinine_var)
        CreateEntryField(frame_1, "Age", self.age_var)
        CreateEntryField(frame_1, "Height (cm)", self.height_var)
        CreateEntryField(frame_1, "Weight (kg)", self.weight_var)

        self.calcEGFRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcEGFRBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class eGFR_ped_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text="Pediatric GFR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        self.disclaimer = tb.Label(page, text="for patients below 18 years", font=("Helvetica", 18), bootstyle="default")
        self.disclaimer.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        # RadioButton for gender selection
        gender_frame = tb.Frame(frame_1, padding='10 10 10 10', width=500)
        gender_frame.pack(pady=5)
        self.genderLabel = tb.Label(gender_frame, text="Gender : ",
           wraplength=150, font=("Helvetica", 14), bootstyle="default")
        self.genderLabel.pack(side="left")
        self.patient_gender = StringVar(value="")      # use a StringVar
        self.male = Radiobutton(gender_frame, variable=self.patient_gender, font=("Helvetica", 14),
            text="Male", value="Male")
        self.male.pack(side="left")
        self.female = Radiobutton(gender_frame, variable=self.patient_gender, font=("Helvetica", 14),
            text="Female", value="Female")
        self.female.pack(side="left")

        self.creatinine_var = StringVar(value="")
        self.height_var = StringVar(value="")
        self.age_var = StringVar(value="")
        CreateEntryField(frame_1, "Creatinine (mg/dl)", self.creatinine_var)
        CreateEntryField(frame_1, "Age", self.age_var)
        CreateEntryField(frame_1, "Height (cm)", self.height_var)

        self.calcPedGFRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcPedGFRBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class uacr_menu :
    def __init__(self, page):
        self.page = page
        self.title = tb.Label(page, text="UACR", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        self.creatinine_var = StringVar(value="")
        self.albumin_var = StringVar(value="")
        self.age_var = StringVar(value="")
        CreateEntryField(frame_1, "Creatinine (mg/dl)", self.creatinine_var)
        CreateEntryField(frame_1, "Albumin (mg/dl)", self.albumin_var)

        self.calcUACRBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcUACRBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class uosm_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text="Urine Osmolarity", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        self.sodium_var = StringVar(value="")
        self.potassium_var = StringVar(value="")
        self.urea_var = StringVar(value="")
        self.glucose_var = StringVar(value="")
        CreateEntryField(frame_1, "Sodium (mmol/L)", self.sodium_var)
        CreateEntryField(frame_1, "Potassium (mmol/L)", self.potassium_var)
        CreateEntryField(frame_1, "Urea (mg/dl)", self.urea_var)
        CreateEntryField(frame_1, "Glucose (mg/dl)", self.glucose_var)

        self.calcUOSMBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcUOSMBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class sosm_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text="Serum Osmolarity", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        self.sodium_var = StringVar(value="")
        self.potassium_var = StringVar(value="")
        self.urea_var = StringVar(value="")
        self.glucose_var = StringVar(value="")
        CreateEntryField(frame_1, "Sodium (mmol/L)", self.sodium_var)
        CreateEntryField(frame_1, "Potassium (mmol/L)", self.potassium_var)
        CreateEntryField(frame_1, "Urea (mg/dl)", self.urea_var)
        CreateEntryField(frame_1, "Glucose (mg/dl)", self.glucose_var)

        self.calcSOSMBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcSOSMBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class ldl_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text=f"LDL Cholesterol\n(Sampson Formula)", font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        self.tc_var = StringVar(value="")
        self.tg_var = StringVar(value="")
        self.hdl_var = StringVar(value="")
        CreateEntryField(frame_1, "Total Cholesterol (mg/dl)", self.tc_var)
        CreateEntryField(frame_1, "Triglyceride (mg/dl)", self.tg_var)
        CreateEntryField(frame_1, "HDL (mg/dl)", self.hdl_var)

        self.calcLDLBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcLDLBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

class hdl_menu :
    def __init__(self, page):
        self.page = page

        self.title = tb.Label(page, text=f"HDL Cholesterol", 
            font=("Helvetica", 28), bootstyle="default")
        self.title.pack(pady=5)
        self.disclaimer = tb.Label(page, text=f"Calculated from Sampson formular\n(making HDL subject of formular)\nPlease HDL should not be calculated but measured.", 
            font=("Helvetica", 14), bootstyle="default")
        self.disclaimer.pack(pady=5)

        # create frame_1     for padding = 'left, top, right, down'
        frame_1 = tb.Frame(page, bootstyle="primary", padding='5 5 5 5', width=500)
        frame_1.pack(pady=10)

        self.tc_var = StringVar(value="")
        self.tg_var = StringVar(value="")
        self.ldl_var = StringVar(value="")
        CreateEntryField(frame_1, "Total Cholesterol (mg/dl)", self.tc_var)
        CreateEntryField(frame_1, "Triglyceride (mg/dl)", self.tg_var)
        CreateEntryField(frame_1, "LDL (mg/dl)", self.ldl_var)

        self.calcHDLBtn = tb.Button(page, text="Calculate", bootstyle="success")
        self.calcHDLBtn.pack(pady=5)
        self.result = tb.Label(page, text="Result", font=("Helvetica", 18), bootstyle="success")
        self.result.pack(pady=5)
        self.interpret_text = tb.Label(page,text="Awaiting input...", font=("Helvetica", 14),bootstyle="secondary")
        self.interpret_text.pack(pady=5)

