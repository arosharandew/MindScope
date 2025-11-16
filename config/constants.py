# config/constants.py
# Data constants
MISSING_VALUES = [-4, 9, 88, 99, 888, 999, 8888, 9999, '.']
TARGET_COLUMN = 'DEMENTED'

# Non-medical features (UPDATED VERSION)
NON_MEDICAL_FEATURES = [
    # Demographic & Personal Info (existing)
    'NACCID', 'NACCADC', 'VISITMO', 'VISITDAY', 'VISITYR', 'NACCVNUM',
    'BIRTHMO', 'BIRTHYR', 'SEX', 'HISPANIC', 'HISPOR', 'RACE', 'RACESEC',
    'RACETER', 'PRIMLANG', 'EDUC', 'MARISTAT', 'NACCLIVS', 'INDEPEND',
    'RESIDENC', 'HANDED', 'NACCAGE', 'NACCAGEB', 'NACCNIHR',

    # Co-participant Demographics (existing)
    'INBIRMO', 'INBIRYR', 'INSEX', 'INHISP', 'INHISPOR', 'INRACE',
    'INRASEC', 'INRATER', 'INEDUC', 'INRELTO', 'INLIVWTH', 'INVISITS',
    'INCALLS', 'INRELY', 'NACCNINR',

    # Family History (existing)
    'NACCFAM', 'NACCMOM', 'NACCDAD', 'NACCFADM', 'NACCFFTD',

    # Visit & Administrative (existing)
    'PACKET', 'FORMVER', 'NACCAVST', 'NACCNVST', 'NACCDAYS', 'NACCFDYS',

    # NEWLY ADDED FEATURES:
    # Lifestyle Factors
    'TOBAC30', 'SMOKYRS', 'ALCFREQ',

    # Functional Abilities (ADLs)
    'BILLS', 'SHOPPING', 'MEALPREP'
]

# Model constants
RANDOM_STATE = 42
TEST_SIZE = 0.2
CV_FOLDS = 5