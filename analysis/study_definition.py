from cohortextractor import (
    StudyDefinition,
    patients, 
    codelist, 
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
)  # NOQA

from codelists import *

pandemic_start = "2020-03-23"
study_end = "2021-08-31"
cohort_start = "2000-01-01"



study = StudyDefinition(
    default_expectations={
        "date": {"earliest": "1900-01-01", "latest": "today"},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.registered_with_one_practice_between(
        "2019-02-01", "2020-02-01"
    ),

#Basic Demographic Factors
    age=patients.age_as_of(
        "2019-09-01",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    address_imd=patients.address_as_of(
        "2019-09-01",
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate":"universal",
            "category": {"ratios": {"100": 0.1, "200": 0.2, "300": 0.7}}
        },
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.49,"F": 0.51}},
        }
    ),

    ethnicity_by_6_groupings=patients.with_ethnicity_from_sus(
        returning="group_6",
        use_most_frequent_code=True,
        return_expectations={
            "category": {"ratios": {"1": 0.2, "2": 0.1, "3":0.1, "4":0.2, "5":0.2, "6": 0.2}},
            "incidence": 0.8,
        },
    ),

#Date of Death
    died_any=patients.died_from_any_cause(
        on_or_after=cohort_start,
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : "2000-02-01", "latest": pandemic_start},
            "incidence" : 0.1
        },
    ),

#SARS-CoV-2
    covid_test_positive=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        between=[pandemic_start, study_end],
        return_expectations={
            "incidence": 0.2,
            "date": {"earliest": pandemic_start, "latest": study_end},
        },

    ),

#Systemic Lupus Erytematosus
    fst_lupus_dt=patients.with_these_clinical_events(
        codelist=systemic_lupus_erytematosus_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.4, "date": {"earliest":"2000-01-01"}},

    ),

#Confounding Health Outcomes 1 Year Prior to the Pandemic Start.

#Chronic Cardiac Disease
    heart_disease=patients.with_these_clinical_events(
        codelist=chronic_heart_disease_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),


#Diabetes
    diabetes_prior=patients.with_these_clinical_events(
        codelist=diabetes_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),


#hypertension
    hypertension_prior=patients.with_these_clinical_events(
        codelist=hypertension_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),


# #CKD
#     chronic_kidney_disease_prior=patients.with_these_clinical_events(
#         codelist=chronic_kidney_disease_codes,
#         returning="date",
#         date_format="YYYY-MM-DD",
#         find_first_match_in_period=True,
#         return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
#     ),


#Cancer (excluding haem and lung cancers)
    cancer_prior=patients.with_these_clinical_events(
        codelist=cancer_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),


#Haematological Cancer
    haematological_cancer_prior=patients.with_these_clinical_events(
        codelist=haematological_cancer_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),

#Lung Cancer
    lung_cancer_prior=patients.with_these_clinical_events(
        codelist=lung_cancer_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2000-01-01"}}        
    ),
)



