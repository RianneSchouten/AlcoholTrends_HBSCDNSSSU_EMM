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
#file_name <- "20210817_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]"
file_name <- "20211214_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers,
                                       remove_data=FALSE,
                                       incomplete=TRUE)

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

write.csv(data, './supplement/data/maxprev.csv', row.names=FALSE)

# dataset 2
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
#file_name <- "20211021_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 10]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None, 'max', 1]"
file_name <- "20211215_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 10]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None, 'max', 1]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers,
                                       remove_data=FALSE,
                                       incomplete=TRUE)

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
  #filter(meting < 2019) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), 
  #                  length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

head(data)

write.csv(data, 'supplement/data/maxmovprevslope.csv', row.names=FALSE)

# dataset 3
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20211221_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, False, 'countsum', 0.01, 'max', 4]"

out <- import_subgroup_from_resultlist(data_name=data_name,
                                       trend_name=trend_name,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers,
                                       remove_data=FALSE,
                                       incomplete=TRUE)

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
  #filter(meting < 2019) %>%
  #mutate(year = rep(c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19'), 
  #                  length(subgroup_numbers) + 1)) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

head(data)

write.csv(data, 'supplement/data/maxmovprevslopecount.csv', row.names=FALSE)
