# BioRing Verification and Validation (V&V) Tools

## Environment setup


### Windows

- Install [pyenv-win](https://github.com/pyenv-win/pyenv-win) to manage Python versions.
- Install Python **3.10.11** using pyenv-win.
- Open this repo in **Git Bash** and run:

  ```bash
  # Create virtual environment folder
  python -m venv .venv
  
  # Activate virtual environment (bash)
  source .venv/Scripts/activate

  # Install Python dependencies
  python -m pip install -r setup/requirements_lock.txt
  ```

- Install VSCode extensions:
  - [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  - [Python Environment Manager](https://marketplace.visualstudio.com/items?itemName=donjayamanne.python-environment-manager): this extension will help create and automatically activate the virtual environment whenever you open this repo in VSCode.

### Run

- Option 1: Double click to `bioring_tool.bat`
- Option 2: From cmd.exe, execute command `bioring_tool.bat`
