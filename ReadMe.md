# Programming2 Assignments

## Program application
This repository contains the programming2 assignment, and it is established for educational purposes. 
 
## Repository parts
This repository serves as the primary submission for Programming 2. It consists of eleven distinct folders, with each one corresponding to a weekly assignment. Within each folder, you'll find all the necessary materials to address the questions presented in that particular assignment. The initial four weeks focus on explaining the principles of object-oriented programming. Meanwhile, the subsequent section of the course is devoted to illustrating effective strategies for handling large datasets and collaborating as an efficient team member.

### Week_1_1
Within this directory, you'll find two files. 'notebook_week1.ipynb' delves into the foundational SOLID principles of object-oriented programming, accompanied by other pertinent concepts. Additionally, you'll encounter an in-depth analysis of the code thoughtfully provided by our instructor. 'UML class.pdf' contains a comprehensive UML diagram depicting the structure of the aforementioned program.

### Week_1_2
This folder contains four 'py' and one 'ipynb' files. It contains three main classes: Atom Class constructs atom objects with attributes like atomic symbol, atomic number, and neutron number, featuring rich comparison methods and instance methods for retrieving proton and mass numbers. Chloroplast Class simulates photosynthesis by maintaining molecule counts, triggering the process upon reaching thresholds, and generating product molecules. Molecule Class represents molecules as tuples of Atom objects and counts, enabling molecule addition and chemical formula generation. The code includes custom exceptions for non-isotope atom pairs and non-Atom objects. Moreover, a notebook file is provided that contains study material of this topic.

### Week_1_3
This folder contains two nearly identical programs, with one of them utilizing the observer pattern while the other does not.

#### With Observer Pattern:
The main structure involves multiple classes interconnected through observer relationships. The Reader class reads CSV data in chunks and notifies first-layer observer classes, AverageYear and AverageMonth, which are responsible for calculating average values for years and months, respectively. These first-layer observers in turn notify second-layer observer classes, Animation, which creates animated plots based on the processed data. The CsvConverter class aids in converting CSV lines to JSON format, while the exception LenghtDiscripancy handles cases where the number of keys and values do not match during the conversion.

#### Without Observer Pattern:
The main classes include Animation, which creates animated plots using the provided data, CsvConverter, which converts CSV lines to JSON format, and Reader, responsible for reading and processing data from a file. The Animation class creates a series of animated plots with adjustable pause and resume functionality. The CsvConverter class handles the conversion of CSV lines to JSON format with error handling for discrepancies between the number of keys and values. this implementation is not based on Observer pattern.

### Week_1_4
Inside this folder, you'll find various files and a sub-folder named "Refactored Code." Within this subdirectory, you'll discover the observer code from week_1_3, but in a revised and refactored form. The primary directory itself contains several files. Specifically, 'crawler,' 'main,' and 'webcrawler' have all been refactored where appropriate. Moreover, I have examined their alignment with SOLID principles in the 'solid_evaluation' file. For educational resources related to week 4, you can explore the 'notebook_week4' file.

### Week_2_1
It constitutes a comprehensive weather data management system, encompassing data extraction, processing, and serving from a CSV file. Comprising three main components, the DataProvider class extracts weather data based on query parameters, converting it to JSON format for retrieval using criteria like specific years or ranges. The NetworkClient class focuses on asynchronous network requests, utilizing asyncio and the requests library for efficient URL-based data retrieval. The ServerHandler class, inheriting from SimpleHTTPRequestHandler, manages HTTP requests by collaborating with DataProvider for customized data retrieval based on user-defined criteria. The code also features an exception class, LenghtDiscripancy, which raises an error when key-value mismatch occurs in the CSV file.

### Week_2_2
It employs multiprocessing to fetch and process scientific literature data using the Entrez module from the BioPython library. It interacts with PubMed and PubMed Central (PMC) databases, extracting and downloading information. After setting up an email and API key, the script retrieves references and metadata using a PubMed identifier (PMID). Through multiprocessing, it efficiently downloads XML data for multiple references simultaneously, enhancing performance by parallelizing the process. The script's modular design allows easy adjustment of the number of references to download, making it a valuable tool for researchers and data enthusiasts who aim to streamline data acquisition and analysis from scientific literature.

### Week_2_3
this folder contains two files. 'prep' facilitates data preparation for the Dask tutorial by enabling the download, generation, and organization of various datasets, such as "random" and "flights." It offers size options and leverages command-line arguments for easy customization. The "flights" function manages NYC Flights dataset tasks, while the "random_array" function creates random array data with chunking options. This script enhances the Dask learning experience by simplifying dataset acquisition and amplifying user capabilities. Week_2_3employs Dask and scikit-learn libraries to preprocess data, train machine learning models, and visualize results. It reads configuration data from a YAML file to create a Dask DataFrame dictionary. The code trains and compares Logistic Regression models from scikit-learn and Dask-ML, showcasing hyperparameter tuning and decision boundary visualization.

### Week_2_4
It demonstrates parallel data generation using Dask, command-line control for parameters, and distributed processing. It also showcases Dask's ability to read, process, and analyze data from CSV files, along with comparing performance between pandas and Dask. Additionally, it employs delayed computation to illustrate efficient task scheduling. This code provides insights into parallel processing, data manipulation, and performance evaluation with Dask.

### Week_2_5
It utilizes Dask to analyze a substantial protein annotation dataset. It performs tasks like cleaning and processing data, computing statistics, and creating visualizations. The script calculates various metrics, including distinct InterPro annotations and protein accessions, average annotations per protein, and correlation between sequence length and feature count. The code also generates scatter plots and identifies common words in InterPro descriptions.

