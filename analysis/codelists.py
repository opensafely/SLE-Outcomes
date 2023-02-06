from cohortextractor import (
    codelist_from_csv,
)  # NOQA


#Codelist into variables

#SLE
systemic_lupus_erytematosus_codes = codelist_from_csv(
    "codelists/opensafely-systemic-lupus-erythematosus-sle.csv", system = "ctv3", column="CTV3ID"
)

#CHD
chronic_heart_disease_codes = codelist_from_csv(
    "codelists/opensafely-chronic-cardiac-disease.csv", system = "ctv3", column="CTV3ID"
)