The `regression` module performs linear regression of one stream (call it `y`) against several others (`x_0, ..., x_n`) over a specified window, i.e., finds the coefficients `b_0, ..., b_n` making the time series `y` as close as possible to the time series `b_0 x_0 + ... + b_n x_n`, with respect to mean squared error. An intercept term is included by default but may be excluded.

The `fit` function has the following parameters. Parameters with no default value are required.

|Parameter name|Type|Description|Default value|
|:---|:---|:---|:---|
|X|list of streams|independent variables in the regression problem|*None*|
|y|stream|dependent variable in the regression problem|*None*|
|window|duration|time window over which to perform the regression|duration('30m')|
|fit_intercept|boolean|whether to include an intercept term|True|


The return value is a dictionary whose contents are described in the following table.

|Key|Type|Description of content|
|:---|:---|:---|
|'coef'|list of streams|list of coefficients, with elements corresponding to elements of the input list `X`|
|'intercept'|stream|intercept term (coefficient of 1 if `fit_intercept=True`, else 0.0)|
|'std_err'|stream|the rolling out-of-sample standard error, computed over a window of the same length as input `window`|
|'R2'|stream|the rolling out-of-sample R^2, again computed over a window of the same length as input `window`|


#### Example usage

~~~~~~~~~~~~~~~~~~~~
from signalfx.stats.linear_model import regression

y = data('cpu.utilization').mean()
X = [data('read_operations').sum(), data('write_operations').sum()]

solution = regression.fit(X, y, window=duration('20m'))

model_estimate = solution['intercept'] + sum(*[solution['coef'][i] * X[i]  for i in range(len(X))])

normalized_residual = ((y - model_estimate) / solution['std_err']).publish('z_score')
~~~~~~~~~~~~~~~~~~~~


Forecasting can be obtained, in the notation of the preceding program, by using, e.g., `X = [y.timeshift('1m'), y.timeshift('2m')]`. The resulting model expresses the current value of `y` as a linear combination of its values one and two minutes ago (and an intercept term); large normalized residuals can then be viewed as anomalies.


#### Notes

The underlying linear algebraic [operations](utils.flow) may be of independent interest.

The `'R2'` can be negative since it compares out-of-sample residuals.

Metadata correlation applies to the union of `y` and the contents of `X`. The common schema of the returned streams is computed from these input schemas.

