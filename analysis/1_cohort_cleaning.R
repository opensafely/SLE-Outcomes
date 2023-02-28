library('tidyverse')
library('dplyr')

df_input <- read_csv(
  here::here("output", "input.csv.gz"))

#Save over the original file for quick resetting
df <- df_input

#create any newly required variables 
df <- df %>% mutate(died_after_20200323_flag = case_when(!is.na(died_after_20200323) ~ 1,
                                                    TRUE ~ 0,),
                    covid_test_positive_flag = case_when(!is.na(covid_test_positive) ~ 1,
                                  TRUE ~ 0),
                    covid_test_negative_flag = case_when(!is.na(covid_test_negative) ~ 1,
                                  TRUE ~ 0),
                    lupus_flag = case_when(!is.na(fst_lupus_dt) ~ 1,
                                  TRUE ~ 0),
                    age_group = case_when(age < 18 ~ '1: <18',
                                          age > 17 & age < 30 ~ '2: 18-29',
                                          age > 29 & age < 40 ~ '3: 18-39',
                                          age > 39 & age < 50 ~ '4: 18-49',
                                          age > 49 & age < 60 ~ '5: 18-59',
                                          age > 59 & age < 70 ~ '6: 18-69',
                                          age > 69 ~ '7: >69',
                                          TRUE ~ 'Other')
                    )

#correctly format all of the variables
df <- df %>% mutate(sex = as.factor(sex),
                    ethnicity_by_6_groupings = as.factor(ethnicity_by_6_groupings),
                    smoking_status = as.factor(smoking_status),
                    smoking_status_comb = as.factor(smoking_status_comb),
                    heart_disease = as.factor(heart_disease),
                    diabetes_prior = as.factor(diabetes_prior),
                    hypertension_prior = as.factor(hypertension_prior),
                    cancer_prior = as.factor(cancer_prior),
                    haematological_cancer_prior = as.factor(haematological_cancer_prior),
                    lung_cancer_prior = as.factor(lung_cancer_prior),
                    admitted_to_hospital_last_year = as.factor(admitted_to_hospital_last_year),
                    azathioprine_last_year = as.factor(azathioprine_last_year),
                    ciclosporin_last_year = as.factor(ciclosporin_last_year),
                    leftlunomide_last_year= as.factor(leftlunomide_last_year),
                    mercaptopurine_last_year= as.factor(mercaptopurine_last_year),
                    methotrexate_last_year= as.factor(methotrexate_last_year),
                    penicilliamine_last_year= as.factor(penicilliamine_last_year),
                    sulfasalazine_last_year= as.factor(sulfasalazine_last_year),
                    died_after_20200323_flag = as.factor(died_after_20200323_flag),
                    covid_test_positive_flag = as.factor(covid_test_positive_flag),#
                    covid_test_negative_flag = as.factor(covid_test_negative_flag),
                    lupus_flag = as.factor(lupus_flag),
                    age_group = as.factor(age_group),
                    imdQ5 = as.factor(imdQ5))

#select only key variables
df <- df %>% select (sex,
                    ethnicity_by_6_groupings,
                    smoking_status,
                    smoking_status_comb,
                    heart_disease,
                    diabetes_prior,
                    hypertension_prior,
                    cancer_prior,
                    haematological_cancer_prior,
                    lung_cancer_prior,
                    admitted_to_hospital_last_year,
                    azathioprine_last_year,
                    ciclosporin_last_year,
                    leftlunomide_last_year,
                    mercaptopurine_last_year,
                    methotrexate_last_year,
                    penicilliamine_last_year,
                    sulfasalazine_last_year,
                    died_after_20200323_flag,
                    covid_test_positive_flag,
                    covid_test_negative_flag,
                    lupus_flag,
                    age_group,
                    imdQ5)


#Loop to create demo table, grouped by having lupus or not
#create a variable list to loop through
variable.list <- ls(df)

#Calculate how many individuals are in each group
lupus.count <- df %>% group_by(lupus_flag) %>% count()

no.lupus <-  lupus.count$n[1]
has.lupus <- lupus.count$n[2]

#create a blank dataframe
master.df <- data.frame(cbind(1,1,1,1,1))
colnames(master.df) <- c("Variable", "Lupus", "Variable Level", "n", "Perc")

#create an empty row
empty.row <- data.frame("","","","","")
colnames(empty.row) <- c("Variable", "Lupus", "Variable Level", "n", "Perc")

#perform the analysis loop


for (i in 1:ncol(df)){
  
  temp.df <- df %>% group_by(df$lupus_flag,df[variable.list[i]]) %>%
    count() %>% data.frame()
  
  temp.df1 <-  data.frame(variable.list[i], temp.df[1], temp.df[2], temp.df[3])
  
  temp.df1 <- temp.df1 %>% mutate(percentage = NA)#case_when(temp.df[1] == 1 ~ (n/has.lupus)*100,
                                            #temp.df[1] == 0 ~ (n/no.lupus)*100))
  
  colnames(temp.df1) <- c("Variable", "Lupus", "Variable Level", "n", "Perc")
  
  master.df <-  rbind(master.df, temp.df1)
}

master.df <- master.df[-1,]

#set any low counts equal to 9
master.df <- master.df %>% mutate(n = case_when(n < 9 ~ 9,
                                                TRUE ~ n))
#round all counts to the nearest 12 
master.df <-  master.df %>% mutate(n = plyr::round_any(n,12))

#Save file as CSV
write.csv(master.df, file="output/cohort_demo.csv", row.names = F)
