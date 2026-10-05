# Daily RegIntel update from a residential connection.
# BPK's WAF blocks GitHub-hosted runners (403), so this runs on the owner's PC via Task Scheduler
# from a dedicated clone (default D:\ketikyuk-regintel-bot) that nobody edits by hand.
$ErrorActionPreference = "Stop"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$logDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir ("run_" + (Get-Date -Format "yyyy-MM-dd") + ".log")
$env:PYTHONIOENCODING = "utf8"

function Say($msg) { "$(Get-Date -Format 'HH:mm:ss')  $msg" | Tee-Object -FilePath $log -Append }

try {
    Set-Location $repo
    Say "pull"
    git pull --rebase --quiet origin master 2>&1 | Out-File $log -Append

    Say "crawl + build"
    Set-Location $PSScriptRoot
    python -W ignore run_daily.py 2>&1 | Out-File $log -Append
    if ($LASTEXITCODE -ne 0) { throw "run_daily.py exited $LASTEXITCODE" }

    Set-Location $repo
    git add imeos/data/regintel imeos/pipeline/state 2>&1 | Out-File $log -Append
    git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { Say "no changes"; exit 0 }
    git commit --quiet -m ("RegIntel data update " + (Get-Date -Format "yyyy-MM-dd") + " (local)") 2>&1 | Out-File $log -Append
    git pull --rebase --quiet origin master 2>&1 | Out-File $log -Append
    git push --quiet origin master 2>&1 | Out-File $log -Append
    if ($LASTEXITCODE -ne 0) { throw "git push exited $LASTEXITCODE" }
    Say "pushed"
}
catch {
    Say "FAILED: $_"
    exit 1
}
