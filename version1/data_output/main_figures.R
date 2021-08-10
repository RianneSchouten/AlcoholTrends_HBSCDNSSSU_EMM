library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/Documents/Github/analysis_alcoholtrends_emm_hbscpeil/")

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

# first, quality measure
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

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
  mutate(subgroup = rep(0, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(general_params_adapted, all_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

prevalence_plot <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence distribution for subgroups with exceptional prevalence") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  theme(legend.position = "none")

prevalence_plot_with_legend <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence for subgroups with exceptional prevalence") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))

prevalence_plot_with_legend

mean_prevalence_plot <- ggplot(data, aes(x = year+1, y = mean, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Mean prevalence for subgroups with exceptional prevalence") + 
  scale_x_continuous(breaks=seq(2004, 2018, 2), limits=c(2004,2018)) + 
  xlab("Weighted average per two years") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") +
  theme(legend.position = "none")

mean_prevalence_plot

shared_legend <- extract_legend(prevalence_plot_with_legend)

pdf("data_output/MPALC_70/exceptional_prevalences.pdf")
grid.arrange(grobs = list(prevalence_plot, mean_prevalence_plot, shared_legend), 
             layout_matrix = rbind(c(1,1,1,1,1,1,3), c(2,2,2,2,2,2,3)))
dev.off()

# make a plot with a selection
sg_sel <- c(0, 1, 2, 3)
data_sel <- data %>%
  filter(subgroup %in% sg_sel)
pal_sel <- pal[sg_sel + 1]

prevalence_plot_with_legend <- ggplot(data_sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence for selected subgroups with exceptional prevalence") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal_sel, 
                     labels = c("D", as.character(sg_sel[2:length(sg_sel)])),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))  

prevalence_plot_with_legend

pdf("data_output/MPALC_70/exceptional_prevalences_subselection.pdf", height=5, width=7)
grid.arrange(prevalence_plot_with_legend)
dev.off()

### second, quality measure
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

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
  mutate(subgroup = rep(0, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(general_params_adapted, all_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

prevalence_plot <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence distribution for subgroups with exceptional slope") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  theme(legend.position = "none")

prevalence_plot

prevalence_plot_with_legend <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence distribution for subgroups with exceptional slope") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))

mean_prevalence_plot <- ggplot(data, aes(x = year+1, y = mean, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Mean prevalence distribution for subgroups with exceptional slope") + 
  scale_x_continuous(breaks=seq(2004, 2018, 2), limits=c(2004,2018)) + 
  xlab("Weighted average per two years") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") +
  theme(legend.position = "none")

shared_legend <- extract_legend(prevalence_plot_with_legend)

pdf("data_output/MPALC_70/exceptional_slopes.pdf")
grid.arrange(grobs = list(prevalence_plot, mean_prevalence_plot, shared_legend), 
             layout_matrix = rbind(c(1,1,1,1,1,1,3), c(2,2,2,2,2,2,3)))
dev.off()

# make a plot with a selection
sg_sel <- c(0, 1, 2, 3, 5, 11, 12, 13, 16, 17, 19, 20)
data_sel <- data %>%
  filter(subgroup %in% sg_sel)
pal_sel <- pal[sg_sel + 1]

mean_plot_with_legend <- ggplot(data_sel, aes(x = year+1, y = mean, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Mean prevalence for selected subgroups with exceptional slope") + 
  scale_x_continuous(breaks=seq(2004, 2018, 2), limits=c(2004,2018)) + 
  xlab("Weighted average per two years") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal_sel, 
                     labels = c("D", as.character(sg_sel[2:length(sg_sel)])),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))  

mean_plot_with_legend

pdf("data_output/MPALC_70/exceptional_slopes_subselection.pdf", height=5, width=7)
grid.arrange(mean_plot_with_legend)
dev.off()

### third, quality measure nr_prev_zero
nr_subgroups = 19.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c("#636363", gg_color_hue(nr_subgroups+1))

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
  mutate(subgroup = rep(0, 9)) %>%
  select(-min_size)
all_params_adapted <- all_params %>% select(-size) %>%
  mutate(subgroup = as.numeric(subgroup) + 1)
data <- rbind(general_params_adapted, all_params_adapted) %>%
  mutate(year = rep(seq(2003, 2019, 2), length(subgroup_numbers) + 1)) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

prevalence_plot <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence distribution for subgroups with horizontal trends") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  theme(legend.position = "none")

prevalence_plot

prevalence_plot_with_legend <- ggplot(data, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Prevalence distribution for subgroups with horizontal trends") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("Year") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))

mean_prevalence_plot <- ggplot(data, aes(x = year+1, y = mean, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Mean prevalence distribution for subgroups with horizontal trends") + 
  scale_x_continuous(breaks=seq(2004, 2018, 2), limits=c(2004,2018)) + 
  xlab("Weighted average per two years") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal, 
                     labels = c("D", "1", "2", "3", "4", "5", "6", "7",
                                "8", "9", "10", "11", "12", "13", "14", "15",
                                "16", "17", "18", "19", "20"),
                     name = "Subgroup") +
  theme(legend.position = "none")

shared_legend <- extract_legend(prevalence_plot_with_legend)

pdf("data_output/MPALC_70/exceptional_slopes_zero.pdf")
grid.arrange(grobs = list(prevalence_plot, mean_prevalence_plot, shared_legend), 
             layout_matrix = rbind(c(1,1,1,1,1,1,3), c(2,2,2,2,2,2,3)))
dev.off()

# make a plot with a selection
sg_sel <- c(0, 1, 2, 3, 4, 5, 6, 8)
data_sel <- data %>%
  filter(subgroup %in% sg_sel)
pal_sel <- pal[sg_sel + 1]

mean_plot_with_legend <- ggplot(data_sel, aes(x = year+1, y = mean, color = subgroup)) + 
  geom_point(size=1.2) + 
  geom_line(size=1) + 
  ggtitle(label = "Mean prevalence for selected subgroups with exceptional slope") + 
  scale_x_continuous(breaks=seq(2004, 2018, 2), limits=c(2004,2018)) + 
  xlab("Weighted average per two years") + 
  ylab("Prevalence Alcohol Use") + 
  scale_color_manual(values = pal_sel, 
                     labels = c("D", as.character(sg_sel[2:length(sg_sel)])),
                     name = "Subgroup") + 
  guides(color=guide_legend(ncol=1))  

mean_plot_with_legend

pdf("data_output/MPALC_70/exceptional_slopes_zero_subselection.pdf", height=5, width=7)
grid.arrange(mean_plot_with_legend)
dev.off()

### fourth pareto front
nr_subgroups = 8.0
subgroup_numbers <- c(0.0:nr_subgroups)
pal <- c(gg_color_hue(nr_subgroups+1), "#636363")

outcome_attr <- 'MPALC_70'
file_name <- "MPALC_70_['nr_mean_zero']_[8, 40, 3, 25, False, 3]_[0.05]_[None, None]_[0.9, 80]_20210505"

out <- import_subgroup_from_resultlist(outcome_attr=outcome_attr,
                                       file_name=file_name, 
                                       subgroup_numbers=subgroup_numbers)
