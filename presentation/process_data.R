library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/Documents/Github/AlcoholTrends_HBSCDNSSSU_EMM/")

### import functions through python
source_python("import_subgroup.py")

# dataset 1
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210810_None_[8, 40, 3, 20]_[0.05, 1.0]_[False, 100]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max']"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers,
                                       remove_data=TRUE)

general_params <- out[[1]]
all_params <- out[[2]]

names(all_params)
names(general_params)

general_params_adapted <- general_params %>%
  mutate(subgroup = rep(50, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(all_params_adapted, general_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

head(data)

write.csv(data, './presentation/data/maxprev.csv', row.names=FALSE)
