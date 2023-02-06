library('tidyverse')
library('dplyr')

df_input <- read_csv(
  here::here("output", "input.csv"),
  col_types = cols(patient_id = col_integer(),age = col_double())
)

#sex = F
df_clean_1 <- df_input %>% filter(sex == "1")

#Save file as CSV
write.csv(df_clean_1, file="output/intermediate_1.csv", row.names = F)

