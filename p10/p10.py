#!/usr/bin/env python
# coding: utf-8
import otter
# nb_name should be the name of your notebook without the .ipynb extension
nb_name = "p10"
py_filename = nb_name + ".py"
grader = otter.Notebook(nb_name + ".ipynb")

import p10_test

# # Project 10: Stars and Planets

# ## Learning Objectives:
#
# In this project, you will demonstrate how to:
#
# * use `os` module to get information of files in a directory,
# * use `os` module to get paths of files,
# * look up data between JSON and CSV files using unique keys,
# * read JSON and CSV files to store data to `namedTuple` objects,
# * clean up missing values and handle cases when the file is too corrupt to parse,
#
# **Please go through [lab-p10](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/tree/main/lab-p10) before working on this project.** The lab introduces some important techniques related to this project.

# ## Note on Academic Misconduct:
#
# **IMPORTANT**: p10 and p11 are two parts of the same data analysis. You **cannot** switch project partners between these two projects. That is if you partner up with someone for p10, you have to sustain that partnership until end of p11. Now may be a good time to review [our course policies](https://cs220.cs.wisc.edu/f22/syllabus.html).

# ## Testing your code:
#
# Along with this notebook, you must have downloaded the file `p10_test.py`. If you are curious about how we test your code, you can explore this file, and specifically the value of the variable `expected_json`, to understand the expected answers to the questions.

# ## Setup:
#
# Before proceeding much further, download `data.zip` and extract it to a directory on your
# computer (using [Mac directions](http://osxdaily.com/2017/11/05/how-open-zip-file-mac/) or
# [Windows directions](https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files)).
#
# You need to make sure that the project files are stored in the following structure:
#
# ```
# +-- p10.ipynb
# +-- p10_test.py
# +-- data
# |   +-- .DS_Store
# |   +-- .ipynb_checkpoints
# |   +-- mapping_1.json
# |   +-- mapping_2.json
# |   +-- mapping_3.json
# |   +-- mapping_4.json
# |   +-- mapping_5.json
# |   +-- planets_1.csv
# |   +-- planets_2.csv
# |   +-- planets_3.csv
# |   +-- planets_4.csv
# |   +-- planets_5.csv
# |   +-- stars_1.csv
# |   +-- stars_2.csv
# |   +-- stars_3.csv
# |   +-- stars_4.csv
# |   +-- stars_5.csv
# ```
#
# Make sure that the files inside `data.zip` are inside the `data` directory. If you place your files inside some other directory, then there is a possibility that your code will **fail on Gradescope** even after passing local tests.

# ## Project Description:
#
# Cleaning data is an important part of a data scientist's work cycle. As you have already seen, the data we will be analyzing in p10 and p11 has been split up into 15 different files of different formats. Even worse, as you shall see later in this project, some of these files have been corrupted, and lots of data is missing. Unfortunately, in the real world, a lot of data that you will come across will be in rough shape, and it is your job to clean it up before you can analyze it. In p10, you will combine the data in these different files to create a few manageable data structures, which can be easily analyzed. In the process, you will also have to deal with broken CSV files (by skipping rows with broken data), and broken JSON files (by skipping the files entirely).
#
# After you create these data structures, in p11, you will dive deeper by analyzing this data and arrive at some exciting conclusions about various planets and stars outside our Solar System.

# ## The Data:
#
# In p10 and p11, you will be studying stars and planets outside our Solar System using this dataset from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars). You will use Python to ask some interesting questions about the laws of the universe and explore the habitability of other planets in our universe. The raw data from the [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=PSCompPars) has been parsed and stored in multiple different files of different formats. You can find these files inside `data.zip`.
#
# You can open each of these files using Microsoft Excel or some other Spreadsheet viewing software to see how the data is stored. For example, these are the first three rows of the file `stars_1.csv`:
#
# |Name|Spectral Type|Stellar Effective Temperature [K]|Stellar Radius [Solar Radius]|Stellar Mass [Solar mass]|Stellar Luminosity [log(Solar)]|Stellar Surface Gravity [log10(cm/s**2)]|Stellar Age [Gyr]|
# |----|-------------|---------------------------------|-----------------------------|-------------------------|-------------------------------|----------------------------------------|-----------------|
# |11 Com|G8 III|4742.00|19.00|2.70|2.243|2.31||
# |11 UMi|K4 III|4213.00|29.79|2.78|2.430|1.93|1.560|
# |14 And|K0 III|4813.00|11.00|2.20|1.763|2.63|4.500|
#
# As you might have already guessed, this file contains data on a number of *stars* outside our solar system along with some important statistics about these stars. The columns here are as follows:
#
# - `Name`: The name given to the star by the International Astronomical Union,
# - `Spectral Type`: The Spectral Classification of the star as per the Morgan–Keenan (MK) system,
# - `Stellar Effective Temperature [K]`: The temperature of a black body (in units of Kelvin) that would emit the observed radiation of the star,
# - `Stellar Radius [Solar Radius]`: The radius of the star (in units of the radius of the Sun),
# - `Stellar Mass [Solar mass]`: The mass of the star (in units of the mass of the Sun),
# - `Stellar Luminosity [log(Solar)]`: The total amount of energy radiated by the star each second (represented by the logarithm of the energy radiated by the Sun in each second),
# - `Stellar Surface Gravity [log10(cm/s**2)]`: The acceleration due to the gravity of the Star at its surface (represented by the logarithm of the acceleration measured in centimeters per second squared),
# - `Stellar Age [Gyr]`: The total age of the star (in units of Giga years, i.e., billions of years).
#
# The four other files `stars_2.csv`, `stars_3.csv`, `stars_4.csv`, and `stars_5.csv` also store similar data in the same format. At this stage of the project, it is alright if you do not understand what these columns mean - they will be explained to you when they become necessary (in p11).
#
# On the other hand, here are the first three rows of the file `planets_1.csv`:
#
# |Planet Name|Discovery Method|Discovery Year|Controversial Flag|Orbital Period [days]|Planet Radius [Earth Radius]|Planet Mass [Earth Mass]|Orbit Semi-Major Axis [au]|Eccentricity|Equilibrium Temperature [K]|Insolation Flux [Earth Flux]|
# |-----------|----------------|--------------|------------------|---------------------|----------------------------|------------------------|---------------------------|------------|---------------------------|----------------------------|
# |11 Com b|Radial Velocity|2007|0|326.03|12.1|6165.6|1.29|0.231|||
# |11 UMi b|Radial Velocity|2009|0|516.21997|12.3|4684.8142|1.53|0.08|||
# |14 And b|Radial Velocity|2008|0|185.84|12.9|1525.5|0.83|0|||
#
# This file contains data on a number of *planets* outside our solar system along with some important statistics about these planets. The columns here are as follows:
#
# - `Planet Name`: The name given to the planet by the International Astronomical Union,
# - `Discovery Method`: The method by which the planet was discovered,
# - `Discovery Year`: The year in which the planet was discovered,
# - `Controversial Flag`: Indicates whether the status of the discovered object as a planet was disputed at the time of discovery, 
# - `Orbital Period [days]`: The amount of time (in units of days) it takes for the planet to complete one orbit around its star,
# - `Planet Radius [Earth Radius]`: The radius of the planet (in units of the radius of the Earth),
# - `Planet Mass [Earth Mass]`: The mass of the planet (in units of the mass of the Earth),
# - `Orbit Semi-Major Axis [au]`: The semi-major axis of the planet's elliptical orbit around its host star (in units of Astronomical Units),
# - `Eccentricity`: The eccentricity of the planet's orbit around its host star,
# - `Equilibrium Temperature [K]`: The temperature of the planet (in units of Kelvin) if it were a black body heated only by its host star,
# - `Insolation Flux [Earth Flux]`:  The amount of radiation the planet receives from its host star per unit of area (in units of the Insolation Flux of the Earth from the Sun).
#
# The four other files `planets_2.csv`, `planets_3.csv`, `planets_4.csv`, and `planets_5.csv` also store similar data in the same format. At this stage of the project, it is alright if you do not understand what these columns mean - they will be explained to you when they become necessary (in p11).
#
#
# Finally, if you take a look at `mapping_1.json` (you can open json files using any Text Editor), you will see that the first three entries look like this:
#
# ```
# {"11 Com b": "11 Com", "11 UMi b": "11 UMi", "14 And b": "14 And", ...}
# ```
#
# This file contains a *mapping* from each *planet* in `planets_1.csv` to the *star* in `stars_1.csv` that the planet orbits. Similarly, `mapping_2.json` contains a *mapping* from each *planet* in `planets_2.csv` to the *star* in `stars_2.csv` that the planet orbits. The pattern also holds true for `mapping_3.json`, `mapping_4.json`, and `mapping_5.json`.

