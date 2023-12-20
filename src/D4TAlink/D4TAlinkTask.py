"""
D4TAlinkTask

D4TAlink Task class. 
"""

__all__ = ["loadTask",
           "Task"]

from datetime import datetime
import os
from pathlib import Path
import json
import pickle
import pandas as pd
from .D4TAlinkPar import *

# -------------------------------------------------------------------------------
def loadTask(project, package, taskname, sponsor=None, quiet=False):
    """Load a task from the task files. The task is identified by the project, package, and taskname. The function returns the task object. If the task does not exist, the function raises a FileNotFoundError exception. If the sponsor is not specified, the function uses the default sponsor. If the task does not exist and the quiet parameter is set to True, the function returns None. If the task does not exist and the quiet parameter is set to False, the function raises a FileNotFoundError exception.
    
    Attributes:
    project (str): The project for the task.
    package (str): The package for the task.
    Taskname (str): The name of the task.
    sponsor (str): The sponsor for the task (optional).
    quiet (bool): A flag to suppress the FileNotFoundError exception.

    Returns:
    Task: The task object.
    """
    if sponsor is None:
        sponsor = getTaskSponsor()
    ta = Task(project, package, taskname, sponsor, author="-",blank=True)
    fn = ta.binaryFn("task",'json')
    task = None
    if(not quiet and not os.path.exists(fn)):
        raise FileNotFoundError(f"Task '{taskname}' does not exist: '{fn}'")
    elif(os.path.exists(fn)):
        with open(fn,"r") as fp:
            ita = json.load(fp)
        for(k,v) in ita.items():
            if isinstance(getattr(ta,k), str) and not isinstance(v, str):
                if not hasattr(v, 'join'):
                    v = "\n".join(v)
            setattr(ta,k,v)
        task = ta
    else :
        task = None
    return task
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
class Task:
    """The Task class represents a task in the D4TAlink framework. A task is a unit of work that is performed by a sponsor on a project and package. The task has a name, sponsor, author, date, version, and dependencies. The task also has directories for documentation, code, data, and data source. The task has methods to get the file paths for the task files.
    
    Attributes:
    project (str): The project for the task.
    package (str): The package for the task.
    taskname (str): The name of the task.
    sponsor (str): The sponsor for the task.
    author (str): The author of the task.
    date (str): The date of the task.
    version (str): The version of the task.
    dependencies (str): The dependencies of the task.
    footer (str): The footer for the task reports.
    copyright (str): The copyright for the task reports.

    Methods:
    getTaskPaths(dirCreate=False): Get the paths for the task directories.
    getTaskFilepath(type,ext,dirtype,subdir=None,dirCreate=True): Get the file path for a task file.
    docFn(type,ext,subdir=None,dirCreate=True): Get the file path for a documentation file.
    binaryFn(type,ext,subdir=None,dirCreate=True): Get the file path for a binary file.
    reportFn(type,ext,subdir=None,dirCreate=True): Get the file path for a report file.
    dataSourceFn(type,ext,subdir=None,dirCreate=True): Get the file path for a data source file.
    docDir(subdir=None,dirCreate=True): Get the directory for a documentation file.
    binaryDir(subdir=None,dirCreate=True): Get the directory for a binary file.
    reportDir(subdir=None,dirCreate=True): Get the directory for a report file.
    dataSourceDir(subdir=None,dirCreate=True): Get the directory for a data source file.
    """
    # -------------------------------------
    def __init__(self,
                 project, package, taskname, sponsor=None, author=None, 
                 overwrite=False,blank=False):
        """
        Initialize the Task object.
        
        Attributes:
        project (str): The project for the task.
        package (str): The package for the task.
        taskname (str): The name of the task.
        sponsor (str): The sponsor for the task.
        author (str): The author of the task.
        overwrite (bool): A flag to overwrite an existing task.
        blank (bool): A flag to create a blank task.

        Returns:
        Task: The task object.
        """
        if sponsor is None:
            sponsor = getTaskSponsor()
        if author is None:
            author = getTaskAuthor()
        if blank :
            sessionStr = ""
            yr = datetime.now().strftime('%Y')
            dt = datetime.now().strftime('%Y-%m-%d')
            self.task      = taskname
            self.project   = project
            self.package   = package
            self.sponsor   = sponsor
            self.author    = author
            self.copyright = f"Copyright (c) {sponsor} {yr}"
            self.date      = dt
            self.footer    = f"Copyright (c) {sponsor} {yr} - CONFIDENTIAL"
            self.version   = "0.0"
            self.dependencies = sessionStr
        else :
            ta = Task(project, package, taskname, sponsor, author, blank=True)
            #print(ta.__dict__)
            self.__dict__.update(ta.__dict__)
            #print(self.__dict__)
            fn = ta.binaryFn("task",'json')
            if os.path.exists(fn) and not overwrite:
                raise FileExistsError(f"Task '{taskname}' already exists.")
            with open(fn,"w") as fp:
                json.dump(self.__dict__,fp)
        return None
    # -------------------------------------
    def __str__(self):
        return(self.sponsor + " - " + self.project + " - " + 
               self.package + " - " + self.task)
    # -------------------------------------
    def getTaskPaths(self,dirCreate=False):
        """Get the paths for the task directories. The function returns a dictionary with the paths for the task directories. The directories are created if the dirCreate parameter is set to True.
        
        Attributes:
        dirCreate (bool): A flag to create the directories.
        
        Returns:
        dict: The paths for the task directories.
        """
        taskRoot = os.path.join(getTaskRoot(),
                                self.sponsor,
                                self.project,
                                self.package)
        taskPaths = {
            "documentation": os.path.join(taskRoot,"docs"),
            "code": os.path.join(taskRoot,"progs"),
            "data": os.path.join(taskRoot,"output",self.task),
            "data_source": os.path.join(taskRoot,"raw"),
            "binary_data": os.path.join(taskRoot,"output",self.task,"bin"),
            "binary": os.path.join(taskRoot,"output",self.task,"bin")
        }
        if(dirCreate):
            for path in taskPaths.values():
                Path(path).mkdir(parents=True,exist_ok=True)
        return taskPaths
    # -------------------------------------
    def getTaskFilepath(self,type,ext,dirtype,subdir=None,dirCreate=True):
        """Get the file path for a task file. The file path is constructed from the task directories, the file type, and the file extension. The file path is returned as a string. The file path is created if the dirCreate parameter is set to True.

        Attributes:
        type (str): The type of the file.
        ext (str): The extension of the file.
        dirtype (str): The type of the directory.
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.

        Returns:
        str: The file path for the task file.
        """
        if not isinstance(type, str):
            if not hasattr(type, 'join'):
                type = "-".join(type)
        pz = self.getTaskPaths(dirCreate=dirCreate)
        if dirtype not in pz:
            raise ValueError(f"Directory type '{dirtype}' not recognized.")
        path = pz[dirtype]
        if not subdir is None:
            path = os.path.join(path,subdir)
        if dirCreate:
            Path(path).mkdir(parents=True,exist_ok=True)
        fn = os.path.join(path,f"{self.task}_{type}.{ext}")
        return fn
    # -------------------------------------
    def docFn(self,type,ext,subdir=None,dirCreate=True):
        """Get the file path for a documentation file. The file path is constructed from the task directories, the file type, and the file extension. The file path is returned as a string. The file path is created if the dirCreate parameter is set to True.
        
        Attributes:
        type (str): The type of the file.
        ext (str): The extension of the file.
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.

        Returns:
        str: The file path for the documentation file.
        """
        return self.getTaskFilepath(type,ext,"documentation",subdir,dirCreate)
    def binaryFn(self,type,ext,subdir=None,dirCreate=True):
        """Get the file path for a binary file. The file path is constructed from the task directories, the file type, and the file extension. The file path is returned as a string. The file path is created if the dirCreate parameter is set to True.
        
        Attributes:
        type (str): The type of the file.
        ext (str): The extension of the file.
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.
        
        Returns:
        str: The file path for the binary file.
        """
        return self.getTaskFilepath(type,ext,"binary",subdir,dirCreate)
    def reportFn(self,type,ext,subdir=None,dirCreate=True):
        """Get the file path for a report file. The file path is constructed from the task directories, the file type, and the file extension. The file path is returned as a string. The file path is created if the dirCreate parameter is set to True.

        Attributes:
        type (str): The type of the file.
        ext (str): The extension of the file.
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.

        Returns:
        str: The file path for the report file.
        """
        return self.getTaskFilepath(type,ext,"data",subdir,dirCreate)
    def dataSourceFn(self,type,ext,subdir=None,dirCreate=True):
        """Get the file path for a data source file. The file path is constructed from the task directories, the file type, and the file extension. The file path is returned as a string. The file path is created if the dirCreate parameter is set to True.

        Attributes:
        type (str): The type of the file.
        ext (str): The extension of the file.
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.

        Returns:
        str: The file path for the data source file.
        """
        return self.getTaskFilepath(type,ext,"data_source",subdir,dirCreate)
    # -------------------------------------
    def docDir(self,subdir=None,dirCreate=True):
        """Get the directory for a documentation file. The directory is created if the dirCreate parameter is set to True. The directory is returned as a string.

        Attributes:
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.

        Returns:
        str: The directory for the documentation file.
        """
        return Path(self.getTaskFilepath("a","a","documentation",subdir,dirCreate)).parent.absolute()
    def binaryDir(self,subdir=None,dirCreate=True):
        """Get the directory for a binary file. The directory is created if the dirCreate parameter is set to True. The directory is returned as a string.
        
        Attributes:
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.
        
        Returns:
        str: The directory for the binary file.
        """
        return Path(self.getTaskFilepath("a","a","binary",subdir,dirCreate)).parent.absolute()
    def reportDir(self,subdir=None,dirCreate=True):
        """Get the directory for a report file. The directory is created if the dirCreate parameter is set to True. The directory is returned as a string.
        
        Attributes:
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.
        
        Returns:
        str: The directory for the report file.
        """
        return Path(self.getTaskFilepath("a","a","data",subdir,dirCreate)).parent.absolute()
    def dataSourceDir(self,subdir=None,dirCreate=True):
        """Get the directory for a data source file. The directory is created if the dirCreate parameter is set to True. The directory is returned as a string.
        
        Attributes:
        subdir (str): The subdirectory for the file (optional).
        dirCreate (bool): A flag to create the directory.
        
        Returns:
        str: The directory for the data source file.
        """
        return Path(self.getTaskFilepath("a","a","data_source",subdir,dirCreate)).parent.absolute()
    # -------------------------------------
    def saveBinary(self,obj,type,subdir=None):
        """Save a binary object to a file. The object is saved to a binary file. The file path is constructed from the task directories, the file type, and the file extension. The file path is created if it does not exist. The object is saved to the file using the pickle module.
        
        Attributes:
        obj (object): The object to save.
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).

        Returns:
        str: The file path for the binary file.
        """
        fn = self.binaryFn(type,"pkl",subdir)
        with open(fn,"wb") as fp:
            pickle.dump(obj,fp)
        return fn
    # -------------------------------------
    def loadBinary(self,type,subdir=None):
        """Load a binary object from a file. The object is loaded from a binary file. The file path is constructed from the task directories, the file type, and the file extension. The object is loaded from the file using the pickle module. The object is returned.
        
        Attributes:
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).
        
        Returns:
        object: The object loaded from the file.
        """
        fn = self.binaryFn(type,"pkl",subdir)
        with open(fn,"rb") as fp:
            obj = pickle.load(fp)
        return obj
    # -------------------------------------
    def saveReportXls(self,df,type,subdir=None):
        """Save a DataFrame to a report file. The DataFrame is saved to an Excel file. The file path is constructed from the task directories, the file type, and the file extension. The file path is created if it does not exist. The DataFrame is saved to the file using the to_excel method.
        
        Attributes:
        df (DataFrame): The DataFrame to save.
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).

        Returns:
        str: The file path for the Excel file.
        """
        fn = self.reportFn(type,"xlsx",subdir)
        df.to_excel(fn,sheet_name='worksheet',index=False)
        return fn
    # -------------------------------------
    def loadReportXls(self,type,subdir=None):
        """Load a DataFrame from a report file. The DataFrame is loaded from an Excel file. The file path is constructed from the task directories, the file type, and the file extension. The DataFrame is loaded from the file using the read_excel method. The DataFrame is returned.
        
        Attributes:
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).
        
        Returns:
        DataFrame: The DataFrame loaded from the file.
        """
        fn = self.reportFn(type,"xlsx",subdir)
        df = pd.read_excel(fn,sheet_name='worksheet')
        return df
    # -------------------------------------
    def saveReportCsv(self,df,type,subdir=None,sep=",",encoding="utf-8"):
        """Save a DataFrame to a report file. The DataFrame is saved to a CSV file. The file path is constructed from the task directories, the file type, and the file extension. The file path is created if it does not exist. The DataFrame is saved to the file using the to_csv method.
        
        Attributes:
        df (DataFrame): The DataFrame to save.
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).
        sep (str): The separator for the CSV file.
        encoding (str): The encoding for the CSV file.

        Returns:
        str: The file path for the CSV file.
        """
        fn = self.reportFn(type,"csv",subdir)
        df.to_csv(fn,index=False,sep=sep,encoding=encoding)
        return fn
    # -------------------------------------
    def loadReportCsv(self,type,subdir=None,sep=",",encoding="utf-8"):
        """Load a DataFrame from a report file. The DataFrame is loaded from a CSV file. The file path is constructed from the task directories, the file type, and the file extension. The DataFrame is loaded from the file using the read_csv method. The DataFrame is returned.
        
        Attributes:
        type (str): The type of the file.
        subdir (str): The subdirectory for the file (optional).
        sep (str): The separator for the CSV file.
        encoding (str): The encoding for the CSV file.
        
        Returns:
        DataFrame: The DataFrame loaded from the file.
        """
        fn = self.reportFn(type,"csv",subdir)
        df = pd.read_csv(fn,sep=sep,encoding=encoding)
        return df
# -------------------------------------------------------------------------------

