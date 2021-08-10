library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/")

### import functions through python
source_python("import_subgroup.py")

# dataset 1
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

outcome_attr <- 'MPALC_70'
file_name <- "MPALC_70_['max_prev']_[8, 40, 3, 20]_[0.05]_[0.9, 80]"

out <- import_subgroup_from_resultlist(outcome_attr=outcome_attr,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)

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

# dataset 2

nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

outcome_attr <- 'MPALC_70'
file_name <- "MPALC_70_['max_prev_slope']_[8, 40, 3, 20]_[0.05]_[0.9, 80]"

out <- import_subgroup_from_resultlist(outcome_attr=outcome_attr,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)

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

write.csv(data, './presentation/data/maxprevslope.csv', row.names=FALSE)

# dataset 3

nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

outcome_attr <- 'MPALC_70'
file_name <- "MPALC_70_['nr_mean_zero']_[8, 40, 3, 20]_[0.05]_[0.9, 80]"

out <- import_subgroup_from_resultlist(outcome_attr=outcome_attr,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)

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

write.csv(data, './presentation/data/maxmovprevslopecount.csv', row.names=FALSE)

# dataset 4

setwd('C:/Users/20200059/Documents/Github/EMM_RCS/')
source_python("import_subgroup.py")

nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210605_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)

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

write.csv(data, 'C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/presentation/data/maxmovprevslope.csv', row.names=FALSE)

