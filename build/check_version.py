"""
check_version.py
If branch is not main, appends timestamp to pyproject version
"""
import os
import subprocess
import toml
from datetime import datetime

def get_branch_name()->str:
    """
    get_branch_name():
    Return the current git branch name
    """
    #Jenkins environment variable
    branch=os.environ.get('BRANCH_NAME')
    if branch:
        return branch

    #git checkout fallback
    try:
        branch=subprocess.check_output('git branch --show-current',text=True).strip()
        if branch:
            return branch
    except subprocess.CalledProcessError:
        pass

    #Detached HEAD fallback
    return 'HEAD'

if __name__=='__main__':
    timestamp=datetime.now().strftime('%Y%m%d%H%M')
    branch=get_branch_name()
    if branch!='main':
        root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path=os.path.join(root,'pyproject.toml')
        pyproject=toml.load(pyproject_path)
        version_new=f"{pyproject['project']['version']}.{timestamp}"
        pyproject['project']['version']=version_new
        with open(pyproject_path,'w') as f:
            toml.dump(pyproject,f)
        print(f'Updated pyproject version to: {version_new}')