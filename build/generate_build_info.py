"""
generate_build_info.py
Saves build info as a .json file
If BRANCH_NAME is not main, appends build timestamp to pyproject version
"""
import os
import subprocess
import json
import toml
from datetime import datetime

if __name__=="__main__":
    #Scraping info
    env_vars=[
        "START_TIME",
        "BRANCH_NAME",
        "GIT_COMMIT"
    ]
    if all(os.environ.get(x) for x in env_vars):
        build_info={x:os.environ.get(x) for x in env_vars}
    else:
        build_info={
            "START_TIME":datetime.now().strftime('%Y%m%d%H%M'),
            "BRANCH_NAME":subprocess.check_output("git rev-parse --abbrev-ref HEAD",shell=True,text=True).strip(),
            "GIT_COMMIT":subprocess.check_output("git rev-parse HEAD",shell=True,text=True).strip(),
        }
    build_info["GIT_COMMIT"]=build_info["GIT_COMMIT"][:7]
    
    #Saving build info file
    root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path=os.path.join(root,"src","SVGPatcher","build_info.json")
    with open(output_path,"w") as write_obj:
        json.dump(build_info,write_obj,indent=2)
    print(f"Generated {output_path}")

    #Updating pyproject version for non-main build
    if build_info["BRANCH_NAME"]!="main":
        pyproject_path=os.path.join(root,"pyproject.toml")
        pyproject=toml.load(pyproject_path)
        version_new=f"{pyproject['project']['version']}.{build_info['START_TIME']}"
        pyproject["project"]["version"]=version_new
        with open(pyproject_path,"w") as write_obj:
            toml.dump(pyproject,write_obj)
        print(f"Updated pyproject version to: {version_new}")