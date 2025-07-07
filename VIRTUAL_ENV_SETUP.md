****# Virtual Environment Setup for Quantitative Trading

This guide will help you set up a clean Python virtual environment for your quantitative trading project.

## Why Use a Virtual Environment?

- **Isolation**: Keep project dependencies separate from system Python
- **Reproducibility**: Ensure consistent package versions across different machines
- **Clean Dependencies**: Avoid conflicts between different projects
- **Easy Management**: Simple to create, activate, and delete environments

## Setup Instructions

### Option 1: Using Python's built-in `venv` (Recommended)

#### 1. Open PowerShell in your project directory
```powershell
cd "c:\Users\DELL\source\trade"
```

#### 2. Create a virtual environment
```powershell
python -m venv quant_trading_env
```

#### 3. Activate the virtual environment
```powershell
# For PowerShell (Windows)
.\quant_trading_env\Scripts\Activate.ps1

# If you get execution policy error, run this first:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 4. Upgrade pip (recommended)
```powershell
python -m pip install --upgrade pip
```

#### 5. Install requirements
```powershell
pip install -r requirements.txt
```

### Option 2: Using `conda` (If you have Anaconda/Miniconda)

#### 1. Create conda environment
```powershell
conda create -n quant_trading python=3.9
```

#### 2. Activate environment
```powershell
conda activate quant_trading
```

#### 3. Install pip requirements
```powershell
pip install -r requirements.txt
```

## Activation Commands

### Every time you work on the project:

**For venv:**
```powershell
cd "c:\Users\DELL\source\trade"
.\quant_trading_env\Scripts\Activate.ps1
```

**For conda:**
```powershell
conda activate quant_trading
```

## Verification

After installation, verify everything works:
```powershell
python -c "import pandas, numpy, yfinance, matplotlib; print('✅ All packages installed successfully!')"
```

## Jupyter Notebook Setup

To use Jupyter with your virtual environment:

1. With environment activated, install Jupyter kernel:
```powershell
python -m ipykernel install --user --name=quant_trading --display-name="Quantitative Trading"
```

2. Start Jupyter:
```powershell
jupyter notebook
```

3. Select "Quantitative Trading" kernel when creating new notebooks

## Deactivation

To exit the virtual environment:
```powershell
deactivate  # for venv
conda deactivate  # for conda
```

## Troubleshooting

### Common Issues:

1. **PowerShell Execution Policy Error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **Package Installation Fails:**
   - Ensure you have Microsoft Visual C++ Build Tools installed
   - For TA-Lib, you might need to install from wheel: `pip install TA-Lib --find-links https://www.lfd.uci.edu/~gohlke/pythonlibs/`

3. **Permission Errors:**
   - Run PowerShell as Administrator
   - Or use `--user` flag: `pip install --user -r requirements.txt`

## Environment Management

### List installed packages:
```powershell
pip list
```

### Export current environment:
```powershell
pip freeze > requirements_current.txt
```

### Delete environment:
```powershell
# For venv
rmdir /s quant_trading_env

# For conda
conda env remove -n quant_trading
```

## Quick Start Script

I've created an automated setup script (`setup_env.ps1`) that will handle the entire process for you!
