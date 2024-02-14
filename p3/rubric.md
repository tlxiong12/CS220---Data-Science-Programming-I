# Project 3 (P3) grading rubric

## Code reviews

- A TA / grader will be reviewing your code after the deadline.
- They will make deductions based on the Rubric provided below.
- To ensure that you don't lose any points in code review, you must review the rubric and make sure that you have followed the instructions provided in the project correctly.

## Rubric

### General guidelines:

- Did not save the notebook file prior to running the cell containing "export". We cannot see your output if you do not save before generating the zip file. This deduction will become stricter for future projects. (-1)

### Question specific guidelines:

- Q1 deductions

  - `prius_id` variable is hard coded as 977 (-5)

- Q2 deductions

  - `num_leaf` variable is hard coded as 11230 (-5)
  - output of `get_id` function is not used as input to `get_sales` function (-3)

- Q3 deductions

  - `max_sales_2017` variable is hard coded as 26500 (-5)
  - `year_max` function is not used (-3)
  - conditionals/iterations are used to get output (-2)

- Q4 deductions

  - `max_sales_2016_to_2018` variable is hard coded as 30200 (-5)
  - `year_max` function is not used (-3)
  - max function is not used or conditionals/iterations are used to get output (-2)

- Q5 deductions

  - `min_sales_model_S` variable is hard coded as 15090 (-5)
  - `sales_min` function is not used (-3)
  - min function is not used in `sales_min` function or conditionals/iterations are used to get output (-2)

- Q6 deductions

  - `min_sales_CV_FFE_NL` variable is hard coded as 4915 (-5)
  - `sales_min` function is not used (-3)
  - min function is not used or conditionals/iterations are used to get output (-2)

- Q7 deductions

  - `sales_avg_prius_2015_to_2019` variable is hard coded as 15765.2 (-5)
  - `sales_avg` function is not used or conditionals/iterations are used to get output (-3)
  - `get_id` function is not used in `sales_avg` function (-1)
  - `get_sales` function is not used in `sales_avg` function (-1)
  - type of the return value of `sales_avg` function is not float (-1)

- Q8 deductions

  - `sales_avg_volt_2015_to_2019` variable is hard coded as 16740.4 (-5)
  - `sales_avg` function is not used or conditionals/iterations are used to get output (-3)

- Q9 deductions

  - `diff_leaf_2018_to_average` variable is hard coded as 798.0 (-5)
  - `sales_avg` function is not used or conditionals/iterations are used to get output (-3)
  - `get_sales` function is not used for getting Nissan Leaf car sales (-1)

- Q10 deductions

  - `sales_sum_2019` variable is hard coded as 82901 (-5)
  - `year_sum` function is not used (-3)
  - Passed more arguments than necessary to `year_sum` function (-1)
  - Default value for year=2019 is changed in `year_sum` function (-1)

- Q11 deductions

  - `sales_sum_2017_to_2019` variable is hard coded as 313783 (-5)
  - `year_sum` function is not used (-3)
  - Passed more arguments than necessary to `year_sum` function (-1)

- Q12 deductions

  - `fusion_average_change` variable is hard coded as -568.5 (-5)
  - `change_per_year` function is not used (-3)
  - Passed more arguments than necessary to `change_per_year` function (-1)
  - Default values for `start_year`=2015, `end_year`=2019 are changed in `change_per_year` function (-1)
  - `get_id` function is not used in `change_per_year` function (-1)
  - `get_sales` function is not used in `change_per_year` function (-1)

- Q13 deductions

  - `volt_average_change` variable is hard coded as -6608.0 (-5)
  - `change_per_year` function is not used (-3)
  - Passed more arguments than necessary to `change_per_year` function (-1)

- Q14 deductions

  - `model_x_average_change` variable is hard coded as 8630.666666666666 (-5)
  - `change_per_year` function is not used (-3)
  - Passed more arguments than necessary to `change_per_year` function (-1)

- Q15 deductions

  - `leaf_sales_in_2021` variable is hard coded as 9913.0 (-5)
  - `estimate_sales` function is not used (-3)
  - `change_per_year` function is not used in `estimate_sales` function (-3)
  - Passed more arguments than necessary to `estimate_sales` function (-1)
  - Default values for `start_year`=2015 and `end_year`=2019 are not specified in `estimate_sales` function (-1)

- Q16 deductions

  - `prius_sales_in_2022` variable is hard coded as 77837.0 (-5)
  - `estimate_sales` function is not used (-3)
  - Required arguments are not passed to `estimate_sales` function (-1)

- Q17 deductions

  - `diff_sales_model_x_2030` variable is hard coded as 57396.25 (-5)
  - `estimate_sales` function is not used (-3)
  - Passed more arguments than necessary to `estimate_sales` function (-1)

- Q18 deductions

  - `diff_sales_leaf_2030` variable is hard coded as -3165.5 (-5)
  - `estimate_sales` function is not used (-3)
  - Passed more arguments than necessary to `estimate_sales` function (-1)

- Q19 deductions

  - `volt_diff_change_per_year` variable is hard coded as -17063.0 (-5)
  - `change_per_year` function is not used (-3)
  - Passed more arguments than necessary to `change_per_year` function (-1)

- Q20 deductions
  - `prius_change_per_year_ratio` variable is hard coded as 1.37023509439786 (-5)
  - `change_per_year` function is not used (-3)
  - Passed more arguments than necessary to `change_per_year` function (-1)
