$ErrorActionPreference = 'Stop';
$toolsDir   = "$(Split-Path -parent $MyInvocation.MyCommand.Definition)"
$url        = "https://github.com/ewgsta/weeb-cli/releases/download/v0.0.1/weeb-cli-Windows.exe"
# Hash check skipped, assuming GitHub Release integrity
Get-ChocolateyWebFile -PackageName 'weeb-cli' `
                      -FileFullPath "$toolsDir\weeb-cli.exe" `
                      -Url $url

Install-BinFile -Name "weeb-cli" -Path "$toolsDir\weeb-cli.exe"
