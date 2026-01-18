# formulas.py
import math

# -----------------------
# Conversion constants
# -----------------------
CR_MGDL_TO_UMOLL = 88.4      # 1 mg/dL creatinine = 88.4 µmol/L
GLUCOSE_MGDL_TO_MMOLL = 1/18.0   # 1 mg/dL glucose = 1/18 mmol/L
UREA_MGDL_TO_MMOLL = 1 / 6.006   # 1 mg/dL urea ≈ 1/6.006 mmol/L (MW urea = 60.06 g/mol)
CHOL_MGDL_TO_MMOL = 1/38.67      # cholesterol ~38.67 mg/dL per mmol/L (for completeness)
TG_MGDL_TO_MMOL = 1/88.57        # triglyceride approx conversion (not used often)

# -----------------------
# Conversion helpers
# -----------------------
def creat_umoll_to_mgdl(val):
    return val / CR_MGDL_TO_UMOLL

def creat_mgdl_to_umoll(val):
    return val * CR_MGDL_TO_UMOLL

def mgl_to_mgdl(val):
    return val / 10.0

def glucose_mmol_to_mgdl(val):
    return val * 18.0

def glucose_mgdl_to_mmol(val):
    return val / 18.0

def urea_mmol_to_mgdl(val):
    return val * 6.006

def urea_mgdl_to_mmol(val):
    return val / 6.006

def kg_from_lb(lb):
    return lb * 0.45359237

def cm_from_m(m):
    return m * 100.0

def lipid_to_mgdl(value, unit, analyte):
    if unit == "mmol/L":
        if analyte in ("TC", "LDL", "HDL"):
            return value * 38.67
        elif analyte == "TG":
            return value * 88.57
    return value

def lipid_from_mgdl(value, unit, analyte):
    if unit == "mmol/L":
        if analyte in ("TC", "LDL", "HDL"):
            return value / 38.67
        elif analyte == "TG":
            return value / 88.57
    return value

# Utility: normalize numeric input
def _to_float(value):
    if value is None or value == "":
        raise ValueError("Empty input")
    try:
        return float(value)
    except Exception:
        raise ValueError("Invalid numeric input")

# -----------------------
# 1) CKD-EPI (2021, race-free) — creatinine must be in mg/dL
#    Returns eGFR in mL/min/1.73m2 (normalized). If adjust_to_bsa=True returns absolute mL/min.
# -----------------------
def egfr_ckdepi2021(creat_value, creat_unit="umol/L", age=40, sex="male", adjust_to_bsa=False, weight_kg=None, height_cm=None):
    # convert creat to mg/dL
    if creat_unit.lower() in ("umol/l", "umol", "µmol/l", "µmol"):
        scr_mgdl = creat_umoll_to_mgdl(_to_float(creat_value))
    elif creat_unit.lower() in ("mg/dl", "mg/dl".lower()):
        scr_mgdl = _to_float(creat_value)
    else:
        raise ValueError("Unsupported creatinine unit")

    age = float(age)
    sex = sex.lower()

    # CKD-EPI 2021 constants (race-free)
    kappa = 0.7 if sex == "female" else 0.9
    alpha = -0.241 if sex == "female" else -0.302
    sex_factor = 1.012 if sex == "female" else 1.0
    # formula:
    x = scr_mgdl / kappa
    egfr = 142 * (min(x, 1) ** alpha) * (max(x, 1) ** -1.200) * (0.9938 ** age) * sex_factor
    if adjust_to_bsa:
        if weight_kg is None or height_cm is None:
            raise ValueError("weight and height required for BSA adjustment")
        # Mosteller BSA
        bsa = math.sqrt((height_cm * weight_kg) / 3600.0)
        egfr_absolute = egfr * (bsa / 1.73)
        return round(egfr_absolute, 2)
    return round(egfr, 2)

# -----------------------
# 2) Cockcroft-Gault (alternative) — returns CrCl in mL/min optionally normalized to 1.73m2
# -----------------------
def cockcroft_gault(age, weight_kg, creat_value, creat_unit="mg/dL", sex="male", normalize_to_bsa=False, height_cm=None):
    age = float(age)
    weight_kg = float(weight_kg)
    sex = sex.lower()

    if creat_unit.lower() in ("umol/l", "umol", "µmol/l", "µmol"):
        scr_mgdl = creat_umoll_to_mgdl(_to_float(creat_value))
    else:
        scr_mgdl = _to_float(creat_value)

    crcl = ((140 - age) * weight_kg) / (72.0 * scr_mgdl)
    if sex == "female":
        crcl *= 0.85
    if normalize_to_bsa:
        if height_cm is None:
            raise ValueError("height required for BSA normalization")
        bsa = math.sqrt((height_cm * weight_kg) / 3600.0)
        crcl_norm = crcl * (1.73 / bsa)
        return round(crcl_norm, 2)
    return round(crcl, 2)

