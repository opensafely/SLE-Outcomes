from cohortextractor import (
    StudyDefinition,
    patients, 
    codelist, 
    codelist_from_csv,
    combine_codelists,
    filter_codes_by_category,
)  # NOQA

from codelists import *


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

    address=patients.address_as_of(
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

    sle=patients.with_these_clinical_events(
        codelist=systemic_lupus_erytematosus_codes,
        between=["2000-01-01","today"],
        find_last_match_in_period=True,
        return_expectations={"incidence": 0.1},
    ),

)
