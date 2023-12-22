import d4talink as D4
import pandas as pd
import string
import shutil
import os

mydir = "~/exampleD4TArepository"
mydir = os.path.expanduser(mydir)

# 1. Clean up
if os.path.exists(mydir):
    shutil.rmtree(mydir)

# 2. Parametrise 
D4.setTaskAuthor("Doe Johns")
D4.setTaskSponsor("myClient")
D4.setTaskRoot(mydir, dirCreate = True)

# 3. Create two tasks (```package``` refers here to a _work package_)
task1 = D4.Task(project = "DiseaseABC", 
                package = "myStudy", 
                taskname = "20220901_myFirstAnalysis")
task2 = D4.Task(project = "DiseaseABC", 
                package = "myStudy", 
                taskname = "20220905_mySecondAnalysis")

#4. List the tasks in repository

# 5. Load a task from the repository 
mytask = D4.loadTask(project = "DiseaseABC", 
                     package = "myStudy", 
                     taskname = "20220905_mySecondAnalysis")

# 6. Add data to a task
d = {"letters" : pd.DataFrame({"a" : list(string.ascii_uppercase), 
                               "b" : list(string.ascii_lowercase), 
                               "c" : list(range(0,
                                             len(list(string.ascii_lowercase))))}), 
     "other" : pd.DataFrame({"a" : [1,2,3], 
                             "b" : [11,12,13]})}
mytask.saveBinary(d, "myTables")

# 7. Load data from a task
e  = mytask.readBinary("myTables")

# 8. Add reports to a task
efn = mytask.saveReportXls(d, "tables")

csvfile = mytask.saveReportCsv(d["letters"], "tables")
print(csvfile)

# 99. Clean up
if os.path.exists(mydir):
    shutil.rmtree(mydir)
