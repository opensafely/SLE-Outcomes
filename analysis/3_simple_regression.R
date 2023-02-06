library('tidyverse')
library('dplyr')

df_input <- read_csv(
  here::here("output", "intermediate_1.csv"),
  col_types = cols(patient_id = col_integer(),age = col_double())
)

#Perform a regression with current variables to look for association with LUPUS and demographic
#factors

model1 <- glm(sle_flag ~ sex +
                         age +
                         address_imd,
                         data = df_input,
                         family = "gaussian")


temp_df <- summary(model1)

temp_df_1 <- data.frame(temp_df$coefficients)

write.csv(temp_df_1, file="output/simple_regression.csv")

