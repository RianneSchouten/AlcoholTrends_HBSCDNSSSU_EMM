library(readxl)
library(stringr)
library(tidyverse)
library(ggplot2)
library(mice)
library(reticulate)
library(gridExtra)
library(directlabels)

setwd("C:/Users/20200059/OneDrive - TU Eindhoven/Documents/Github/AlcoholTrends_HBSCDNSSSU_EMM/data_output/HBSC_DNSSSU/MPALC/")

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

# prevalence, max, new figure
date <- "date17032024"
trendvar <- 'prev'
qm <- 'max'
nr_subgroups = 20

general_params <- read_excel(paste0(date,'/',trendvar,'_',qm,'.xlsx'),sheet='general_params_pd') %>%
  select(meting, n, prev, prev_se) %>%
  mutate(subgroup = 50)
for(j in 0:(nr_subgroups-1)){
  params = read_delim(paste0(date,'/',trendvar,'_',qm,'_',j,'.txt')) %>%
    select(meting, n, prev, prev_se) %>%
    mutate(subgroup = j+1)
  general_params <- rbind(general_params,params)
}
data <- general_params %>%
  mutate(year = meting) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup))))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,4,6,11,13,50),]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(linewidth=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=seq(2003, 2019, 2)) + 
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     #labels = c("1", "4", "6", "11", "13", "D"),
                     labels = c("1", "2", "3", "4", "5", "D"),
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

name <- "maxprev.pdf"
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence, max, figure 2
date <- "date18032024"
trendvar <- 'mov_prev_slope'
qm <- 'max'
nr_subgroups = 20

general_params <- read_excel(paste0(date,'/',trendvar,'_',qm,'.xlsx'),sheet='general_params_pd') %>%
  select(meting, n, prev, prev_se, mov_prev, mov_prev_se) %>%
  mutate(subgroup = as.numeric(50))
for(j in 0:(nr_subgroups-1)){
  params = read_delim(paste0(date,'/',trendvar,'_',qm,'_',j,'.txt')) %>%
    select(meting, n, prev, prev_se, mov_prev, mov_prev_se) %>%
    mutate(subgroup = j+1)
  general_params <- rbind(general_params,params)
}
data <- general_params %>%
  mutate(year = meting) %>%
  filter(year < 2019) %>%
  mutate(year = rep(c(1:8), 20 + 1)) %>%
  mutate(subgroup = as.numeric(subgroup)) %>% arrange(subgroup) %>%
  mutate(subgroup = as.factor(subgroup))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,5,6,10,16,50), ]

#pal = c("#fdb462", "#bebada", "#fb8072", "#238b45", "#80b1d3", "#dfc27d", "#1f78b4", "#b3de69", "#ae017e", "#7bccc4", "#636363")
#pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#b3de69", "#636363")
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#ae017e", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(linewidth=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_y_continuous(breaks=seq(0.0,0.8,0.2), limits=c(0.0,0.85)) +
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     #labels = c("1", "2", "3", "6", "11", "D"), 
                     labels = c("1", "2", "3", "4", "6", "D"),
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

name <- "maxmovprevslope.pdf"
ggsave(name, width = 8, height = 5, units = "cm")

# mov avg prevalence, count, figure 3
date <- "date19032024"
trendvar <- 'mov_prev_slope'
qm <- 'countsum'
nr_subgroups = 20

general_params <- read_excel(paste0(date,'/',trendvar,'_',qm,'.xlsx'),sheet='general_params_pd') %>%
  select(meting, n, prev, prev_se, mov_prev, mov_prev_se) %>%
  mutate(subgroup = 50)
for(j in 0:(nr_subgroups-1)){
  params = read_delim(paste0(date,'/',trendvar,'_',qm,'_',j,'.txt')) %>%
    select(meting, n, prev, prev_se, mov_prev, mov_prev_se) %>%
    mutate(subgroup = j+1)
  general_params <- rbind(general_params,params)
}
data <- general_params %>%
  mutate(year = meting) %>%
  mutate(subgroup = reorder(subgroup, sort(as.numeric(subgroup)))) %>%
  filter(year < 2019) %>%
  mutate(year = rep(c(1:8), 20 + 1))

#sel <- data[data$subgroup %in% c(1:25,50), ]
sel <- data[data$subgroup %in% c(1,2,5,9,50), ]
pal = c("#fdb462", "#bebada", "#fb8072", "#80b1d3", "#636363")
#pal <- c(gg_color_hue(nr_subgroups+1), "#636363")
trend_plot <- ggplot(sel, aes(x = year, y = mov_prev, color = subgroup)) + 
  geom_point(size=0.8) + 
  geom_line(size=0.7) + 
  ggtitle(label = "") + #Prevalence of alcohol use among Dutch adolescents") + 
  scale_x_continuous(breaks=1:8,labels=c('03/05', '05/07', '07/09', '09/11', '11/13', '13/15', '15/17', '17/19')) + 
  scale_y_continuous(breaks=seq(0.0,0.8,0.2), limits=c(0.0,0.85)) +
  xlab("") + 
  ylab("") + 
  scale_color_manual(values = pal, 
                     #labels = c("1", "2", "5", "7", "D"),
                     labels = c("1", "2", "3", "4", "D"),
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

name <- "maxmovprevslopecount.pdf"
ggsave(name, width = 8, height = 5, units = "cm")
