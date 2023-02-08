#Script for separating out the dmard medication codelists
library(stringr)
library(dplyr)
library(tidyverse)
library(readr)


#import the codelist from the codelists folder
opensafely_dmards <- read_csv(
  here::here("codelists", "opensafely-dmards.csv")
)

#select the first word of the dmd name to create a list of medications in the
#dmard list
opensafely_dmards$short_name <- word(opensafely_dmards$dmd_name, 1)

medications_short <- opensafely_dmards %>% select(short_name) %>% distinct()

#medications can then be manually separated based on the short_name
sulfasalazine_codes <- opensafely_dmards %>% filter(short_name == "Sulfasalazine"|
                                                    short_name == "Salazopyrin"|
                                                      short_name == "Sulazine"                                                      
                                                    )

mercaptopurine_codes <- opensafely_dmards %>% filter(short_name == "Mercaptopurine" |
                                                 short_name == "Puri-Nethol" |
                                                 short_name == "Xaluprine"|
                                                 short_name == "Hanixol" )
methotrexate_codes <- opensafely_dmards %>% filter(short_name == "Methotrexate"|
                                                     short_name == "Zlatal"|
                                                     short_name == "Nordimet")

azathioprine_codes <- opensafely_dmards %>% filter(opensafely_dmards$short_name == "Azathioprine"|
                                               short_name == "Imuran"|
                                               short_name == "Immunoprin"|
                                               short_name == "Azapress")

mycophenolate_codes <- opensafely_dmards %>% filter(short_name == "Mycophenolate"|
                                                      short_name == "CellCept"|
                                                      short_name == "Myfenax"|
                                                      short_name == "Arzip")

ciclosporin_codes <- opensafely_dmards %>% filter(short_name == "Ciclosporin"|
                                                  short_name == "Sandimmun"|
                                                  short_name == "Neoral"|
                                                    short_name == "Deximune"|
                                                    short_name == "Capimune"|
                                                    short_name == "Capsorin"|
                                                    short_name == "Vanquoral")

penicilliamine_codes <- opensafely_dmards %>% filter(short_name == "Penicilliamine"|
                                                       short_name == "Distamine"|
                                                       short_name == "Metalcaptase"|
                                                       short_name == "Myocrisin")

leftlunomide_codes <- opensafely_dmards %>% filter(short_name == "Leftlunomide"|
                                               short_name == "Arava"|
                                               short_name == "Maxtrex"|
                                               short_name == "Metoject"|
                                               short_name == "Ebetrex"|
                                               short_name == "Methofill"|
                                               short_name == "Jylamvo")

write.csv(azathioprine_codes, file="local_codelists/azathioprine_codes.csv", row.names = F)

write.csv(ciclosporin_codes, file="local_codelists/ciclosporin_codes.csv", row.names = F)

write.csv(leftlunomide_codes, file="local_codelists/leftlunomide_codes.csv", row.names = F)

write.csv(mercaptopurine_codes, file="local_codelists/mercaptopurine_codes.csv", row.names = F)

write.csv(methotrexate_codes, file="local_codelists/methotrexate_codes.csv", row.names = F)

write.csv(mycophenolate_codes, file="local_codelists/mycophenolate_codes.csv", row.names = F)

write.csv(penicilliamine_codes, file="local_codelists/penicilliamine_codes.csv", row.names = F)

write.csv(sulfasalazine_codes, file="local_codelists/sulfasalazine_codes.csv", row.names = F)



