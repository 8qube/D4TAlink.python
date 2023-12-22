% D4TAlink - python

<!--ts-->
   1. [Introduction](#introduction)
   2. [Installation](#installation)
   3. [Quick start](#quick-start)
   4. [Usage](#usage)

<!--te-->


# 1. Introduction

[D4TAlink](https://bitbucket.org/SQ4/d4talink.python/) is a python
package integrating [D4TAlink](https://d4ta.link/)'s python methods. [D4TAlink](https://d4ta.link/) enables seamless compliance with FAIR data and ALCOA principles. 

[D4TAlink](https://d4ta.link/)'s key features:

* speed up data analytics and statistics projects,
* reduce resources and lower costs, 
* enable traceability and reproducibility seamlessly, 
* unclog data analysts' life, 
* ease collaboration, 
* facilitate validation and review processes, 
* open, easy and light weight.

[D4TAlink](https://d4ta.link/) is a software suite for the management of data analytics projects
developed and distributed by [SQU4RE](https://SQU4RE.com).

See also: 

1. FAIR principles: Jacobsen et al., 2017 ([doi:10.1162/dint_r_00024](https://doi.org/10.1162/dint_r_00024))
2. ALCOA principles: Food & Drug Administration, 2018 ([Data Integrity and Compliance With Drug CGMP - Questions and Answers Guidance for Industry](<https://www.fda.gov/regulatory-information/search-fda-guidance-documents/data-integrity-and-compliance-drug-cgmp-questions-and-answers-guidance-industry>)).

# 2. Installation #


# 3. Quick start #

1. Load [D4TAlink.light](https://bitbucket.org/SQ4/d4talink.light/)
```py
import d4talink as D4
```

2. Parametrise 
```py
D4.setTaskAuthor("Doe Johns")
D4.setTaskSponsor("myClient")
D4.setTaskRoot("~/myDataRepository", dirCreate = True)
```

3. Create two tasks (```package``` refers here to a _work package_)
```py
task1 = D4.Task(project = "DiseaseABC", 
                package = "myStudy", 
                taskname = "20220901_myFirstAnalysis")
task2 = D4.Task(project = "DiseaseABC", 
                package = "myStudy", 
                taskname = "20220905_mySecondAnalysis")
```

4. List the tasks in repository
```py
```

5. Load a task from the repository 
```py
mytask = D4.loadTask(project = "DiseaseABC", 
                     package = "myStudy", 
                     taskname = "20220905_mySecondAnalysis")
```

6. Add data to a task
```py
import pandas as pd
import string
d = {"letters" : pd.DataFrame({"a" : list(string.ascii_uppercase), 
                               "b" : list(string.ascii_lowercase), 
                               "c" : list(range(0,
                                             len(list(string.ascii_lowercase))))}), 
     "other" : pd.DataFrame({"a" : [1,2,3], 
                             "b" : [11,12,13]})}
mytask.saveBinary(d, "myTables")
```

7. Load data from a task
```py
e  = mytask.readBinary("myTables")
```

8. Add reports to a task
```R
excelfilename = mytask.saveReportXls(d, "tables")

csvfile = mytask.saveReportCsv(d["letters"], "tables")
print(csvfile)
```


# 4. Usage #

...


<sup><sub>Copyright &copy; 2016-2022 [SQU4RE](https://squ4re.com/). [SQU4RE](https://squ4re.com/) and [D4TAlink](https://D4TA.link/) are registered trademarks.</sub></sup>
