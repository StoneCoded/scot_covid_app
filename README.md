# scot_covid_app (Scotland Covid Web App)

## Contents
1. Files and Implementation
2. Project Overview
3. Results and Observations
4. Licensing, Authors, and Acknowledgements

## 1. Files and Implementation

###Files

Anything that doesn't exist within the `wrangling_scripts` folder is to do with 
the web app deployment on Heroku.

`wrangling_scripts`:
  - `wrangle_data.py` - Contains all functions used in app.Gets data from government API, 
                        cleans if need and creates graphs using plotly.

Other than he standard Anaconda distribution of Python 3 you will also need:

- [Pandas](https://pandas.pydata.org/)
- [Plotly](https://plotly.com)
- [urllib3](https://pypi.org/project/urllib3/) - to handle  data retrieval
- [certifi](https://pypi.org/project/certifi/) - to handle certificate verification

For information on deployment to Heroku [click here](https://devcenter.heroku.com/categories/deployment)

##2. Project Overview

As of March 2020, Scotland entered into one of many National Lockdowns. It also
marked the beginning of my self propelled education in Python and Data Science.
As time wore on I wanted to build myself a tool to moniter the current situation 
without having to rely on news sites or social media posts.


## 3. Results and Observations

The fully opperation web app can be found [here](http://scotcovidapp.herokuapp.com)

## 5.Licensing, Authors, and Acknowledgements
All data is owned by the Scottish Government.

Scottish Government Data : [Link](https://statistics.gov.scot/home)


Copyright 2021 Ben Stone

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