# ## Project Requirements:
#
# You **may not** hardcode indices in your code, unless the question explicitly. If you open your `.csv` files with Excel, manually count through the rows and use this number to loop through the dataset, this is also considered as hardcoding. We'll **manually deduct** points from your autograder score on Gradescope during code review.
#
# **Store** your final answer for each question in the **variable specified for each question**. This step is important because Otter grades your work by comparing the value of this variable against the correct answer.
#
# For some of the questions, we'll ask you to write (then use) a function to compute the answer. If you compute the answer **without** creating the function we ask you to write, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Functions:
# - `star_cell`
# - `get_stars`
# - `planet_cell`
# - `get_planets`
#
# In this project, you will also be required to define certain **data structures**. If you do not create these data structures exactly as specified, we'll **manually deduct** points from your autograder score on Gradescope, even if the way you did it produced the correct answer.
#
# Required Data Structures:
# - `Star` (**namedtuple**)
# - `stars_dict` (**dictionary** mapping **strings** to `Star` objects)
# - `Planet` (**namedtuple**)
# - `planets_list` (**list** of `Planet` objects)
#
# In addition, you are also **required** to follow the requirements below:
#
# * You **must** never use the output of the `os.listdir` function directly. You **must** always first remove all files and directories that start with `"."`, and sort the list before doing anything with it.
# * You are **not** allowed to use *bare* `try/except` blocks. In other words, you can **not** use `try/except` without explicitly specifying the type of exceptions that you want to catch.
# * You are **only** allowed to use Python commands and concepts that have been taught in the course prior to the release of p10. In particular, this means that you are **not** allowed to use **modules** like `pandas` to answer the questions in this project.
#
# You are also **required** to follow good coding practices, such as the following:
#
# * Do **not** use meaningless names for variables or functions (e.g. uuu = "my name").
# * Do **not** write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
# * Avoid **inappropriate** use of data structures. For example, using a for loop to search for a corresponding value in a dictionary with a given key instead of using dictname[key] directly.
# * Do **not** name variables or functions as python keywords or built-in functions. Bad example: str = "23".
# * Do **not** define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
# * Do **not** leave in irrelevant output or test code that we didn't ask for.
#
# We will **manually deduct** points if you do **not** follow these guidelines.
#
# For more details on what will cause you to lose points during code review and specific requirements, please take a look at the [Grading rubric](https://git.doit.wisc.edu/cdis/cs/courses/cs220/cs220-f22-projects/-/blob/main/p10/rubric.md).

# ## Questions and Functions:
#
# Let us start by importing all the modules we will need for this project.
# it is considered a good coding practice to place all import statements at the top of the notebook
# please place all your import statements in this cell if you need to import any more modules for this project
import math
import csv
import pandas
import os
from collections import namedtuple
import json
# ### File handling:
#
# In the next questions, you will be using functions in the `os` module to make **lists** of files and paths in the `data` directory. All your **lists** **must** satisfy the following conditions:
#
# * Any files with names beginning with `"."` **must** be **excluded**.
# * The list **must** be **explicitly** sorted in **alphabetical** order.
#
# You may consider writing a single function to answer several questions, but this is **not required**. If you want to define such a function, you can insert a new cell in your notebook under this cell, and define the function there.
#
# **Hint**: Things that change for different questions can often be represented with parameters.

# **Question 1:** What are the **names** of the files present in the `data` directory
#
# Your output **must** be a **list** of **strings** representing the **names** of the files.

data = os.listdir('data')

# compute and store the answer in the variable 'files_in_data', then display it
files_in_data = []
for idx in data:
    if idx[0] != ".":
        files_in_data.append(idx)
files_in_data.sort()
files_in_data
grader.check("q1")

# **Question 2:** What are the **relative paths** of all the files in the `data` directory?
#
# Your output **must** be a **list** of **strings** representing the **paths** of the files.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# compute and store the answer in the variable 'file_paths', then display it
file_paths = []
for idx in files_in_data:
    test = os.path.join('data', idx)
    file_paths.append(test)
file_paths
grader.check("q2")

# **Question 3:** What are the **relative paths** of all the **JSON files** present in `data` directory?
#
# Your output **must** be filtered to **only** include files ending in `.json`.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# compute and store the answer in the variable 'json_file_paths', then display it
json_file_paths = []
for idx in file_paths:
    if idx[-4:] == "json":
        json_file_paths.append(idx)
json_file_paths
grader.check("q3")

# **Question 4:** What are the **relative paths** of all the files present in `data` directory, that **begin** with the phrase `'stars'`?
#
# Your output **must** be filtered to **only** include files start with `stars`.
#
# **Warning:** Please **do not hardcode** `"/"` or `"\"` in your path because doing so will cause your function to **fail** on a computer that's not using the same operating system as yours. This may result in your code failing on Gradescope.

# compute and store the answer in the variable 'stars_paths', then display it
stars_paths = []
for idx in file_paths:
    if idx[5:10] == 'stars':
        stars_paths.append(idx)
sorted(stars_paths)
stars_paths
grader.check("q4")

# ### Data Structure 1: namedtuple `Star`
#
# You will be using namedtuples to store the data in the `stars_1.csv`, ..., `stars_5.csv` files. Before you start reading these files however, you **must** create a new `Star` type (using namedtuple). It **must** have the following attributes:
#
# * `spectral_type`
# * `stellar_effective_temperature`
# * `stellar_radius`
# * `stellar_mass`
# * `stellar_luminosity`
# * `stellar_surface_gravity`
# * `stellar_age`

