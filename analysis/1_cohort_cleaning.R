library('tidyverse')
library('dplyr')

df_input <- read_csv(
  here::here("output", "input.csv"),
  col_types = cols(patient_id = col_integer(),age = col_double())
)

#Create binary variable that flags individuals with SLE
df_clean_1 <- df_input %>% mutate(sle_flag = case_when(!is.na(fst_lupus_dt) ~ 1,
                                                              TRUE ~ 0))

#Save file as CSV
write.csv(df_clean_1, file="output/intermediate_1.csv", row.names = F)

