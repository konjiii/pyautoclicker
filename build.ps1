$binary_name = "pyautoclicker.exe"

# Function to display spinner with a message
function Loading {
    param(
        [Parameter(Mandatory)]
        [string]$Message,
        [Parameter(Mandatory)]
        [scriptblock]$ScriptBlock
    )

    # loading animations
    $spinner = if ($PSVersionTable.PSVersion.Major -ge 7) {
        @("⠧","⠏","⠛","⠹", "⠼", "⠶")
    } else {
        @("/", "-", "\", "|")
    }

    $index = 0
    $job = Start-Job -ScriptBlock {
        # set location to current one and execute scriptblock
        powershell -noprofile -command "Set-Location $using:PWD ; $($using:ScriptBlock)" 
    }

    while ($job.State -eq 'Running') {
        # Capture job outputs and errors and write it above the spinner line
        Receive-Job -Job $job -OutVariable out -ErrorVariable err -ErrorAction SilentlyContinue | Out-Null
        if ($out) {
            $currentLine = [Console]::CursorTop
            $formattedOut = $out -join "`n"
            # move one line up
            [Console]::SetCursorPosition(0, $currentLine - 1)
            # create new line
            Write-Host ""
            # empty new line
            [Console]::Write(" " * ([Console]::WindowWidth - 1))
            # move back to start of line
            [Console]::SetCursorPosition(0, $currentLine)
            Write-Host $formattedOut
        }
        if ($err) {
            $currentLine = [Console]::CursorTop
            $formattedErr = $err -join "`n"
            [Console]::SetCursorPosition(0, $currentLine - 1)
            Write-Host ""
            [Console]::Write(" " * ([Console]::WindowWidth - 1))
            [Console]::SetCursorPosition(0, $currentLine)
            Write-Host $formattedErr
        }
        
        $currentLine = [Console]::CursorTop
        # Go back to lowest line and update spinner
        [Console]::SetCursorPosition(0, $currentLine)
        $spinnerChar = $spinner[$index % $spinner.Count]
        Write-Host -NoNewLine "$spinnerChar $Message..." -ForegroundColor Cyan
        $index++
        # sleep 100 ms so not too much cpu resources are used
        Start-Sleep -Milliseconds 100
    }

    # Cleanup
    # Capture job outputs and errors and write it above the spinner line
    Receive-Job -Job $job -OutVariable out -ErrorVariable err -ErrorAction SilentlyContinue | Out-Null
    if ($out) {
        $currentLine = [Console]::CursorTop
        $formattedOut = $out -join "`n"
        [Console]::SetCursorPosition(0, $currentLine - 1)
        Write-Host ""
        [Console]::Write(" " * ([Console]::WindowWidth - 1))
        [Console]::SetCursorPosition(0, $currentLine)
        Write-Host $formattedOut
    }
    if ($err) {
        $currentLine = [Console]::CursorTop
        $formattedErr = $err -join "`n"
        [Console]::SetCursorPosition(0, $currentLine - 1)
        Write-Host ""
        [Console]::Write(" " * ([Console]::WindowWidth - 1))
        [Console]::SetCursorPosition(0, $currentLine)
        Write-Host $formattedErr -ForegroundColor Red
    }
    
    # finish with a Done message
    Write-Host "`r$Message Done" -ForegroundColor Green
    Write-Host ""
}

Write-Output "creating virtual environment..."

# Download Winpython 3.13.2
Loading -Message "Downloading Winpython" -ScriptBlock {
    Invoke-WebRequest -Uri https://github.com/winpython/winpython/releases/download/11.2.20241228final/Winpython64-3.13.1.0dot.zip -OutFile Winpython64-3.13.1.zip
}

# Extract Winpython
Loading -Message "Extracting Winpython" -ScriptBlock {
    tar -xf .\Winpython64-3.13.1.zip
}

# activating environment
.\WPy64-31310\scripts\WinPython_PS_Prompt.ps1

# Installing required packages
Write-Output "building application..."

Loading -Message "Installing packages" -ScriptBlock {
    pip install -r .\requirements.txt --disable-pip-version-check
}

# Build application
Loading -Message "Building application" -ScriptBlock ([scriptblock]::Create(@"
    pyinstaller .\main.py --noconfirm --onefile --windowed --icon .\textures\icon.ico
    Move-Item .\dist\main.exe $binary_name -Force
"@))

# Move binary and clean up
Write-Output "cleaning up..."

Loading -Message "Removing Python" -ScriptBlock {
    Remove-Item -Recurse -Force dist, build, main.spec
    # Uninstall Python
    Remove-Item -Recurse -Force .\WPy64-31310
    Remove-Item .\Winpython64-3.13.1.zip
}

Write-Output "build finished. resulting binary is $binary_name"