# +
# define the namedtuple 'Star' here
# we have done this one for you

# define the list of attributes we want in our namedtuple
star_attributes = ['spectral_type',
                  'stellar_effective_temperature',
                  'stellar_radius',
                  'stellar_mass',
                  'stellar_luminosity',
                  'stellar_surface_gravity',
                  'stellar_age']

# create the namedtuple type 'Star' with the correct attributes
Star = namedtuple("Star", star_attributes)
# +
# run this following cell to initialize and test an example Star object
# if this cell fails to execute, you have likely not defined the namedtuple 'Star' correctly

sun = Star('G2 V', 5780.0, 1.0, 1.0, 0.0, 4.44, 4.6)

sun
# -

grader.check("star_object")


# ### Creating `Star` objects
#
# Now that we have created the `Star` namedtuple, our next objective will be to read the files `stars_1.csv`, ..., `stars_5.csv` and create `Star` objects out of all the stars in there. In order to process the CSV files, you will first need to copy/paste the `process_csv` function you have been using since p6.

# # copy & paste the process_csv file from previous projects here
def process_csv(filename):
    example_file = open(filename, encoding="utf-8")
    example_reader = csv.reader(example_file)
    example_data = list(example_reader)
    example_file.close()
    return example_data


# You are now ready to read the data in `stars_1.csv` using `process_csv` and convert the data into `Star` objects. In the cell below, you **must** read the data in `stars_1.csv` and extract the **header** and the non-header **rows** of the file.
#
# **Warning:** You **must** use the **relative path** of the file to read the file. If you **hardcode** the **absolute path**, your code will pass on your computer, but **fail** on the testing computer.

# +
# replace the ... with your code

stars_1_csv = process_csv(os.path.join("data", "stars_1.csv")) # read the data in 'stars_1.csv'
stars_header = stars_1_csv[0]
stars_1_rows = stars_1_csv[1:]
# -

stars_header


# If you wish to **verify** that you have read the file and defined the variables correctly, you can check that `stars_header` has the value:
#
# ```python
# ['Name', 'Spectral Type', 'Stellar Effective Temperature [K]', 'Stellar Radius [Solar Radius]',
#  'Stellar Mass [Solar mass]', 'Stellar Luminosity [log(Solar)]', 
#  'Stellar Surface Gravity [log10(cm/s**2)]', 'Stellar Age [Gyr]']
# ```
#
# and that `stars_rows` has **1508** rows of which the **first three** are:
#
# ```python
# [['11 Com', 'G8 III', '4742.00', '19.00', '2.70', '2.243', '2.31', ''],
#  ['11 UMi', 'K4 III', '4213.00', '29.79', '2.78', '2.430', '1.93', '1.560'],
#  ['14 And', 'K0 III', '4813.00', '11.00', '2.20', '1.763', '2.63', '4.500']]
# ```

# ### Function 1: `star_cell(row_idx, col_name, stars_rows, header=stars_header)`
#
# This function **must** read the **list** of **lists** `stars_rows`, and extract the value at **row** index `row_idx` and **column** name `col_name`. The function **must** typecast the value based on `col_name`. If the value in `stars_rows` is **missing** (i.e., it is `''`), then the value returned **must** be `None`.
#
# The **column** of `stars_rows` where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Column of `stars_rows`|Data Type|
# |------|---------|
# |Spectral Type|**string**|
# |Stellar Effective Temperature [K]|**float**|
# |Stellar Radius [Solar Radius]|**float**|
# |Stellar Mass [Solar mass]|**float**|
# |Stellar Luminosity [log(Solar)]|**float**|
# |Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |Stellar Age [Gyr]|**float**|

# copy/paste the 'star_cell' function from lab-p10 here
def star_cell(row_idx, col_name, stars_rows, header=stars_header):
    col_idx = header.index(col_name)
    val = stars_rows[row_idx][col_idx]
    if val =='':
        return None
    elif col_name =='Stellar Mass [Solar mass]':
        val = float(val)
    elif col_name == 'Stellar Effective Temperature [K]':
        val = float(val)
    elif col_name=='Stellar Radius [Solar Radius]':
        val = float(val)
    elif col_name == 'Stellar Luminosity [log(Solar)]':
        val = float(val)
    elif col_name == 'Stellar Surface Gravity [log10(cm/s**2)]':
        val = float(val)
    elif col_name == 'Stellar Age [Gyr]':
        val = float(val)
    return val


# **Question 5:** Create a `Star` object for the **third** star in `"stars_1.csv"`.
#
# You **must** access the values in `stars_1.csv` using the `star_cell` function. Note that the third star would be at **index** 2.
#
# The **attribute** of the `Star` namedtuple object, the corresponding **column** of the `stars_1.csv` file where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Attribute of `Star` object|Column of `stars_1.csv`|Data Type|
# |---------|------|---------|
# |`spectral_type`|Spectral Type|**string**|
# |`stellar_effective_temperature`|Stellar Effective Temperature [K]|**float**|
# |`stellar_radius`|Stellar Radius [Solar Radius]|**float**|
# |`stellar_mass`|Stellar Mass [Solar mass]|**float**|
# |`stellar_luminosity`|Stellar Luminosity [log(Solar)]|**float**|
# |`stellar_surface_gravity`|Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |`stellar_age`|Stellar Age [Gyr]|**float**|

# +
# compute and store the answer in the variable 'third_star', then display it
row_idx = 2 # the index of the star we want to convert into a Star object

spectral_type = stars_1_rows[row_idx][stars_header.index('Spectral Type')]
stellar_effective_temperature = float(stars_1_rows[row_idx][stars_header.index('Stellar Effective Temperature [K]')])
stellar_radius = float(stars_1_rows[row_idx][stars_header.index('Stellar Radius [Solar Radius]')])
stellar_mass = float(stars_1_rows[row_idx][stars_header.index('Stellar Mass [Solar mass]')])
stellar_luminosity = float(stars_1_rows[row_idx][stars_header.index('Stellar Luminosity [log(Solar)]')])
stellar_surface_gravity = float(stars_1_rows[row_idx][stars_header.index('Stellar Surface Gravity [log10(cm/s**2)]')])
stellar_age = float(stars_1_rows[row_idx][stars_header.index('Stellar Age [Gyr]')]) # extract the value in the column 'Stellar Age [Gyr]' and typecast

third_star = Star(spectral_type, stellar_effective_temperature, stellar_radius, \
                  stellar_mass, stellar_luminosity, \
                  stellar_surface_gravity, stellar_age)

third_star
# -

grader.check("q5")