# -----------------------
# 3) Pediatric eGFR (Schwartz) — expects height in cm, creatinine in mg/dL
# -----------------------
def egfr_schwartz(height_cm, creat_value, creat_unit="mg/dL"):
    height_cm = float(height_cm)
    if creat_unit.lower() in ("umol/l", "umol", "µmol/l", "µmol"):
        scr_mgdl = creat_umoll_to_mgdl(_to_float(creat_value))
    else:
        scr_mgdl = _to_float(creat_value)

    if scr_mgdl <= 0 or height_cm <= 0:
        raise ValueError("Height and creatinine must be positive numbers.")

    k = 0.413  # bedside Schwartz (k=0.413) commonly used
    egfr = (k * height_cm) / scr_mgdl
    return round(egfr, 2)


def calc_pediatric_egfr(height, age_var, sex, creat_value, creat_unit="mg/dL"):
        height_cm = _to_float(height)
        if creat_unit.lower() in ("umol/l", "umol", "µmol/l", "µmol"):
            scr_mgdl = creat_umoll_to_mgdl(_to_float(creat_value))
        else:
            scr_mgdl = _to_float(creat_value)
        #flags
        if scr_mgdl <= 0 or height_cm <= 0:
            raise ValueError("Height and creatinine must be positive numbers.")
       
        # Determine constant k based on age and gender
        if age_var < 1:
            k = 0.45
        elif 1 <= age_var < 13:
            k = 0.55
        elif age_var >= 13 and sex.lower() == "male":
            k = 0.70
        elif age_var >= 13 and sex.lower() == "female":
            k = 0.55
        else:
            k = 0.55  # fallback

        egfr = (k * height_cm) / scr_mgdl
        return round(egfr, 2)
     
# -----------------------
# 4) UACR (mg/g) — accepts albumin in mg/L or mg/dL; creatinine in mg/dL
#     Default SI albumin unit: mg/L (we convert to mg/dL internally)
# -----------------------
def calc_uacr(alb_value, albumin_unit, creat_value, creat_unit="mg/dL"):
    """
    Returns UACR in mg/g
    """
    # Albumin → mg/dL
    if albumin_unit.lower() in ("mg/l", "mg/L"):
        albumin_mg_dl = mgl_to_mgdl(_to_float(alb_value))
    else:
        albumin_mg_dl = _to_float(alb_value)

    # Creatinine → mg/dL
    if creat_unit.lower() in ("umol/l", "umol", "µmol/l", "µmol"):
        creatinine_mg_dl = creat_umoll_to_mgdl(_to_float(creat_value))
    elif creat_unit.lower() in ("mg/l", "mg/L"):
        creatinine_mg_dl = mgl_to_mgdl(_to_float(creat_value))
    else:
        creatinine_mg_dl = _to_float(creat_value)

    # UACR mg/g
    uacr = (albumin_mg_dl / creatinine_mg_dl) * 1000
    return round(uacr, 2)

# -----------------------
# 5) Serum Osmolality (mOsm/kg) — urea in mg/dL or mmol/L, glucose in mg/dL or mmol/L
#    Uses exact molecular weight conversions for precision
#    Formula: 2*(Na + K) + glucose_mgdl/18 + urea_mgdl/6.006
# -----------------------
def calc_serum_osm(na, k, glucose_value, glucose_unit="mg/dL", urea_value=None, urea_unit="mg/dL"):
    na = float(na)
    k = float(k)
    if glucose_unit.lower() in ("mmol/l", "mmol"):
        glucose_mgdl = glucose_mmol_to_mgdl(_to_float(glucose_value))
    else:
        glucose_mgdl = _to_float(glucose_value)

    if urea_value is None or urea_value == "":
        # If urea omitted, assume 0
        urea_mgdl = 0.0
    else:
        if urea_unit.lower() in ("mmol/l", "mmol"):
            urea_mgdl = urea_mmol_to_mgdl(_to_float(urea_value))
        else:
            urea_mgdl = _to_float(urea_value)

    osm = 2.0 * (na + k) + (glucose_mgdl / 18.0) + (urea_mgdl / 6.006)
    return round(osm, 2)

