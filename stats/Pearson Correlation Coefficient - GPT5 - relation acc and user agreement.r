# Before starting, make sure you have opened a new terminal and typed: radian
# To run the entire script, type: Ctrl+Shift+S, for one line simply Ctrl+Enter
# To modify linter try this page: https://lintr.r-lib.org/articles/lintr.html#configuring-linters

# This script calculates Pearson's correlation coefficient and Spearman's Rank Correlation 
# Coefficient to measure the linear relationship between the two data series

# These methods will still work even if the values in the two series are on different scales
# because correlation measures relative relationships, not absolute values.

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

data_series1 <- c(92,81,89,97,92,94,87,93,78,93,89,96,93,89,92)  # LLM-Proxy Alignment
data_series2 <- c(73,33,40,52,32,65,55,48,18,27,2,2,17,7,18)  # User Study 03 Classification Accuracy



# GPT5.1 Model | PEARSON CORRELATION COEFFICIENT CALCULATION ### 
# Pearson correlation ranges from -1 to 1, measuring linear relationship between two series.
# Values near 1 indicate a strong positive relationship (as X increases, Y increases).
# Values near -1 indicate a strong negative relationship (as X increases, Y decreases).
# Values around 0 indicate little or no linear relationship.
# As a rough guide: |r| > 0.7 is strong, 0.3–0.7 is moderate, and < 0.3 is weak.

pearson_test <- cor.test(data_series1, data_series2, method = "pearson")
cat(sprintf("Pearson correlation coefficient: %.4f, p-value: %.4e\n", pearson_test$estimate, pearson_test$p.value))




# Scatter plot
plot(data_series1, data_series2, main = "LLM-Proxy Alignment vs Human Classification Accuracy",
     xlab = "LLM-Proxy Alignment", ylab = " Human Classification Accuracy", pch = 19, col = "darkgreen")
abline(lm(data_series2 ~ data_series1), col = "red", lwd = 3)
grid() 



# # Calculate Spearman rank correlation coefficient
# spearman_test <- cor.test(data_series1, data_series2, method = "spearman")
# cat(sprintf("Spearman correlation coefficient: %.4f, p-value: %.4e\n", spearman_test$estimate, spearman_test$p.value))
