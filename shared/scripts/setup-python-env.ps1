# PowerShell Script to Setup Python Environment for Data Science Projects
param(
    [Parameter(Mandatory = $true)]
    [string]$EnvName,
    
    [Parameter(Mandatory = $false)]
    [string]$PythonVersion = "3.11",
    
    [Parameter(Mandatory = $false)]
    [string[]]$Packages = @("pandas", "numpy", "matplotlib", "seaborn", "jupyter", "scikit-learn")
)

Write-Host "🐍 Setting up Python environment: $EnvName" -ForegroundColor Green

# Check if conda is available
if (Get-Command conda -ErrorAction SilentlyContinue) {
    Write-Host "📦 Using Conda for environment management" -ForegroundColor Yellow
    
    # Create conda environment
    conda create -n $EnvName python=$PythonVersion -y
    
    # Activate environment and install packages
    conda activate $EnvName
    
    foreach ($package in $Packages) {
        Write-Host "📥 Installing $package..." -ForegroundColor Cyan
        conda install $package -y
    }
    
    Write-Host "✅ Environment '$EnvName' created successfully!" -ForegroundColor Green
    Write-Host "📝 To activate: conda activate $EnvName" -ForegroundColor Blue
    
}
elseif (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "📦 Using Python venv for environment management" -ForegroundColor Yellow
    
    # Create virtual environment
    python -m venv $EnvName
    
    # Activate environment
    & "$EnvName\Scripts\Activate.ps1"
    
    # Install packages
    foreach ($package in $Packages) {
        Write-Host "📥 Installing $package..." -ForegroundColor Cyan
        pip install $package
    }
    
    Write-Host "✅ Environment '$EnvName' created successfully!" -ForegroundColor Green
    Write-Host "📝 To activate: $EnvName\Scripts\Activate.ps1" -ForegroundColor Blue
    
}
else {
    Write-Error "❌ Python not found. Please install Python or Anaconda first."
    exit 1
}

Write-Host "`n🎯 Next steps:" -ForegroundColor Magenta
Write-Host "1. Activate your environment" -ForegroundColor White
Write-Host "2. Navigate to your project folder" -ForegroundColor White  
Write-Host "3. Start coding! 🚀" -ForegroundColor White