# ### Function 2:  `get_stars(star_file)`
#
# This function **must** take in as its input, the **relative path** of a CSV file `star_file` which contains data on stars in the same format as `stars_1.csv`. It **must** return a **dictionary** mapping the `Name` of each star in `star_file` to a `Star` object containing all the other details of the star.
#
# You **must** access the values in `stars_1.csv` using the `star_cell` function.
#
# Once again, as a reminder, the attributes of the `Star` objects should be obtained from the **rows** of `star_file` and stored as follows:
#
# |Attribute of `Star` object|Column of `star_file`|Data Type|
# |---------|------|---------|
# |`spectral_type`|Spectral Type|**string**|
# |`stellar_effective_temperature`|Stellar Effective Temperature [K]|**float**|
# |`stellar_radius`|Stellar Radius [Solar Radius]|**float**|
# |`stellar_mass`|Stellar Mass [Solar mass]|**float**|
# |`stellar_luminosity`|Stellar Luminosity [log(Solar)]|**float**|
# |`stellar_surface_gravity`|Stellar Surface Gravity [log10(cm/s**2)]|**float**|
# |`stellar_age`|Stellar Age [Gyr]|**float**|
#
# In case any data in `star_file` is **missing**, the corresponding value should be `None`.
#
# For example, when this function is called with the file `stars_1.csv` as the input, the **dictionary** returned should look like:
#
# ```python
# {'11 Com': Star(spectral_type='G8 III', stellar_effective_temperature=4742.0, 
#                 stellar_radius=19.0, stellar_mass=2.7, stellar_luminosity=2.243, 
#                 stellar_surface_gravity=2.31, stellar_age=None),
#  '11 UMi': Star(spectral_type='K4 III', stellar_effective_temperature=4213.0, 
#                 stellar_radius=29.79, stellar_mass=2.78, stellar_luminosity=2.43, 
#                 stellar_surface_gravity=1.93, stellar_age=1.56),
#  '14 And': Star(spectral_type='K0 III', stellar_effective_temperature=4813.0, 
#                 stellar_radius=11.0, stellar_mass=2.2, stellar_luminosity=1.763, 
#                 stellar_surface_gravity=2.63, stellar_age=4.5),
#  ...
# }
# ```

# copy/paste the 'star_cell' function from lab-p10 here
def star_cell(row_idx, col_name, stars_rows, header=stars_header):
    col_idx = header.index(col_name)
    val = stars_rows[row_idx][col_idx]
    if val =='':
        return None
    elif col_name =='Stellar Mass [Solar mass]':
        val = float(val)
    elif col_name == 'Stellar Effective Temperature [K]':
        val = float(val)
    elif col_name=='Stellar Radius [Solar Radius]':
        val = float(val)
    elif col_name == 'Stellar Luminosity [log(Solar)]':
        val = float(val)
    elif col_name == 'Stellar Surface Gravity [log10(cm/s**2)]':
        val = float(val)
    elif col_name == 'Stellar Age [Gyr]':
        val = float(val)
    return val


# +
# replace the ... with your code

stars_1_csv = process_csv(os.path.join("data", "stars_1.csv")) # read the data in 'stars_1.csv'
stars_header = stars_1_csv[0]
stars_1_rows = stars_1_csv[1:]


# +
# define the function 'get_stars' here

def get_stars(star_file):
    # TODO: read star_file to a list of lists
    # TODO: loop through each row in star_file
    stars_csv = process_csv(star_file)
    stars_header = stars_csv[0]
    stars_rows = stars_csv[1:]
    
    
    empty_dict = {}
    for row_idx in range(len(stars_rows)):
        star_name = star_cell(row_idx, 'Name', stars_rows)      
        star = Star(star_cell(row_idx, 'Spectral Type', stars_rows), star_cell(row_idx, 'Stellar Effective Temperature [K]', stars_rows), \
        star_cell(row_idx, 'Stellar Radius [Solar Radius]', stars_rows), star_cell(row_idx, 'Stellar Mass [Solar mass]', stars_rows), \
        star_cell(row_idx, 'Stellar Luminosity [log(Solar)]', stars_rows), star_cell(row_idx, 'Stellar Surface Gravity [log10(cm/s**2)]', stars_rows),\
        star_cell(row_idx, 'Stellar Age [Gyr]', stars_rows))
        empty_dict[star_name] = star
    return empty_dict


    # TODO: add each Star objet to a dictionary
    # TODO: return the dictionary at the end of the loop
# replace with your code
# -

# you can now use 'get_stars' to read the data in 'stars_1.csv' but DO NOT display
stars_1_dict = get_stars(os.path.join("data", "stars_1.csv"))

# **Question 6:** What is the `Star` object of the star (in `stars_1.csv`) named *DP Leo*?
#
# You **must** access the `Star` object in `stars_1_dict` **dictionary** defined above to answer this question.

# compute and store the answer in the variable 'dp_leo', then display it
dp_leo = stars_1_dict["DP Leo"]
dp_leo
grader.check("q6")

# **Question 7:** What's the **average** `stellar_luminosity` of **all** the stars in the `star_1.csv` file?
#
# You **must** use the `stars_1_dict` **dictionary** defined above to answer this question.
#
# To find the average, you **must** first **add** up the `stellar_luminosity` value of all the stars and **divide** by the total **number** of stars. You **must skip** stars which don't have the `stellar_luminosity` data. Such stars should not contribute to either the sum of `stellar_luminosity` or to the number of stars.

# +
# compute and store the answer in the variable 'avg_lum_stars_1', then display it
avg_lum_stars_1 = 0
none_counter = 0
for luminosity in stars_1_dict:
    if stars_1_dict[luminosity].stellar_luminosity == None:
        continue
    else:
        avg_lum_stars_1 += stars_1_dict[luminosity].stellar_luminosity
        none_counter += 1

avg_lum_stars_1 = avg_lum_stars_1 / none_counter
    
avg_lum_stars_1
# -
grader.check("q7")

# **Question 8:** What is the **average** `stellar_age` of **all** the stars in the `stars_2.csv` file?
#
# You **must** use the function `get_stars(csv_file)` to read the data in `stars_2.csv`. Your output **must** be a **float** representing the `stellar_age` in units of *gigayears*. You **must** skip stars which have missing `stellar_age` data.

# +
# compute and store the answer in the variable 'avg_age_stars_2', then display it
stars_2_dict = get_stars(os.path.join("data", "stars_2.csv"))

avg_age_stars_2 = 0
none_counter = 0
for ages in stars_2_dict:
    if stars_2_dict[ages].stellar_age == None:
        continue
    else:
        avg_age_stars_2 += stars_2_dict[ages].stellar_age
        none_counter += 1
    
avg_age_stars_2 = avg_age_stars_2 / none_counter

avg_age_stars_2
avg_age_stars_2
# -
grader.check("q8")

# ### Data Structure 2: `stars_dict`
#
# You are now ready to read all the data about the stars stored in the `data` directory. You **must** now create a **dictionary** mapping the `Name` of each star in the `data` directory (inside the files `stars_1.csv`, ..., `stars_5.csv`) to the `Star` object containing all the other details about the star.
#
# You **must not** hardcode the files/paths of the files `stars_1.csv`, ..., `stars_5.csv` to answer this question. Instead, you **must** use the `os` module to find all the files in the `data` directory that begin with `'stars'`, and use the `get_stars` function on each of those files to create `stars_dict`.
#
# **Hints:** You may use the `stars_paths` variable defined earlier in q4 to get the list of paths needed for this question. You can use the `update` dictionary **method** to combine two **dictionaries**.

