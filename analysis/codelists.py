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

#Diabetes
diabetes_codes = codelist_from_csv(
    "codelists/opensafely-diabetes.csv", system = "ctv3", column="CTV3ID"
)

#Hypertension
hypertension_codes = codelist_from_csv(
    "codelists/opensafely-hypertension.csv", system = "ctv3", column="CTV3ID"
)

# #CKD
# chronic_kidney_disease_codes = codelist_from_csv(
#     "codelists/opensafely-chronic-kidney-disease-snomed.csv", system = "snomed", column="snomed_id"
# )

#Cancer
cancer_codes = codelist_from_csv(
    "codelists/opensafely-cancer-excluding-lung-and-haematological.csv", system = "ctv3", column="CTV3ID"
)

#Haematological Cancer
haematological_cancer_codes = codelist_from_csv(
    "codelists/opensafely-haematological-cancer.csv", system = "ctv3", column="CTV3ID"
)

#Lung Cancer
lung_cancer_codes = codelist_from_csv(
    "codelists/opensafely-lung-cancer.csv", system = "ctv3", column="CTV3ID"
)