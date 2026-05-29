"""
check_version.py
If branch is not main, appends timestamp to pyproject version
"""
import os
import subprocess
import toml
from datetime import datetime

if __name__=="__main__":
    timestamp=datetime.now().strftime('%Y%m%d%H%M')
    branch=subprocess.check_output("git rev-parse --abbrev-ref HEAD",shell=True,text=True).strip()
    if branch!="main":
        root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path=os.path.join(root,"pyproject.toml")
        pyproject=toml.load(pyproject_path)
        version_new=f"{pyproject['project']['version']}.{timestamp}"
        pyproject['project']['version']=version_new
        with open(pyproject_path,"w") as f:
            toml.dump(pyproject,f)
        print(f"Updated pyproject version to: {version_new}")