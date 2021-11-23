library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/Documents/Github/AlcoholTrends_HBSCDNSSSU_EMM/")

gg_color_hue <- function(n) {
  hues = seq(15, 375, length = n + 1)
  hcl(h = hues, l = 65, c = 100)[1:n]
}

extract_legend <- function(my_ggp) {
  step1 <- ggplot_gtable(ggplot_build(my_ggp))
  step2 <- which(sapply(step1$grobs, function(x) x$name) == "guide-box")
  step3 <- step1$grobs[[step2]]
  return(step3)
}

### import functions through python
source_python("import_subgroup.py")

# prevalence, max, new figure
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20210817_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]"
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

#sel <- data[data$subgroup %in% c(1:25,50), ]
#sel <- data[data$subgroup %in% c(1,5,7,14,19,50), ]
sel <- data[data$subgroup %in% c(1,5,7,19,50), ]
#pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
pal = c("#fdb462", "#bebada", "#fb8072", "#b3de69", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     labels = c("1", "5", "7", "19", "D"),
                     #labels = c("1", "2", "3", "4", "D"),
                     name = "") + 
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- "data_output/HBSC_DNSSSU/MPALC/maxprev.pdf"
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence, max, figure 2
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20211021_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 10]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None, 'max', 1]"
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
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup)))) %>%
  filter(year < 2019) %>%
  mutate(year = rep(c(1:8), 20 + 1))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,5,7,11,12,14,15,17,18,20,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#238b45", "#80b1d3", "#dfc27d", "#1f78b4", "#b3de69", "#ae017e", "#7bccc4", "#636363")
#pal = c("#fdb462", "#bebada", "#fb8072", "#b3de69", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  #scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_y_continuous(breaks=seq(0.0,0.8,0.2), limits=c(0.0,0.85)) +
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     labels = c("1", "5", "7", "11", "12", "14", "15", "17", "18", "20", "D"),
                     #labels = c("1", "2", "3", "4", "D"),
                     name = "") + 
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- "data_output/HBSC_DNSSSU/MPALC/maxmovprevslope.pdf"
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence, count, figure 3
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)

data_name <- 'HBSC_DNSSSU'
trend_name <- 'MPALC'
file_name <- "20211021_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 10]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, False, 'count', 0.01, 'max', 1]"
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
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup)))) %>%
  filter(year < 2019) %>%
  mutate(year = rep(c(1:8), 20 + 1))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,2,3,5,6,50), ]
#pal = c("#fdb462", "#bebada", "#fb8072", "#238b45", "#80b1d3", "#dfc27d", "#1f78b4", "#b3de69", "#ae017e", "#7bccc4", "#636363")
pal = c("#fdb462", "#bebada", "#fb8072", "#238b45", "#80b1d3", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  #scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_y_continuous(breaks=seq(0.0,0.8,0.2), limits=c(0.0,0.85)) +
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     labels = c("1", "2", "3", "5", "6", "D"),
                     name = "") + 
  guides(color = guide_legend(nrow=1, override.aes = list(size = 0.7)),
         shape = guide_legend(override.aes = list(size = 0.7))) + 
  theme_bw(base_size=7) + 
  theme(legend.position="top",
        legend.justification="right",
        legend.box.margin = margin(0,0,-0.2,0, "line"),
        panel.grid.major.x = element_blank(),
        panel.grid.minor.x = element_blank(),
        panel.grid.minor.y = element_blank(),
        legend.text  = element_text(size = 7),
        legend.key.width = unit(0.2,"cm"),
        legend.key.size = unit(0.2,"cm"),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
trend_plot

name <- "data_output/HBSC_DNSSSU/MPALC/maxmovprevslopecount.pdf"
ggsave(name, width = 8, height = 5, units = "cm")