# define the variable 'stars_dict' here,
# but do NOT display the variable at the end
stars_dict = {}
for idx in stars_paths:
    value = get_stars(idx)
    stars_dict.update(value)

# If you wish to **verify** that you have read the files and defined `stars_dict` correctly, you can check that `stars_dict` has **3879** key/value pairs in it.

len(stars_dict)

# **Question 9:** What is the `stellar_effective_temperature` of the star *Kepler-220*?
#
# You **must** access the correct `Star` object in the `stars_dict` **dictionary** defined above to answer this question.

# compute and store the answer in the variable 'kepler_220_temp', then display it
kepler_220_temp = stars_dict["Kepler-220"].stellar_effective_temperature
kepler_220_temp
grader.check("q9")

# **Question 10:** Find the **name** of the **largest** star (in terms of `stellar_radius`) in the `stars_dict` **dictionary**.
#
# Your output **must** be a **string**. You do **not** need to worry about any ties. You **must** skip any stars with **missing** `stellar_radius` data.

# +
# compute and store the answer in the variable 'biggest_star', then display it
test = []
for radius in stars_dict:
#     print(radius)
    rad = stars_dict[radius].stellar_radius
    if rad == None:
        continue
    if rad > 100:
        test.append(radius)

#from geeks for geeks
def listToString(s):
    str1 = " "
    return (str1.join(s))
biggest_star = test
biggest_star = listToString(biggest_star)
biggest_star


    
# -

grader.check("q10")

# **Question 11:** What is the **average** `stellar_age` (in *gigayears*) of **all** the stars in the `stars_dict` **dictionary** whose names **start with** `"Kepler"`?
#
# Your output **must** be a **float**. You **must** skip all stars with **missing** `stellar_age` data.

value = 'Kepler-1000'
value[:6]

# compute and store the answer in the variable 'avg_age_kepler', then display it
avg_age_kepler = []
for age in stars_dict:
    ages = stars_dict[age].stellar_age
    if ages == None:
        continue
    if age.startswith('Kepler'):
        avg_age_kepler.append(ages)
avg_age_kepler = sum(avg_age_kepler) / len(avg_age_kepler)
avg_age_kepler

grader.check("q11")

# ### Data Structure 3: namedtuple `Planet`
#
# Just as you did with the stars, you will be using namedtuples to store the data about the planets in the `planets_1.csv`, ..., `planets_5.csv` files. Before you start reading these files however, you **must** create a new `Planet` type (using namedtuple). It **must** have the following attributes:
#
# * `planet_name`
# * `host_name`
# * `discovery_method`
# * `discovery_year`
# * `controversial_flag`
# * `orbital_period`
# * `planet_radius`
# * `planet_mass`
# * `semi_major_radius`
# * `eccentricity`
# * `equilibrium_temperature`
# * `insolation_flux`

# +
# define the namedtuple 'Planet' here
planet_attributes = ['planet_name',
                    'host_name',
                    'discovery_method',
                    'discovery_year',
                    'controversial_flag',
                    'orbital_period',
                    'planet_radius',
                    'planet_mass',
                    'semi_major_radius',
                    'eccentricity',
                    'equilibrium_temperature',
                    'insolation_flux']

Planet = namedtuple("Planet",planet_attributes)
# +
# run this following cell to initialize and test an example Planet object
# if this cell fails to execute, you have likely not defined the namedtuple 'Star' correctly
jupiter = Planet('Jupiter', 'Sun', 'Imaging', 1610, False, 4333.0, 11.209, 317.828, 5.2038, 0.0489, 110, 0.0345)

jupiter
# -

grader.check("planet_object")

# ### Creating `Planet` objects
#
# We are now ready to read the files in the `data` directory and create `Planet` objects. Creating `Planet` objects however, is going to be more difficult than creating `Star` objects, because the data required to create a single `Planet` object is split up into different files.
#
# The `planets_1.csv`, ..., `planets_5.csv` files contain all the data required to create `Planet` objects **except** for the `host_name`. The `host_name` for each planet is to be found in the `mapping_1.json`, ..., `mapping_5.json` files.

# First, let us read the data in `planets_1.csv`. Since this is a CSV file, you can use the `process_csv` function from above to read this file. In the cell below, you **must** read the data in `planets_1.csv` and extract the **header** and the non-header **rows** of the file.

youngest_star_planets = [Planet(planet_name='Kepler-1663 b', host_name='Kepler-1663', discovery_method='Transit', discovery_year=2020, controversial_flag=False, orbital_period=17.6046, planet_radius=3.304, planet_mass=10.9, semi_major_radius=0.1072, eccentricity=0.0, equilibrium_temperature=362.0, insolation_flux=4.07)]

# +
# replace the ... with your code

planets_1_csv = process_csv(os.path.join("data", 'planets_1.csv')) # read the data in 'planets_1.csv'
planets_header = planets_1_csv[0]
planets_rows = planets_1_csv[1:]


# -

# If you wish to **verify** that you have read the file and defined the variables correctly, you can check that `planets_header` has the value:
#
# ```python
# ['Planet Name', 'Discovery Method', 'Discovery Year', 'Controversial Flag', 'Orbital Period [days]',
#  'Planet Radius [Earth Radius]', 'Planet Mass [Earth Mass]', 'Orbit Semi-Major Axis [au]',
#  'Eccentricity', 'Equilibrium Temperature [K]', 'Insolation Flux [Earth Flux]']
# ```
#
# and that `planets_rows` has **1508** rows of which the **first three** are:
#
# ```python
# [['11 Com b', 'Radial Velocity', '2007', '0', '326.03', '12.1', '6165.6', '1.29', '0.231', '', ''],
#  ['11 UMi b', 'Radial Velocity', '2009', '0', '516.21997', '12.3', '4684.8142', '1.53', '0.08', '', ''],
#  ['14 And b', 'Radial Velocity', '2008', '0', '185.84', '12.9', '1525.5', '0.83', '0', '', '']]
# ```

# Now, you are ready to read the data in `mapping_1.json`. Since this is a JSON file, you will need to copy/paste the `read_json` function lab-p10, and use it to read the file.

# # copy & paste the read_json file from lab-p10
def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# now use the read_json function to read 'mapping_1.json'
mapping_1_json = read_json(os.path.join("data", "mapping_1.json"))


# If you wish to **verify** that you have read the file correctly, you can check that `mapping_1_json` has the value:
#
# ```python
# {'11 Com b': '11 Com',
#  '11 UMi b': '11 UMi',
#  '14 And b': '14 And',
#  ...
#  }
# ```
#
# Now that we have read `planets_1.csv` and `mapping_1.json`, we are now ready to combine these two files to create `Planet` objects.

