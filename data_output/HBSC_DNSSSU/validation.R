library(foreign)
library(tidyverse)
library(ggplot2)
library(lme4)

getwd()
data <- read.spss("../Data/PeilHBSC20032019_MPALC_30.sav", use.value.label=TRUE, to.data.frame=TRUE)
head(data)

# remove younger and older children
data <- data[data$lft > 11 & data$lft < 17, ]
unique(data$lft)
class(data$spijbel)
unique(data$spijbel)
class(data$meting)

# exceptionality type 1
# trend 1, subgroup 1
data$R <- ifelse((data$lft == 12) & (data$cijferleven > 7) & (data$spijbel == '0 uur'), 1, 0)
sum(data$R)
summary <- data %>% group_by(R, meting) %>% summarize(m = mean(mpalc), n = n()) %>%
  mutate(var = (m*(1-m)/(n-1)))
summary %>% ggplot(aes(y = m, color = as.factor(R), x = meting)) + geom_point() + geom_line()
globalmean <- mean(data$mpalc)
groupmeans <- data %>% group_by(R) %>% summarize(m = mean(mpalc))

# glm
# intercept only model
data$meting = data$meting - 2003
summary(glm(data = data, mpalc ~ 1, family = binomial(link="logit")))
lin = -0.59714
exp(lin) / (exp(lin) + 1)
# fixed intercept sg vs sgc
summary(glm(data = data, mpalc ~ R, family = binomial(link="logit")))
lin = -0.44256 - 1.78310 # sg
exp(lin) / (exp(lin) + 1)
lin = -0.44256 # sgc
exp(lin) / (exp(lin) + 1)
# two fixed effects
summary(glm(data = data, mpalc ~ R + meting, family = binomial(link="logit")))
lin = 0.2829 - (0.094859*2019) - 1.839093
exp(lin) / (exp(lin) + 1) # there is variation around the regression line
lin = 0.2829 - (0.094859*2019)
exp(lin) / (exp(lin) + 1)
# fixed effects and interaction
summary(glm(data = data, mpalc ~ R * meting, family = binomial(link="logit")))

#glmm
# random intercept nested groups
# fixed effect of R, fixed effect of meting, random intercept (structure = meting)
summary(glmer(data = data, mpalc ~ R + meting + (1 | meting), family = binomial(link="logit")))
# fixed effect of R, random intercept, random effect of R
summary(glmer(data = data, mpalc ~ R + (R | meting), family = binomial(link="logit")))
summary(glm(data = data, mpalc ~ R, family = binomial(link="logit")))
summary(glmer(data = data, mpalc ~ meting + (meting | R), family = binomial(link="logit")))

# trend 2, subgroup 5
data$R <- ifelse((data$lft < 14) & (data$cijferleven > 6) & (data$spijbel == '0 uur'), 1, 0)
summary(glm(data = data, mpalc ~ R * meting, family = binomial(link="logit")))

# trend 3, subgroup 14
data$R <- ifelse((data$lft > 14), 1, 0)
summary(glm(data = data, mpalc ~ R * meting, family = binomial(link="logit")))

# trend 4, subgroup 19
data$R <- ifelse((data$lft < 15) & (data$lft > 11) & (data$spijbel == '0 uur'), 1, 0)
summary(glm(data = data, mpalc ~ R * meting, family = binomial(link="logit")))

### dfd
mean <- 4.07
sd <- 0.184662
# trend 1 subgroup 1
(38.5 - mean)/sd
# trend 2 subgroup 5
(32 - mean)/sd
# trend 3 subgroup 14
(22.4 - mean)/sd
# trend 4 subgroup 19
(21.6 - mean)/sd

