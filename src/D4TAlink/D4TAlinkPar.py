"""
D4TAlinkPar

D4TAlink globals. 
"""

__all__ = ["setTaskRoot",
           "getTaskRoot",
           "setTaskSponsor",
           "getTaskSponsor",
           "setTaskAuthor",
           "getTaskAuthor"]

import os

# -------------------------------------------------------------------------------
def D4TAlinkInit():
    """Initialize the global variables for the D4TAlink module."""
    if not "_D4TAlinkPar" in globals():
        global _D4TAlinkPar
        globals()["_D4TAlinkPar"] = {}
        globals()["_D4TAlinkPar"]["author"] = os.getlogin()
# -------------------------------------------------------------------------------
D4TAlinkInit()
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
def setTaskRoot(root, dirCreate = False):
    """Set the root directory for the tasks. This is the directory where the tasks are stored. The root directory should contain subdirectories for each sponsor, project, and package. The task files are stored in the package directory. The root directory should be a string with the full path to the root directory. The function returns the root directory.
    
    Attributes:
    root (str): The root directory for the tasks.

    Returns:
    str: The root directory for the tasks.
    """
    if dirCreate:
        os.makedirs(root, exist_ok = True)
    if not os.path.exists(root):
        raise FileNotFoundError(f"Root directory '{root}' does not exist.")
    D4TAlinkInit()
    globals()["_D4TAlinkPar"]["root"] = root
    return globals()["_D4TAlinkPar"]["root"]
# -------------------------------------------------------------------------------
def getTaskRoot():
    """Get the root directory for the tasks. This is the directory where the tasks are stored. The root directory should contain subdirectories for each sponsor, project, and package. The task files are stored in the package directory. The root directory should be a string with the full path to the root directory. The function returns the root directory.
    
    Returns:
    str: The root directory for the tasks.
    """
    v = globals()["_D4TAlinkPar"]["root"]
    if not os.path.exists(v):
        raise FileNotFoundError(f"Root directory '{v}' does not exist.")
    return v
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
def setTaskSponsor(sponsor):
    """Set the sponsor for the tasks. The sponsor is the organization responsible for the tasks. The sponsor should be a string with the name of the sponsor. The function returns the sponsor.
    
    Attributes:
    sponsor (str): The sponsor for the tasks.
    
    Returns:
    str: The sponsor for the tasks.
    """
    D4TAlinkInit()
    globals()["_D4TAlinkPar"]["sponsor"] = sponsor
    return globals()["_D4TAlinkPar"]["sponsor"]
# -------------------------------------------------------------------------------
def getTaskSponsor():
    """Get the sponsor for the tasks. The sponsor is the organization responsible for the tasks. The sponsor should be a string with the name of the sponsor. The function returns the sponsor.
    
    Returns:
    str: The sponsor for the tasks.
    """
    v = globals()["_D4TAlinkPar"]["sponsor"]
    if v is None:
        raise ValueError("Sponsor is not defined.")
    return v
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
def setTaskAuthor(author):
    """Set the author for the tasks. The author is the statistician responsible for the task. The author should be a string with the name of the author. The function returns the author.
    
    Attributes:
    author (str): The author for the tasks.
    
    Returns:
    str: The author for the tasks.
    """
    D4TAlinkInit()
    globals()["_D4TAlinkPar"]["author"] = author
    return globals()["_D4TAlinkPar"]["author"]
# -------------------------------------------------------------------------------
def getTaskAuthor():
    """Get the author for the tasks. The author is the statistician responsible for the tasks. The author should be a string with the name of the author. The function returns the author.
    
    Returns:
    str: The author for the tasks.
    """
    v = globals()["_D4TAlinkPar"]["author"]
    if v is None:
        raise ValueError("Author is not defined.")
    return v
# -------------------------------------------------------------------------------