# ### Function 3: `planet_cell(row_idx, col_name, planets_rows, header=planets_header)`
#
# This function **must** read the **list** of **lists** `planets_rows`, and extract the value at **row** index `row_idx` and **column** index `col_idx`. The function **must** typecast the value based on `col_name`. If the value in `stars_rows` is **missing** (i.e., it is `''`), then the value returned **must** be `None`.
#
# The **column** of `planets_rows` where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Column of `planets_rows`|Data Type|
# |------|---------|
# |Planet Name|**string**|
# |Discovery Year|**int**|
# |Discovery Method|**string**|
# |Controversial Flag|**bool**|
# |Orbital Period [days]|**float**|
# |Planet Radius [Earth Radius]|**float**|
# |Planet Mass [Earth Mass]|**float**|
# |Orbit Semi-Major Axis [au]|**float**|
# |Eccentricity|**float**|
# |Equilibrium Temperature [K]|**float**|
# |Insolation Flux [Earth Flux]|**float**|
#
# **Important Hint:** While computing the value of the attribute `controversial_flag`, note that the `Controversial Flag` column of `planets_1.csv` represents `True` with `'1'` and `False` with `'0'`. You **must** be careful with typecasting **strings** to **booleans**.

# +
# copy/paste the function 'planet_cell' from lab-p10 here
# replace the ... with your code

def planet_cell(row_idx, col_name, planets_rows, header=planets_header):
    col_idx = header.index(col_name) # extract col_idx from col_name and header
    val = planets_rows[row_idx][col_idx]  # extract the value at row_idx and col_idx
    if val == '':
        return None
    if col_name in ["Controversial Flag"]:
        if val == "1":
            return True
        else:
            return False
    if col_name in ['Discovery Year']:
        return int(val)
    if col_name in ["Orbital Period [days]", 'Planet Radius [Earth Radius]', 
                    'Planet Mass [Earth Mass]','Orbit Semi-Major Axis [au]',
                    'Eccentricity', 'Equilibrium Temperature [K]', 'Insolation Flux [Earth Flux]' ]:
        return float(val)
    return val
    # for all other columns typecast 'val' depending on col_name and return it


# -

# **Question 12:** Create a `Planet` object for the **fifth** planet in the `planets_1.csv` file.
#
# You **must** access the values in `planets_1.csv` using the `planet_cell` function. Note that the ninth star would be at **index** 4.
#
# The **attribute** of the `Planet` namedtuple object, the corresponding **column** of the `planets_1.csv` file where the value should be obtained from, and the correct **data type** for the value are listed in the table below:
#
# |Attribute of `Planet` object|Column of `planets_1.csv`|Data Type|
# |---------|------|---------|
# |`planet_name`|Planet Name|**string**|
# |`host_name`| - |**string**|
# |`discovery_method`|Discovery Method|**string**|
# |`discovery_year`|Discovery Year|**int**|
# |`controversial_flag`|Controversial Flag|**bool**|
# |`orbital_period`|Orbital Period [days]|**float**|
# |`planet_radius`|Planet Radius [Earth Radius]|**float**|
# |`planet_mass`|Planet Mass [Earth Mass]|**float**|
# |`semi_major_radius`|Orbit Semi-Major Axis [au]|**float**|
# |`eccentricity`|Eccentricity|**float**|
# |`equilibrium_temperature`|Equilibrium Temperature [K]|**float**|
# |`insolation_flux`|Insolation Flux [Earth Flux]|**float**|
#
#
# The value of the `host_name` attribute is found in `mapping_1.json`.

# +
row_idx = 4
planet_name = planet_cell(row_idx,'Planet Name', planets_rows)
host_name = mapping_1_json[planet_name]
discovery_method = planet_cell(row_idx, 'Discovery Method',planets_rows)
discovery_year = planet_cell(row_idx, 'Discovery Year',planets_rows)
controversial_flag = planet_cell(row_idx, 'Controversial Flag',planets_rows)
orbital_period = planet_cell(row_idx, 'Orbital Period [days]',planets_rows)
planet_radius = planet_cell(row_idx, 'Planet Radius [Earth Radius]',planets_rows)
planet_mass = planet_cell(row_idx, 'Planet Mass [Earth Mass]',planets_rows)
semi_major_radius = planet_cell(row_idx, 'Orbit Semi-Major Axis [au]',planets_rows)
eccentricity = planet_cell(row_idx, 'Eccentricity',planets_rows)
equilibrium_temperature = planet_cell(row_idx, 'Equilibrium Temperature [K]',planets_rows)
insolation_flux = planet_cell(row_idx, 'Insolation Flux [Earth Flux]',planets_rows)

fifth_planet = Planet(planet_name, host_name, discovery_method, discovery_year, controversial_flag, orbital_period,
                     planet_radius, planet_mass, semi_major_radius, eccentricity, equilibrium_temperature, insolation_flux)
fifth_planet
# -

grader.check("q12")


# ### Function 4: `get_planets(planet_file, mapping_file)`: 
#
# This function **must** take in as its input, a CSV file `planet_file` which contains data on planets in the same format as `planets_1.csv`, as well as a JSON file `mapping_file` which maps planets in `planet_file` to their host star in the same format as `mapping_1.json`. This function **must** return a **list** of `Planet` objects by combining the data in these two files. The `Planet` objects **must** appear in the same order as they do in `planet_file`.
#
# You **must** access the values in `planets_1.csv` using the `planet_cell` function.
#
# Once again, as a reminder, the attributes of the `Planet` objects should be obtained from the **rows** of `planet_file` and from `mapping_file` and stored as follows:
#
# |Attribute of `Planet` object|Column of `planets_1.csv`|Data Type|
# |---------|------|---------|
# |`planet_name`|Planet Name|**string**|
# |`host_name`| - |**string**|
# |`discovery_method`|Discovery Method|**string**|
# |`discovery_year`|Discovery Year|**int**|
# |`controversial_flag`|Controversial Flag|**bool**|
# |`orbital_period`|Orbital Period [days]|**float**|
# |`planet_radius`|Planet Radius [Earth Radius]|**float**|
# |`planet_mass`|Planet Mass [Earth Mass]|**float**|
# |`semi_major_radius`|Orbit Semi-Major Axis [au]|**float**|
# |`eccentricity`|Eccentricity|**float**|
# |`equilibrium_temperature`|Equilibrium Temperature [K]|**float**|
# |`insolation_flux`|Insolation Flux [Earth Flux]|**float**|
#
# The value of the `host_name` attribute is found in `mapping_file`.
#
# In case any data in `planet_file` is **missing**, the corresponding value should be `None`.
#
# For example, when this function is called with the file `planets_1.csv` and `mapping_1.json` as the input, the **list** returned should look like:
#
# ```python
# [
#     Planet(planet_name='11 Com b', host_name='11 Com', discovery_method='Radial Velocity', 
#            discovery_year=2007, controversial_flag=False, orbital_period=326.03, 
#            planet_radius=12.1, planet_mass=6165.6, semi_major_radius=1.29, 
#            eccentricity=0.231, equilibrium_temperature=None, insolation_flux=None),
#     Planet(planet_name='11 UMi b', host_name='11 UMi', discovery_method='Radial Velocity', 
#            discovery_year=2009, controversial_flag=False, orbital_period=516.21997, 
#            planet_radius=12.3, planet_mass=4684.8142, semi_major_radius=1.53, 
#            eccentricity=0.08, equilibrium_temperature=None, insolation_flux=None),
#     Planet(planet_name='14 And b', host_name='14 And', discovery_method='Radial Velocity', 
#            discovery_year=2008, controversial_flag=False, orbital_period=185.84, 
#            planet_radius=12.9, planet_mass=1525.5, semi_major_radius=0.83, 
#            eccentricity=0.0, equilibrium_temperature=None, insolation_flux=None),
#     ...
# ]
# ```

