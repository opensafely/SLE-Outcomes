from cohortextractor import (
    codelist_from_csv,
)  # NOQA


#Codelist into variables

#Other 
#Smoking
clear_smoking_codes = codelist_from_csv(
    "codelists/opensafely-smoking-clear.csv", system="ctv3", column="CTV3Code", 
        category_column="Category",
)

#Diseases/Conditions
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

#MEDICATIONS (REQUIRES SOME SEPARATE HANDLING TO SPLIT CODES UP INTO INDIVIDUAL VARIABLES)
#DMARDS*****
#azathioprine
azathioprine_codes = codelist_from_csv(
    "local_codelists/azathioprine_codes.csv", system = "snomed", column="snomed_id"
)

#ciclosporin
ciclosporin_codes = codelist_from_csv(
    "local_codelists/ciclosporin_codes.csv", system = "snomed", column="snomed_id"
)

#leftlunomide
leftlunomide_codes = codelist_from_csv(
    "local_codelists/leftlunomide_codes.csv", system = "snomed", column="snomed_id"
)

#mercaptopurine
mercaptopurine_codes = codelist_from_csv(
    "local_codelists/mercaptopurine_codes.csv", system = "snomed", column="snomed_id"
)

#methotrexate
methotrexate_codes = codelist_from_csv(
    "local_codelists/methotrexate_codes.csv", system = "snomed", column="snomed_id"
)

#mycophenolate
mycophenolate_codes = codelist_from_csv(
    "local_codelists/mycophenolate_codes.csv", system = "snomed", column="snomed_id"
)

#penicilliamine
penicilliamine_codes = codelist_from_csv(
    "local_codelists/penicilliamine_codes.csv", system = "snomed", column="snomed_id"
)

#sulfasalazine
sulfasalazine_codes = codelist_from_csv(
    "local_codelists/sulfasalazine_codes.csv", system = "snomed", column="snomed_id"
)

# #ICD10 infection    ***Going to need to work out how to implement infection codes A00-B99)
# infection_codes = codelist_from_csv(
#     "local_codelists/infection_codes.csv", system = "icd10", column = "code"
# )

