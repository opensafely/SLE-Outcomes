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
    # Index date
    index_date = pandemic_start, # this gives you flexibility to substract eg 1 year of this date

    population=patients.registered_with_one_practice_between(
        "index_date - 1 year", "index_date" #LN: what is the reason for restricting your study to this population?
    ),

    #Basic Demographic Factors
    age=patients.age_as_of(
        "2019-09-01", # LN: why this date?
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),

    #English IMD goes from 0-32000, welsh goes from 0-1892, best to do quintiles in 
    #post processing
    address_imd=patients.address_as_of(
        "2019-09-01", # LN: why this date?
        returning="index_of_multiple_deprivation",
        round_to_nearest=100,
        return_expectations={
            "rate":"universal",
            "category": {"ratios": {"6399": 0.2, "12000": 0.2, "19000": 0.2,"25000": 0.2,"31000":0.2}}
        },
    ),

    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"1": 0.49,"2": 0.51}},
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

    #Date of Death (After Pandemic Start)
    died_after_20200323=patients.died_from_any_cause(
        on_or_after="index_date",
        returning="date_of_death",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {"earliest" : pandemic_start, "latest": pandemic_start},
            "incidence" : 0.1
        },
    ),

    #Smoking
    smoking_status=patients.categorised_as(
        {
            "S": "most_recent_smoking_code = 'S'",
            "E": """
                     most_recent_smoking_code = 'E' OR (
                       most_recent_smoking_code = 'N' AND ever_smoked
                    )
                """,
            "N": "most_recent_smoking_code = 'N' AND NOT ever_smoked",
            "M": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "S": 0.6,
                    "E": 0.1,
                    "N": 0.2,
                    "M": 0.1,
                }
            },
        },
        most_recent_smoking_code=patients.with_these_clinical_events(
            clear_smoking_codes,
            find_last_match_in_period=True,
            on_or_before="index_date",
            returning="category",
        ),
        ever_smoked=patients.with_these_clinical_events(
            filter_codes_by_category(clear_smoking_codes, include=["S", "E"]),
            on_or_before="index_date",
        ),
    ),
    # smoking status (combining never and missing)
    smoking_status_comb=patients.categorised_as(
        {
            "S": "most_recent_smoking_code = 'S'",
            "E": """
                     most_recent_smoking_code = 'E' OR (
                       most_recent_smoking_code = 'N' AND ever_smoked
                    )
                """,
            "N + M": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"S": 0.6, "E": 0.1, "N + M": 0.3}, }
        },
    ),

    #SARS-CoV-2
    covid_test_positive=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="positive",
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        between=["index_date", study_end],
        return_expectations={
            "incidence": 0.2,
            "date": {"earliest": pandemic_start, "latest": study_end},
        },

    ),

    covid_test_negative=patients.with_test_result_in_sgss(
        pathogen="SARS-CoV-2",
        test_result="negative",
        find_first_match_in_period=True,
        returning="date",
        date_format="YYYY-MM-DD",
        between=["index_date", study_end],
        return_expectations={
            "incidence": 0.2,
            "date": {"earliest": pandemic_start, "latest": study_end},
        },

    ),    

    #Systemic Lupus Erytematosus
    #LN: Think we discussed this cohort_start issue previously, I can see you're only using cohort_start here and not for e.g. comorbities. Think it'd be good to discuss if this is really what you want
    fst_lupus_dt=patients.with_these_clinical_events(
        codelist=systemic_lupus_erytematosus_codes,
        between=[cohort_start, "index_date"],
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.4, "date": {"earliest":cohort_start, 
                                                        "latest": pandemic_start}}, # the returning expectations framework will affect your dummy data

    ),

    #Confounding Health Outcomes 1 Year Prior to the Pandemic Start.

    #Chronic Cardiac Disease
    heart_disease=patients.with_these_clinical_events(
        codelist=chronic_heart_disease_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),

    #Diabetes
    diabetes_prior=patients.with_these_clinical_events(
        codelist=diabetes_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),

    #hypertension
    hypertension_prior=patients.with_these_clinical_events(
        codelist=hypertension_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),