def get_planets(planet_file, mapping_file):
    # TODO: read planet_file to a list of lists
    # TODO: extract the header and rows from planet_file
    # TODO: read mapping_file to a dictionary
    # TODO: loop through each row in planet_file
    # TODO: create a Planet object (namedTuple) for each row
    # TODO: add each Planet objet to a list
    # TODO: return the list at the end of the loop
    planets_csv = process_csv(planet_file)
    planets_header = planets_csv[0]
    planets_rows = planets_csv[1:]
    try:
        mapping_files = read_json(mapping_file)
    except json.decoder.JSONDecodeError:
        mapping_files = []
   
    blank_list = []
    for row_idx in range(len(planets_rows)):
        try:
            planet_name = planet_cell(row_idx,'Planet Name', planets_rows)
            host_name = mapping_files[planet_name]
            discovery_method = planet_cell(row_idx, 'Discovery Method', planets_rows)
            discovery_year = planet_cell(row_idx, 'Discovery Year', planets_rows)
            controversial_flag = planet_cell(row_idx, 'Controversial Flag', planets_rows)
            orbital_period = planet_cell(row_idx, 'Orbital Period [days]', planets_rows)
            planet_radius = planet_cell(row_idx, 'Planet Radius [Earth Radius]', planets_rows)
            planet_mass = planet_cell(row_idx, 'Planet Mass [Earth Mass]', planets_rows)
            semi_major_radius = planet_cell(row_idx, 'Orbit Semi-Major Axis [au]', planets_rows)
            eccentricity = planet_cell(row_idx, 'Eccentricity', planets_rows)
            equilibrium_temperature = planet_cell(row_idx, 'Equilibrium Temperature [K]', planets_rows)
            insolation_flux = planet_cell(row_idx, 'Insolation Flux [Earth Flux]', planets_rows)

            planet = Planet(planet_name, host_name, discovery_method, discovery_year,\
                    controversial_flag, orbital_period, planet_radius, planet_mass,\
                    semi_major_radius, eccentricity, equilibrium_temperature, insolation_flux)


            blank_list.append(planet)
        except (RuntimeError, KeyError, ValueError, TypeError, IndexError):
            continue
   
    return blank_list
planets_1_dict = get_planets(os.path.join('data', "planets_1.csv"), os.path.join('data', 'mapping_1.json'))

# **Question 13:** What are the **last five** `Planet` objects in the **list** returned by `get_planets` when `planet_file` is `planets_1.csv` and `mapping_file` is `mapping_1.json`?
#
# Your output **must** be a **list** of `Planet` objects.
#
# **Hint:** First, you **must** use the `get_planets` function to parse the data in `planets_1.csv` and `mapping_1.json` and create a **list** of `Planet` objects. Then, you may slice this **list** to get the last five `Planet` objects.

ex_list = [1,2,3,4,5,6,7,8,9,10]
ex_list[-5:]

# compute and store the answer in the variable 'last_five_planets_1', then display it
last_five_planets_1 = planets_1_dict[-5:]
last_five_planets_1

grader.check("q13")

# **Question 14:** What are the `Planet` objects whose `controversial_flag` attribute is `True` in the **list** returned by `get_planets` when `planet_file` is `planets_2.csv` and `mapping_file` is `mapping_2.json`?
#
# Your output **must** be a **list** of `Planet` objects.

# +
# compute and store the answer in the variable 'controversial_planets', then display it
planets_2_dict = get_planets(os.path.join('data', "planets_2.csv"), os.path.join('data', 'mapping_2.json'))

controversial_planets = []
for trues in planets_2_dict:
    flag = trues.controversial_flag
    if flag == True:
        controversial_planets.append(trues)
        
controversial_planets
        
# -
grader.check("q14")

# ### Data Cleaning 1: broken CSV rows
#
# Our function `get_planets` works very well so far. However, it is likely that it will not work on all the files in the `data` directory. For example, if you use the function `get_planets` to read the data in `planets_4.csv` and `mapping_4.json`, you will most likely run into an error. **Try it yourself to verify!**
#
# The reason your code likely crashed is because there the file `planets_4.csv` is **broken**. For some reason, several rows in `planets_4.csv` have their data jumbled up. For example, in the **566**th row of `planets_4.csv`, we come across this row:
#
# |Planet Name|Discovery Method|Discovery Year|Controversial Flag|Orbital Period [days]|Planet Radius [Earth Radius]|Planet Mass [Earth Mass]|Orbit Semi-Major Axis [au]|Eccentricity|Equilibrium Temperature [K]|Insolation Flux [Earth Flux]|
# |-----------|----------------|--------------|------------------|---------------------|----------------------------|------------------------|---------------------------|------------|---------------------------|----------------------------|
# |pi Men c|pi Men|Transit|2018|0|6.26790772|2.060|3.63000|0.068647|0.076939|1170|
#
# We can see that for some reason, the value under the column `Discovery Method` is the name of the planet's host star. This causes the value under the column `Discovery Year` to be a **string** instead of a number.
#
# We will call such a **row** in a CSV file where the values under a column do not match the expected format to be a **broken row**. While it is possible to sometimes extract useful data from broken rows, in this project, we will simply **skip** broken rows.
#
# You **must** now go back to your definition of `get_planets` and edit it, so that any **broken rows get skipped**.
#
# **Hints:**
#
# 1. The simplest way to recognize if a row is broken is if you run into any **RunTime Errors** when you call the `get_planets` function. So, one simple way to skip bad rows would be to use `try/except` blocks to avoid processing any rows that cause the code to crash; remember **not** to use *bare* `try/except` blocks.
# 2. There are **several different kinds** of errors that you can expect to find when you try to parse `planets_4.csv`. You should **explicitly** handle each of these errors using `try/except` blocks.
# 3. There are only **5** broken rows in `planets_4.csv`, and they are all bunched up at the very end. You can manually **inspect** these rows, and figure out why these rows are broken.
#
# **Important Warning:** You are **not** allowed to **hardcode** the indices of the broken rows. You may inspect `planets_4.csv` to identify how to tell a **broken row** apart. Therefore, to use the example of the **broken row** above, you **may not** hardcode to skip the **566**th row of `planets_4.csv`. However, it is **acceptable** to make your function **skip** any row for which the value under the `Discovery Year` is not numeric, by observing that this is the reason why the row is broken.

# **Question 15:** What are the **last five** `Planet` objects produced by `get_planets` when `planet_file` is `planets_4.csv` and `mapping_file` is `mapping_4.json`?
#
# Your output **must** be a **list** of `Planet` objects.

# compute and store the answer in the variable 'last_five_planets_4', then display it
last_five_planets_4 =  get_planets(os.path.join('data', "planets_4.csv"), os.path.join('data', 'mapping_4.json'))[-5:]
last_five_planets_4
grader.check("q15")