# -----------------------
# 6) Urine Osmolality estimate (mOsm/kg) — sodium,k in mmol/L, urea mg/dL, glucose mg/dL
#    Formula: 2*(Na + K) + urea_mgdl/6.006 + glucose_mgdl/18
# -----------------------
def calc_urine_osm(na, k, urea_value, urea_unit="mg/dL", glucose_value=0.0, glucose_unit="mg/dL"):
    na = float(na)
    k = float(k)
    if glucose_unit.lower() in ("mmol/l", "mmol"):
        glucose_mgdl = glucose_mmol_to_mgdl(_to_float(glucose_value))
    else:
        glucose_mgdl = _to_float(glucose_value)

    if urea_unit.lower() in ("mmol/l", "mmol"):
        urea_mgdl = urea_mmol_to_mgdl(_to_float(urea_value))
    else:
        urea_mgdl = _to_float(urea_value)

    osm = 2.0 * (na + k) + (urea_mgdl / 6.006) + (glucose_mgdl / 18.0)
    return round(osm, 1)

# -----------------------
# 7) Sampson LDL formula 
#    Using commonly used Sampson variant:
#      LDL = TC - HDL - (TG/6.85) + (TG * nonHDL)/2600
# -----------------------
def calc_ldl_sampson(tc, tc_unit, tg, tg_unit, hdl, hdl_unit):
    tc_mg = lipid_to_mgdl(_to_float(tc), tc_unit, "TC")
    tg_mg = lipid_to_mgdl(_to_float(tg), tg_unit, "TG")
    hdl_mg = lipid_to_mgdl(_to_float(hdl), hdl_unit, "HDL")

    if tg_mg > 800:
        raise ValueError("Triglycerides too high for Sampson equation")

    #ldl_mg = (tc_mg / (1 + 0.16 * tg_mg / 100) - hdl_mg - (tg_mg / 8.9) + (tg_mg * tc_mg / 2140) - (tg_mg ** 2 / 16100) )
    non_hdl = tc_mg - hdl_mg
    ldl_mg = (tc_mg/0.948) - (hdl_mg/0.971) - ((tg_mg/8.56) + (tg_mg * non_hdl/2140) - ((tg_mg * tc_mg)/16100)) - 9.44
#    ldl_mg = tc_mg - hdl_mg - (tg_mg / 6.85) + ((tg_mg * non_hdl) / 2600)


    return lipid_from_mgdl(ldl_mg, hdl_unit, "LDL")

# -----------------------
# 8) Rearranged Sampson to solve for HDL given TC, TG, LDL
#    HDL = TC - LDL - (TG/8.9) + ((TG * TC) / 2140) - ((TG**2) / 16100)
#    Provided as estimation only — prefer measured HDL.
# -----------------------
def calc_hdl_from_sampson(tc_val, tc_unit, tg_val, tg_unit, ldl_val, ldl_unit):
    tc_mg = lipid_to_mgdl(_to_float(tc_val), tc_unit, "TC")
    tg_mg = lipid_to_mgdl(_to_float(tg_val), tg_unit, "TG")
    ldl_mg = lipid_to_mgdl(_to_float(ldl_val), ldl_unit, "LDL")

    if tg_mg > 800:
        raise ValueError("Triglycerides too high for Sampson equation")

   # hdl_mg = (tc_mg - ldl_mg - (tg_mg / 8.9) + (tg_mg * tc_mg / 2140) - (tg_mg ** 2 / 16100))

    numerator = (ldl_mg - (tc_mg / 0.948) + (tg_mg / 8.56) + (tg_mg * tc_mg / 2140) - (tg_mg ** 2 / 16100) + 9.44)
    denominator = (tg_mg / 2140) - (1 / 0.971)
    if abs(denominator) < 1e-6:
        raise ValueError("Unstable Sampson HDL calculation (denominator ≈ 0)")
    hdl_mg = numerator / denominator

    return lipid_from_mgdl(hdl_mg, ldl_unit, "HDL")

# -----------------------
# 9) BMI helper
# -----------------------
def calc_bmi(weight_kg, height_cm):
    w = _to_float(weight_kg)
    h_m = _to_float(height_cm) / 100.0
    if h_m <= 0:
        raise ValueError("Height must be > 0")
    return round(w / (h_m * h_m), 1)

def calculate_bsa(weight_kg, height_cm):
    """
    Du Bois formula
    """
    return 0.007184 * (weight_kg ** 0.425) * (height_cm ** 0.725)
