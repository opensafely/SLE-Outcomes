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
            "category": {"ratios": {"1": 0.49,"2": 0.51}},
        }
    ),

    #HAS SYSTEMIC LUPUS 
    #-- USE LUPUS DATE TO CREATE A BINARY VARIABLE AS CREATING BINARY VAR AND DATE VAR DON'T ALIGN.
    # sle=patients.with_these_clinical_events(
    #   codelist=systemic_lupus_erytematosus_codes, 
    #   return_expectations={"incidence": 0.05} 
    # ),

    fst_lupus_dt=patients.with_these_clinical_events(
        codelist=systemic_lupus_erytematosus_codes,
        returning="date",
        date_format="YYYY-MM-DD",
        find_first_match_in_period=True,
        return_expectations={"incidence": 0.4, "date": {"earliest":"2000-01-01"}},

    ),

    #DEATH
    died_any=patients.died_from_any_cause(
    on_or_after=cohort_start,
    returning="date_of_death",
    date_format="YYYY-MM-DD",
    return_expectations={
        "date": {"earliest" : "2000-02-01", "latest": pandemic_start},
        "incidence" : 0.1
    },
)

)