# ### Data Cleaning 2: broken JSON files
#
# We are now ready to read **all** the files in the `data` directory and create a **list** of `Planet` objects for all the planets in the directory. However, if you try to use `get_planets` on all the planet CSV files and mapping JSON files, you will likely run into another error. **Try it for yourself by calling `get_planets` on all the files in `data`!**
#
# It is likely that your code crashed when you tried to read the data in `planets_5.csv` and `mapping_5.json`. This is because the file `mapping_5.json` is **broken**. Unlike **broken** CSV files, where we only had to skip the **broken rows**, it is much harder to parse **broken JSON files**. When a JSON file is **broken**, we often have no choice but to **skip the file entirely**.
#
# You **must** now go back to your definition of `get_planets` and edit it, so that if the JSON file is **broken**, then the file is completely skipped, and only an **empty list** is returned.
#
# **Important Warning:** You are **not** allowed to **hardcode** the name of the files to be skipped. You **must** use `try/except` blocks to determine whether the JSON file is **broken** and skip the file if it is. Remmeber **not** to use *bare* `try/except` blocks.
#
# **Hint:** Your resulting function will need to have **two** separate `try/except blocks` - one for handling broken CSV rows and one for handling the broken JSON files.

# ### Data Structure 4: `planets_list`
#
# You are now ready to read all the data about the planets stored in the `data` directory. You **must** now create a **list** containing `Planet` objects by parsing the data inside the files `planets_1.csv`, ..., `planets_5.csv` and `mapping_1.json`, ..., `mapping_5.json`.
#
# You **must** skip any **broken rows** in the CSV file, and also completely skip any **broken JSON files**. However, you are **not** allowed to **hardcode** the file you need to skip. You **must** call `get_planets` on **all** 5 pairs of files to answer this question.
#
# You **must** use the `get_planets` function on each of the five pairs of files in the `data` directory to create `planets_list`.
#
# **Hint:** Recall that you have already created the variable `json_file_paths` in q3. You can similarly create a list of paths of the files that start with `"planets"` (see q4 for a similar question). After sorting the paths in these **lists**,  you just need to loop through the indices of these two lists, and use that to extract the pairs of paths from these two lists.

planets_paths = []
for idx in data:
    if idx.startswith('planets'):
        planets_paths.append(os.path.join('data', idx))
planets_paths

json_file_paths = []
for idx in file_paths:
    if idx.endswith('json'):
        json_file_paths.append(idx)
json_file_paths

# +
# define the variable 'planets_list' here,
# but do NOT display the variable at the end
# TODO: create empty list planets_list
planets_list = []
# TODO: get an alphabetical list of planet files and mapping files
for idx in range(len(planets_paths)):
    #print(idx)
    test = get_planets(planets_paths[idx], json_file_paths[idx])
    planets_list.extend(test)
#     read = get_planets(planet_file, mapping_file)
#     planets_list.extend(read)
    
# TODO: iterate through the indices of one of the lists
# TODO: call 'get_planets' and extend to 'planets_list'

# -

len(planets_list)

# If you wish to **verify** that you have read the files and defined `planets_list` correctly, you can check that `planets_list` has **4724** `Planet` objects in it.

# **Question 16:** What is the output of `planets_list[4520:4525]`?
#
# Your output **must** be a **list** of `Planet` objects.

# compute and store the answer in the variable 'planets_4520_4525', then display it
planets_4520_4525 = planets_list[4520:4525]
planets_4520_4525
grader.check("q16")

# **Question 17:** How many planets in `planets_list` were discovered in the year *2022*?
#
# Your output **must** be an **integer**.

# compute and store the answer in the variable 'planets_disc_2022', then display it
planets_disc_2022 = 0
for idx in planets_list:
    year = idx.discovery_year
    if year == 2022:
        planets_disc_2022 += 1
planets_disc_2022
grader.check("q17")

# **Question 18**: Find the `Star` object around which the `Planet` named *TOI-2202 c* orbits.
#
# Your output **must** be a a `Star` object.
#
# **Hint:** You **must** first find the `Planet` object with the `planet_name` *TOI-2202 c* and then use the `host_name` attribute to identify the name of the star aroud which the planet orbits. Then, you can get the `Star` object using the `stars_dict` **dictionary** defined above.

# +
# compute and store the answer in the variable 'toi_2022_c_star', then display it
for idx in planets_list:
    name = idx.planet_name
    if name == "TOI-2202 c":
        dud = idx.host_name

toi_2022_c_star = stars_dict[dud]
toi_2022_c_star

    

# -
grader.check("q18")

# **Question 19:** Find the **average** `planet_radius` (in units of the radius of the Earth) of the planets that orbit stars with `stellar_radius` more than *10* (i.e. more than *10* times the radius of the Sun).
#
# Your output **must** be a **float**. You **must** skip any `Planet` objects with **missing** `planet_radius` data and any `Star` objects with **missing** `stellar_radius` data.

# +
# compute and store the answer in the variable 'avg_planet_radius_big_stars', then display it
planet_rad = 0
divider = 0
for planets in planets_list:
    radius = planets.planet_radius
    if radius == None:
        continue
    star_rad = stars_dict[planets.host_name].stellar_radius
    if star_rad == None:
        continue
    if star_rad > 10:
        planet_rad += radius
        divider += 1

avg_planet_radius_big_stars = planet_rad / divider
avg_planet_radius_big_stars
# -
grader.check("q19")

# **Question 20**: Find all the `Planet` objects that orbit the **youngest** `Star` object.
#
# Your output **must** be a **list** of `Planet` objects (even if there is **only one** `Planet` in the list). The age of a `Star` can be found from its `stellar_age` column. You **must** skip any stars with **missing** `stellar_age` data. You do **not** have to worry about any ties. There is a **unique** `Star` in the dataset which is the youngest star.

# +
min_star_age = None
youngest_star_planet = []
for stars in stars_dict:
    if stars_dict[stars].stellar_age != None:
        if min_star_age == None:
            min_star_age = stars
        elif stars_dict[min_star_age].stellar_age > stars_dict[stars].stellar_age:
            min_star_age = stars
for idx in range(len(planets_list)):
    if planets_list[idx].host_name == min_star_age:
        break

youngest_star_planets
# -

grader.check("q20")

# ## Submission
# Make sure you have run all cells in your notebook in order before running the following cells, so that all images/graphs appear in the output.
# It is recommended that at this stage, you Restart and Run all Cells in your notebook.
# That will automatically save your work and generate a zip file for you to submit.
#
# **SUBMISSION INSTRUCTIONS**:
# 1. **Upload** the zipfile to Gradescope.
# 2. Check **Gradescope otter** results as soon as the auto-grader execution gets completed. Don't worry about the score showing up as -/100.0. You only need to check that the test cases passed.

# running this cell will create a new save checkpoint for your notebook
from IPython.display import display, Javascript
display(Javascript('IPython.notebook.save_checkpoint();'))

# !jupytext --to py p10.ipynb

p10_test.check_file_size("p10.ipynb")
grader.export(pdf=False, run_tests=True, files=[py_filename])

#  
