library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/Documents/Github/AlcoholTrends_HBSCDNSSSU_EMM/")

# prevalence, max
params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20210817_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]_prev.xlsx",
                     sheet = 3)
params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20211214_None_[8, 40, 3, 20]_[0.05, 1.0]_[True, 10]_[0.9, 80]_['prev', 'data', None, None, 'max', None, 'max', 1]_prev.xlsx",
                     sheet = 3)
namesparams <- names(params)
#nrcons <- list(c(1,2,3), c(1,2,3), c(1,2,3), c(1,2,3), 
#               c(1,2,3), c(1,2,3), 
#               c(1,2), c(1,2,3), c(1,2), c(1,2,3), c(1,2,3), 
#               c(1,2), c(1,2,3), c(1), c(1,2),
#               c(1,2), c(1,2,3), c(1,2), c(1,2), c(1,2))

nrcons <- list(c(1,2,3), c(1,2,3), c(1,2,3), 
               c(1,2,3), c(1,2,3), 
               c(1,2), c(1,2), c(1,2), c(1,2,3),
               c(1,2,3), c(1,2), c(1,2),
               c(1), c(1,2), c(1,2), c(1,2),
               c(1,2), c(1), c(1,2), c(1,2))

pal = c("#abdda4", "#fdae61", "#9e0142")
for(i in c(1:20)){
  nrcon <- nrcons[i][[1]]
  nams <- sapply(nrcon, function(x) paste('condition', i, x, sep=""))
  labels <- sapply(nrcon, function(x) paste('condition', x, sep=""))
  sel_params <- params %>% 
    select(meting,  
           nams) %>%
    rename(year = meting) %>%
    gather(group, prev, -c(year))
  min_prev <- min(sel_params$prev)
  max_prev <- max(sel_params$prev)
  ylabels <- seq(round(min_prev, digits=1), round(max_prev, digits=1), by = 0.1)
  conditions_plot <- ggplot(sel_params, aes(x = year, y = prev, color = group)) +
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = paste("Subgroup ", i, sep="")) + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     labels = labels,
                     name = "") + 
  scale_y_continuous(breaks = ylabels) + 
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
        plot.title = element_text(vjust=-8),
        plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
  name <- paste("data_output/HBSC_DNSSSU/MPALC/conditions/maxprevconditions", i, ".pdf", sep="")
  ggsave(name, width = 8, height = 5, units = "cm")
}

# prevalence slope, max
#params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20211215_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 10]_[0.9, 80]_['mov_prev_slope', 'data', None, None, 'max', None, 'max', 1]_mov_prev.xlsx",
#                     sheet = 3)
params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20211215_max_mov_prev.xlsx",
                     sheet = 3)
namesparams <- names(params)
nrcons <- list(c(1), c(1,2), c(1,2), c(1,2,3),
               c(1,2),c(1,2), c(1,2), c(1,2), c(1,2), c(1,2), 
               c(1,2), c(1,2), c(1,2), c(1), c(1,2),
               c(1,2), c(1,2), c(1), c(1,2), c(1,2))

pal = c("#abdda4", "#fdae61", "#9e0142")
for(i in c(1,5,6,10,12,16)){
  nrcon <- nrcons[i][[1]]
  nams <- sapply(nrcon, function(x) paste('condition', i, x, sep=""))
  labels <- sapply(nrcon, function(x) paste('condition', x, sep=""))
  sel_params <- params %>% 
    filter(meting < 2019) %>%
    select(meting,  
           nams) %>%
    rename(year = meting) %>%
    mutate(year = c(1:8)) %>%
    gather(group, mov_prev, -c(year))
  min_prev <- min(sel_params$mov_prev)
  max_prev <- max(sel_params$mov_prev)
  ylabels <- seq(round(min_prev, digits=1), round(max_prev, digits=1), by = 0.1)
  conditions_plot <- ggplot(sel_params, aes(x = year, y = mov_prev, color = group)) +
    geom_point(size=0.8) + 
    geom_line(size=0.7) + 
    ggtitle(label = paste("Subgroup ", i, sep="")) + 
    scale_x_continuous(breaks=1:8,
                       labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
    xlab("") + 
    ylab("") + 
    scale_color_manual(values = pal, 
                       labels = labels,
                       name = "") + 
    scale_y_continuous(breaks = ylabels) + 
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
          plot.title = element_text(vjust=-8),
          plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
  name <- paste("data_output/HBSC_DNSSSU/MPALC/conditions/maxmovprevconditions", i, ".pdf", sep="")
  ggsave(name, width = 8, height = 5, units = "cm")
}

# to see difference in movprevslope
#params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20211221_None_[8, 40, 3, 20]_[0.05, 0.78]_[True, 100]_[0.9, 80]_['mov_prev_slope', 'value', 0.0, False, 'countsum', 0.01, 'max', 4]_mov_prev_slope.xlsx",
#                     sheet = 3)
params <- read_excel("data_output/HBSC_DNSSSU/MPALC/insp_desc_20211221_count_mov_prev_slope.xlsx",
                     sheet = 3)

nrcons <- list(c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),
               c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),
               c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),c(1,2,3),
               c(1,2,3),c(1,2),c(1,2,3),c(1,2,3),c(1,2,3))

pal = c("#abdda4", "#fdae61", "#9e0142")
for(i in c(1,2,5,9)){
  nrcon <- nrcons[i][[1]]
  nams <- sapply(nrcon, function(x) paste('condition', i, x, sep=""))
  labels <- sapply(nrcon, function(x) paste('condition', x, sep=""))
  sel_params <- params %>% 
    filter(meting < 2017) %>%
    select(meting,  
           nams,
           mov_prev_slope) %>%
    mutate_at(vars(-matches('meting')), ~ . - mov_prev_slope) %>%
    select(-mov_prev_slope) %>%
    rename(year = meting) %>%
    mutate(year = c(1:7)) %>%
    gather(group, mov_prev_slope, -c(year))
  min_prev <- min(sel_params$mov_prev_slope)
  max_prev <- max(sel_params$mov_prev_slope)
  ylabels <- seq(round(min_prev, digits=1), round(max_prev, digits=2), by = 0.02)
  conditions_plot <- ggplot(sel_params, aes(x = year, y = mov_prev_slope, color = group)) +
    geom_point(size=0.8) + 
    geom_line(size=0.7) + 
    ggtitle(label = paste("Subgroup ", i, " - Dataset", sep="")) + 
    scale_x_continuous(breaks=1:7,
                       labels=c('03/07', '05/09', '07/11', '09/13', '11/15', '13/17', '15/19')) + 
    xlab("") + 
    ylab("") + 
    scale_color_manual(values = pal, 
                       labels = labels,
                       name = "") + 
    scale_y_continuous(breaks = ylabels) + 
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
          plot.title = element_text(vjust=-8),
          plot.margin = unit(x = c(-2, 1, -2, -2), units = "mm"))
  name <- paste("data_output/HBSC_DNSSSU/MPALC/conditions/maxmovprevdifconditions", i, ".pdf", sep="")
  ggsave(name, width = 8, height = 5, units = "cm")
}



