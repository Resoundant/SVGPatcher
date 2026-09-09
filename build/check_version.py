"""
check_version.py
For non-main branches, writes a PEP 440 local version to pyproject.toml using
the branch name and build timestamp (for example, ``0.3.1+feature.20260828-153045``).
"""
import os
import re
import subprocess
import tomllib
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
        branch=subprocess.check_output(
            ["git", "branch", "--show-current"], text=True
        ).strip()
        if branch:
            return branch
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    #Detached HEAD fallback
    return 'HEAD'

if __name__=='__main__':
    timestamp=datetime.now().strftime('%Y%m%d-%H%M%S')
    branch=get_branch_name()
    if branch!='main':
        root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        pyproject_path=os.path.join(root,'pyproject.toml')
        with open(pyproject_path, 'rb') as f:
            pyproject=tomllib.load(f)
        version_old=pyproject['project']['version']
        # Drop the development and local-version suffixes left by a previous
        # build so rerunning in the same Jenkins workspace starts from the
        # stable version.
        version_base=version_old.split("+", 1)[0]
        version_base=re.sub(r'\.dev\d*$', '', version_base)
        branch_sanitized=re.sub(r'[^A-Za-z0-9]', '_', branch)
        version_new=f"{version_base}.dev+{branch_sanitized}.{timestamp}"

        # Replace only the version in [project], preserving formatting and all
        # other project metadata instead of rewriting the complete TOML file.
        with open(pyproject_path, newline='') as f:
            pyproject_text=f.read()
        before_project, project_marker, remaining=pyproject_text.partition('[project]')
        if not project_marker:
            raise ValueError('pyproject.toml has no [project] section')
        project_body, section_marker, later_sections=remaining.partition('\n[')
        version_pattern=r'(?m)^(version\s*=\s*)"[^"]*"'
        project_body, replacements=re.subn(
            version_pattern, rf'\g<1>"{version_new}"', project_body, count=1
        )
        if replacements != 1:
            raise ValueError('pyproject.toml has no project version')
        with open(pyproject_path, 'w', newline='') as f:
            f.write(
                before_project + project_marker + project_body
                + section_marker + later_sections
            )
        print(f'Updated pyproject version to: {version_new}')
