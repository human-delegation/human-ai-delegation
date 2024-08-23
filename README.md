# AI Delegation Project

The materials in this repository are a snapshot of the data and codes used in the research reported in the paper MISQ 2022-RN-18232. The repository contains THREE folders: **Raw Data**, **Data Processing**, and **Data Analysis**. The raw data in this public repository has the same format as the company's raw data. Due to the Non-Disclosure Agreement with the company that provided the dataset, the raw data is censored and transformed in this public repository. 

## Requirements

The data processing and experiments were performed using Python on a server with 2X 10-core Intel Xeon Gold 5215 Processor, 1 TB RAM. For this project, we use the following Python Packages:

1. [**os**](https://docs.python.org/3/library/os.html) provides a portable way of using operating system dependent functionality.
2. NumPy (v1.19.5) is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.
3. pandas (v1.3.5) is a software library written for the Python programming language for data manipulation and analysis. In particular, it offers data structures and operations for manipulating numerical tables and time series.
4. SciPy (v1.4.3) is a free and open-source Python library used for scientific computing and technical computing. 

## Raw Data folder
The **Raw Data** folder contains the log files of retail stores' daily operations. Specifically, each file is named by the store ID (censored) and includes the following spreadsheets.

**transaction\-inventory**. The ''transaction_inventory'' contains the daily sales, inventory, and stockout information. It has the following columns:


* ''product id'': the ID of this product.
* ''date'': ''day/month/year'' of this record.
* ''sale'': total number of products sold on this day. Note: this column was transformed by randomly generating a number between the minimum and maximum number of product sales of this store.
* "last selling time": the last time a product was sold on this day.
* "inventory end of day": number of products not sold by the end of this day.

**replenishment**. The "replenishment" sheet contains the daily replenishment operations made by human manager and AI. It has the following columns:

* "product id": the ID of this product.
* "product name": name of the product (replaced by the category of this product).
* "order date": date the replenishment order is made.
* "big class": the big category of this product.
* "sub class": the subcategory of this product.
* "optimal purchase bymodel": model's replenishment decision.
* "final purchase bymanager": the real number of replenishment products.
* "demand third day": AI's replenishment decision.

**modify\_delivery\_by\_manager**: this sheet contains the changes and detailed reasons for the tasks not delegated to AI. It has the following columns:

* "product id": the ID of this product.
* "order date": date the replenishment order is made.
* "expect by manager": manager's estimation on product sales.
* "forecast": decisions made by AI.
* "reason": manager's reason of not delegating this task to AI. 
	
## Data Processing folder
The **Data Processing** folder contains the calculation of KPIs for weekly performance evaluation. This folder has five subfolders, including three output folders (**0-Logsummary**, **1-KPIsummary**, and **2-KPI-summary-with-weather**), one folder for codes (**CodeProcessing**), and one folder for other input data (**OtherInputs). Specifically, the data processing has the following three steps: 

1. summarize log file (**Step1-logfile-processing.py**): in this step, we process the raw log file to calculate daily sales performance, demand loss, and product waste.
2. calculate KPI (**Step2-KPICalculate.py**): in this step, we calculate the overall store-level KPIs that were presented to the store managers, and the KPIs for some sub-categories of products for robustness tests.
3. merge weather and holiday information (**Step3-MergeWeatherHoliday.py**). We combine the weekly KPIs, the weather and holiday information for that week.

###*Output Folder*
The folder **2-KPI-summary-with-weather** is the output of data processing, which contains the research data for data analysis. Specifically, each file in this folder represents a sequence of delegation decisions, KPIs, and weather and holiday conditions for a single retail store (the censored name of this file). It contains the following columns:

* date: index of period after AI deployment.
* DelegationDecision: percentage of tasks delegated to AI.
* sale_improvement: Team vs. Human, the manager's sales improvement in period t after AI implementation.
* Manager_outperform: Team vs. AI, sales performance comparison between order by pure system and order after the manager's modification in period t.
*  outperform_area: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t
* BadWeather: Number of days with bad weather (rainy, snowy, etc.) in period t.
* Holiday: Number of holidays in period t.

The rest columns are calculated for alternative measurements of DV and for different categories of items.

* DelegationDecision\_demand: percentage of tasks delegated to AI at the product-quantity level.
* DelegationDecision\_bakery: percentage of tasks for bakery products delegated to AI.
* DelegationDecision\_dairy: percentage of tasks for dairy products delegated to AI.
* sale_bakery\_improvement: Team vs. Human, the manager's sales improvement in period t after AI implementation for bakery products.
* sale\_dairy\_improvement: Team vs. Human, the manager's sales improvement in period t after AI implementation for dairy products.
* Manager\_outperform\_bakery: Team vs. AI, sales performance comparison between order by pure system and order after the manager's modification'' in period t for bakery products.
* Manager\_outperform\_dairy: eam vs. AI, sales performance comparison between order by pure system' and order after the manager's modification in period t for dairy products.
* outperform\_area\_bakery: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t for bakery products.
* outperform\_area\_dairy: Team vs. Team, difference of sales improvement between the retail store and the regional average after AI implementation in period t for dairy products.


## Data Analysis folder

The **Data Analysis** foler contains the core scripts used for the Hidden Markov Model (HMM). Specifically, it contains: 

1. The Hidden Markov Model: (**Hidden Markov Model.py**). This is the main model for data analysis, which use the files in the data processing output folder **2-KPI-summary-with-weather**.
2. Initialization of parameters: Initial_parameters.csv. This file contains the initial papameters for HMM optimization. 
3. Model outputs: coefficient_estimations.csv. This is the file contains the estimation results for all retail stores in the Raw Data folder.





