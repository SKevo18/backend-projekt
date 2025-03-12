# cd in dir of script
$scriptPath = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path -Path $scriptPath -Parent
Set-Location -Path $scriptDir

# set env
if (-not $env:DB_ROOT_PASSWORD) {
    $secureRootPwd = Read-Host -Prompt "'DB_ROOT_PASSWORD' = " -AsSecureString
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureRootPwd)
    $env:DB_ROOT_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
}

if (-not $env:DB_PASSWORD) {
    $securePwd = Read-Host -Prompt "'DB_PASSWORD' = " -AsSecureString
    $bstr = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($securePwd)
    $env:DB_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($bstr)
    [System.Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
}

# run (default profile - HTTP only)
docker compose --profile="default" -f docker-compose.yaml up --build -d --force-recreate