# #CKD
#     chronic_kidney_disease_prior=patients.with_these_clinical_events(
#         codelist=chronic_kidney_disease_codes,
#         returning="binary_flag",
#         between=["index_date - 1 years", "index_date"],
#         return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
#                                                         "latest": pandemic_start}}        
#     ),


    #Cancer (excluding haem and lung cancers)
    cancer_prior=patients.with_these_clinical_events(
        codelist=cancer_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),


    #Haematological Cancer
    haematological_cancer_prior=patients.with_these_clinical_events(
        codelist=haematological_cancer_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),

    #Lung Cancer
    lung_cancer_prior=patients.with_these_clinical_events(
        codelist=lung_cancer_codes,
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence": 0.05, "date": {"earliest":"2019-03-23",
                                                         "latest": pandemic_start}}        
    ),

        #Hospital admissions 1 year prior
    admitted_to_hospital_last_year=patients.admitted_to_hospital(
        returning="binary_flag",
        between=["index_date - 1 years", "index_date"],
        return_expectations={"incidence":0.1},
    ),

# #Hospital Admission for infection 1 year prior ***currently not working will need to implement
#     admitted_to_hospital_for_infection_last_year=patients.admitted_to_hospital(
#         with_these_primary_diagnoses=infection_codes,   
#         returning="binary_flag",
#         between=["2019-03-23",pandemic_start],
#         return_expectations={"incidence":0.1},    
#     ),

    #MEDICATIONS 
    #DMARDS
    #AZATHIOPRINE
    # LN: Would you like ALL medications or restrict to a certain time window?
    azathioprine_last_year=patients.with_these_clinical_events(
        azathioprine_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,
    ),

    ciclosporin_last_year=patients.with_these_clinical_events(
        ciclosporin_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,
    ),

    leftlunomide_last_year=patients.with_these_clinical_events(
        leftlunomide_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,
    ),

    mercaptopurine_last_year=patients.with_these_clinical_events(
        mercaptopurine_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,
    ),

    methotrexate_last_year=patients.with_these_clinical_events(
        methotrexate_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,   
    ),    

    penicilliamine_last_year=patients.with_these_clinical_events(
        penicilliamine_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,   
    ),

    sulfasalazine_last_year=patients.with_these_clinical_events(
        sulfasalazine_codes,
        returning="binary_flag",
        on_or_before="index_date",
        find_last_match_in_period=True,   
    ),       

    #Outcomes*********************(post pandemic start)
    #Date of an admission to hospital
    #ONS Death registration (any cause)

    # #diagnosis of:
    # #post-viral-illness
    # new_post_viral_diagnoses=patients.with_these_clinical_events(
    #     codelist= #Create codelist
    #     returning="date",
    #     date_format="YYYY-MM-DD",
    #     find_first_match_in_period=True,
    #     return_expectations={"incidence": 0.4, "date": {"earliest":"2020-03-23"}},

    # ),  

    #Fatigue
    new_fatigue_diagnoses=patients.with_these_clinical_events(
        codelist= fatigue_codes,
        on_or_after="index_date", #LN: I'm inferring this from your expectations
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2020-03-23"}},

    ),  

    #Cardiovascular conditions
    new_cvd_diagnoses=patients.with_these_clinical_events(
        codelist=chronic_heart_disease_codes,
        on_or_after="index_date", #LN: I'm inferring this from your expectations
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2020-03-23"}},

    ),      
    #Depression
     new_depression_diagnoses=patients.with_these_clinical_events(
        codelist=depression_codes,
        on_or_after="index_date", #LN: I'm inferring this from your expectations
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.05, "date": {"earliest":"2020-03-23"}},

    ),     

    #New SLE
    new_lupus_diagnoses=patients.with_these_clinical_events(
        codelist=systemic_lupus_erytematosus_codes,
        on_or_after="index_date", #LN: I'm inferring this from your expectations
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.4, "date": {"earliest":"2020-03-23"}},

    ),    
    
)



