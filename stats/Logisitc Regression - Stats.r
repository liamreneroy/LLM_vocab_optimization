# Before starting, make sure you have opened a new terminal and typed: radian
# To run the entire script, type: Ctrl+Shift+S, for one line simply Ctrl+Enter
# To modify linter try this page: https://lintr.r-lib.org/articles/lintr.html#configuring-linters

# This script performs a logistic regression on the data from Study 2

# Reference Video (StatQuest)
# https://www.youtube.com/watch?v=C4N3_XJJ-jU&list=PLblh5JKOoLUKxzEP5HA2d-Li7IJkHfXSe&index=7&ab_channel=StatQuestwithJoshStarmer

# Reference Code (StatQuest)
# https://github.com/StatQuest/logistic_regression_demo/blob/master/logistic_regression_demo.R

# References for Explaining Output
# https://quantifyinghealth.com/logistic-regression-in-r-with-categorical-variables/
# https://towardsdatascience.com/simply-explained-logistic-regression-with-example-in-r-b919acb1d6b3
# https://stats.idre.ucla.edu/r/dae/logit-regression/

### INSTALLING PACKAGES ###
## if you see the version is out of date, run: update.packages()

# install.packages("readxl")
# install.packages("ggplot2")
# install.packages("cowplot")

### LOADING PACKAGES ###
library("readxl")
library("ggplot2")
library("cowplot")


### CHECK CURRENT DIRECTORY LOCATION
getwd() 

# Load in Data for State 0/1/2, Jackal/Spot, Pre/Post Learning (All data combined)
regression_data <- read_excel("data/study_results/llm_vocab_study04_prelim_data.xlsx", sheet="formated_data", range = "A1:L2529", col_names = TRUE, col_types = NULL, na = "", skip = 0)

# Look at the data
head(regression_data)

# Remove the first and third column (Value and User ID)
regression_data_trim <- subset(regression_data, select = -c(1, 4, 7, 8, 9, 10, 11))

# Look at the data structure (see what type of data is in each column)
str(regression_data_trim)

# DATA CLEANING
# Facotrs = catagorical data.
# In general, we want to convert ordinal data (which may appear as 'num') to catagorical ('factors')
# In this case, we dont have any ordinal data, so we dont need to convert anything
# We do however have 'chr' which needs to be changed to 'factors' (catagorical)

# Replace the binary 0/1 output for 'Correct' with "Correct" and "Incorrect" and change to factor
regression_data_trim$Correct <- ifelse(test=regression_data_trim$Correct == 1, yes="=Correct", no="=Incorrect")
regression_data_trim$Correct <- factor(regression_data_trim$Correct) # Now convert to a factor


# Change GroupOrder to factors (catagorical)
regression_data_trim[regression_data_trim$GroupOrder == "three_then_five",]$GroupOrder <- "=three_then_five"
regression_data_trim[regression_data_trim$GroupOrder == "five_then_three",]$GroupOrder <- "=five_then_three"
regression_data_trim$GroupOrder <- factor(regression_data_trim$GroupOrder, levels=c("=five_then_three", "=three_then_five"))


# # Change VocabularySize to factors (catagorical)
regression_data_trim[regression_data_trim$VocabularySize == "five",]$VocabularySize <- "=five"
regression_data_trim[regression_data_trim$VocabularySize == "three",]$VocabularySize <- "=three"
regression_data_trim$VocabularySize <- factor(regression_data_trim$VocabularySize, levels=c("=five", "=three"))


# Change GenerationMethod to factors (catagorical)
# Here we specify the levels to be in a specific order (Random Human GPT4) therefor random is the reference level
regression_data_trim[regression_data_trim$GenerationMethod == "iso",]$GenerationMethod <- "=iso"
regression_data_trim[regression_data_trim$GenerationMethod == "non",]$GenerationMethod <- "=proxy"
regression_data_trim[regression_data_trim$GenerationMethod == "emd",]$GenerationMethod <- "=proxy+emd"
regression_data_trim[regression_data_trim$GenerationMethod == "dyn",]$GenerationMethod <- "=proxy+kin"
regression_data_trim$GenerationMethod <- factor(regression_data_trim$GenerationMethod, levels=c("=iso", "=proxy", "=proxy+emd", "=proxy+kin"))


# Look at the data structure again (see what type of data is in each column)
str(regression_data_trim)


# Good practice: check that there is a good amount of samples for correct and incorrect responses
table(regression_data_trim$Correct)


# Good practice: exclude variables that only have 1 or 2 samples in a category
# since +/- one or two samples can have a large effect on the odds/log(odds)
# We only need to do this for our data that is catagorical (not continuous)
xtabs(~ Correct + GroupOrder, data=regression_data_trim)
xtabs(~ Correct + VocabularySize, data=regression_data_trim)
xtabs(~ Correct + GenerationMethod, data=regression_data_trim)


# First let check if there are any interactions between our variables (A, B, C, AB, AC, BC, etc... )
interactions_logit <- glm(Correct ~ GroupOrder + VocabularySize + GenerationMethod +
  (GroupOrder * VocabularySize) + (GroupOrder * GenerationMethod) +
  (VocabularySize * GenerationMethod),
  data = regression_data_trim, family = "binomial")
summary(interactions_logit)


# Now lets run a logistic regression using the glm function
# Lets look at the model with all variables
regression_logit <- glm(Correct ~ GroupOrder + VocabularySize + GenerationMethod + (VocabularySize * GenerationMethod),
                         data=regression_data_trim, family='binomial')

summary(regression_logit)


