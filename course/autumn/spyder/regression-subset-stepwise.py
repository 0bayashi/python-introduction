#!/usr/bin/env python
# coding: utf-8

#%%
# ## Linear Regression: Best Subset and Stepwise Regression
# 
# **Functions**
# 
# `np.linalg.lstsq`, `sklearn.model_selection.cross_val_score`, `sklearn.linear_model.LinearRegression`, `sklearn.model_selection.KFold`
# 
# This notebook shows how Best Subset and Stepwise Regression can be implemented. The motivating example is tracking portfolio construction which replicates a portfolio using other assets. The underlying regression model excludes a constant since we want to track both the shocks and match the mean return.
# 
# $$ R_{i,p} = \beta_1 R_{i,1} + \beta_2 R_{i,2} + \ldots + \beta_k R_{i,k} + \epsilon_{i} $$
# 
# where $R_{i,j}$ are returns on the assets used to construct the tracking portfolio. OLS minimizes the variance of the tracking error (in-sample).

#%%


#%%
# ## Data
# 
# We start by leading the data which have all been downloaded from [Ken French's website]().  In this exercise we will use the Value-weighted Market Return and 12 industry portfolios.

#%%


#%%
# The data is subsetted into 1980 - 2014 (inclusive) and the data from 2015 to the end of the sample will be used to evaluate model performance.

#%%


#%%
# ## Best Subset Regression
# 
# Best subset regression involves fitting all possible model.  Python's `itertools` module has a function `combinations` that will construct all distinct combinations of $n$ items from a collection. This can be used with different $n$ to build all possible models.  Below we see that it outputs list of columns names.
# 
# ### Caution
# The number of distinct models grows at rate $2^p$ and so this code may be very slow when $p$ is modestly large.

#%%


#%%
# We use `lstsq` from `numpy.linalg` to estimate the regression parameters.  This function is quite a bit faster than `OLS` from `statsmodels. It returns multiple outputs but we only need the first which is selected using `[0]`.
# 
# The best model is selected by iterating across all model sizes and retaining the model with the smallest SSE. The variable `best_sse` is initialized to be infinity so that at least one model will always be smaller.
# 
# Finally, we store the columns of the best model in a dictionary where the key is the number of variables in the model. The last line prints the set of models selected.

#%%


#%%
# ## Cross-validation
# We need to cross-validate the set of best models. To do this, we can write a function (see below for a method available through scikit-learn that will simplify this step) so that we can reuse it later. The function defaults to non-random cross-validation which will leave out blocks containing 20% of the data in order. The function can optionally be used to randomly select the data left out.

#%%


#%%
# When we randomize we get different values.  Randomization may select different models.  It usually makes little difference.

#%%


#%%
# We can apply `xval_5fold` to the data to compute the cross-validate SSE, and retain the best. We loop over the keys in the `best_models` and select the contents of the dictionary using `best_models[n_var]`.
# 
# While some of the cross-validated SSEs are very large, many are similar to the best. 

#%%


#%%
# If we use randomization we may select a different model. The alternative model will usually have an SSE that is close to the SSE of the previous model selected.

#%%


#%%
# ## Forward Stepwise Regression
# 
# Forward Stepwise Regression is implemented by tracking the variables that have been included in the model. We then add one variables from those that are excluded to the included and find the model that minimizes the SSE from the next iteration. The is repeated until all variables are added.  The list of included contains the variables in the order they are added, so that `included[:k]` returns the list of included variables in a model containing `k` variables.

#%%


#%%
# Next we cross-validate the FSR sequence of models by looping across the list of included variables, in order.
# 
# We store the cross-validated SSE as a dictionary that we can convert to a `Series`. We can then get the best using `idxmin()` to return the index associated with the smallest cross-validated SSE.

#%%


#%%
# ## Backward Stepwise Regression
# 
# Backward Stepwise Regression is substantially similar to Forward except that we being with the included set contains all columns and then remove one at a time.  We always retain the model with the smallest SSE that has one variable removed from the previous model.

#%%


#%%
# We can then cross-validate the BSR models using the same code as for FSR

#%%


#%%
# ## Using scikit-learn to cross-validate
# 
# scikit-learn is a machine-learning library that can contains codes for many models and tasks. This includes OLS and cross-validation.  Below we show how the function `cross_val_score` can be used to cross-validate a set of linear regression models.

#%%


#%%
# The negative MSE is simply 
# 
# $$ -\frac{SSE}{t} $$
# 
# so it is simple to invert back to SSE. These values are the same as above.

#%%


#%%
# The default cross-validation blocks the data in the order it occurs in the inputs. If randomization is desired it is necessary to pass a cross-validation scheme that will randomize.  We do these here using `KFold` with `shuffle=True`. We also pass a `random_state` seed value to ensure that the cross-validation is reproducible. 

#%%


#%%
# ## Out-of-Sample Evaluation
# 
# Finally, we can look at out-of-sample evaluation.  We simply estimate the regression coefficients in-sample and then use these with the out-of-sample x values. The residuals are the computed from these out-of-sample prediction.

#%%


#%%
# We can also look at the out-of-sample $R^2$ defined as
# 
# $$ 1 - \frac{SSE_{OOS}}{TSS_{OOS}} $$
# 
# where the $SSE_{OOS}$ is the SSE using the predicted values and the $TSS_{OOS}$ is the TSS computed using the in-sample value (without demeaning since the models we are fitting do not include a constant.)

#%%


#%%
# ## Using scikit-learn to produce out-of-sample fits
# 
# scikit-learn is optimized for prediction and so producing out-of-sample prediction is particularly simple. 

#%%