### Week_2_6
This directory consists of two files: 'FlavourDB' encompasses all the revisions and corrections I suggest for this program. Additionally, 'article_summary' encompasses summaries of two articles and answers to the questions posed by our teacher based on these articles.

### Week_2_7
This program constitutes a comprehensive program for processing, analyzing, and modeling time-series sensor data in order to detect anomalies. The program is designed to handle various tasks, from data preprocessing to model training and evaluation, ultimately producing insights and visualizations. The main module, encapsulated within the Main class, orchestrates the entire process. It begins by locating new data files in a target directory, then reads, transforms, predicts, and evaluates the data using a pre-trained machine learning model. The results, including evaluation metrics, anomaly plots, and model predictions, are systematically saved in designated directories.

Two preprocessing classes, DataDivider and ModelTrainer, play crucial roles in preparing the data and training the model, respectively. The DataDivider class converts the input data into time-series format, divides it into training and testing sets, and saves the divided datasets. On the other hand, the ModelTrainer class trains an Isolation Forest model through grid search, optimizing hyperparameters for the best performance. The resulting trained model is stored for future use. 

Moreover, this program contains an analytical notebook that contains all the reasoning and methods that I used during the main pipeline.

The dataset of this pipline is the following dataset.

**Pump Sensor dataset**:

Name: pump_sensor_data

From: https://www.kaggle.com

link: [https://www.kaggle.com/datasets/nphantawee/pump-sensor-data]

Downloading tip: one can easily download the dataset from kaggle website and extract it into a proper folder.

## Challenges
During making this repository, I have faced some challenges:

1. As a physicist, I have many challenges in learning fundamental principles of object-oriented programmin. But I could tackle those problems and learned about the advanced principle such as SOLID.

2. I have some problems using animation library of matplotlib in an observer pattern. Consequently, I wrote my own animation to work harmonously with observer pattern.

3. The challenge that I can encounter for myself while using Dask, was that I could work only on the university's computers for this specific assignment that made me quite limited to the time that university was open.

4. The last Assignment, by far, was the most challenging and simultanously the most inetersting and educational task. I really enjoyed it since I could put everything that I have leaned into practice.
 

## Run and use the program
This program was written in Python 3.9.13 which is the diffult version of Anaconda environment. Also, 
the below packages were used in this program:

async-timeout             4.0.2                    pypi_0    pypi

biopython                 1.81                     pypi_0    pypi

dask                      2023.8.0                 pypi_0    pypi

dask-glm                  0.2.0                    pypi_0    pypi

dask-ml                   2023.3.24                pypi_0    pypi

glob2                     0.7                pyhd3eb1b0_0

ipykernel                 6.15.2           py39haa95532_0

joblib                    1.2.0                    pypi_0    pypi

json5                     0.9.6              pyhd3eb1b0_0

matplotlib                3.2.0                    pypi_0    pypi

matplotlib-inline         0.1.6            py39haa95532_0

networkx                  2.8.4            py39haa95532_0

nltk                      3.7                pyhd3eb1b0_0

node2vec                  0.4.6                    pypi_0    pypi

numpy                     1.21.6                   pypi_0    pypi

opencv-python             4.7.0.72                 pypi_0    pypi

pandas                    2.0.3                    pypi_0    pypi

pathlib                   1.0.1            py39hcbf5309_7    conda-forge

pickleshare               0.7.5           pyhd3eb1b0_1003

pylint                    2.14.5           py39haa95532_0

pygam                     0.9.0                    pypi_0    pypi

pysptools                 0.15.0                   pypi_0    pypi

python                    3.9.13               h6244533_1

regex                     2022.7.9         py39h2bbff1b_0

scanpy                    1.9.4                    pypi_0    pypi

scikit-image              0.19.2           py39hf11a4ad_0

scikit-learn              1.2.2                    pypi_0    pypi

scikit-learn-intelex      2021.6.0         py39haa95532_0

scipy                     1.9.1                    pypi_0    pypi

seaborn                   0.12.2                   pypi_0    pypi

statsmodels               0.13.2           py39h2bbff1b_0

requests                  2.28.1           py39haa95532_0

tensorflow                2.13.0                   pypi_0    pypi

tmtoolkit                 0.12.0                   pypi_0    pypi

typing-extensions         4.3.0            py39haa95532_0

urllib3                   1.26.11          py39haa95532_0

watchdog                  2.1.6            py39haa95532_0

wordcloud                 1.9.2                    pypi_0    pypi

yaml                      0.2.5                he774522_0    conda-forge

Regarding technical aspect of using this repository, one can read each question related to each week on the following link [https://hanze-hbo-ict.github.io/programming2/], then have a look the answers of that question.

The only assignment that should have an instruction is week_2_7. To turn on the machine, one should first adjust all the directories in the config file to work on their computers. Then, first run DataDivider program to make the test and train data., run ModelTrainer module to traina model based on the training datset, and finally run the main program. MyDogWatcher constantly look at the target repository, and when one upload a csv file there it notifies the Main module to start a process.

## Credits
Each assignment may contain its own links and references, so one can find the references inside each notebook, and I just mention the main link of this repo:

https://hanze-hbo-ict.github.io/programming2/

To get access to this repository one can click on the following link

[https://github.com/hooman-b/Programming_2]

## License
apache license 2.0

## Contact Information
Email: h.bahrdo@st.hanze.nl
Phone Number: +31681254428