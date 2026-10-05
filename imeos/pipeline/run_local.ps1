# Daily RegIntel update from a residential connection.
# BPK's WAF blocks GitHub-hosted runners (403), so this runs on the owner's PC via Task Scheduler
# from a dedicated clone (default D:\ketikyuk-regintel-bot) that nobody edits by hand.
# Native tools write warnings to stderr (pypdf, git), which Windows PowerShell 5.1 turns into
# terminating errors under "Stop" -- so we keep "Continue" and check exit codes instead.
$ErrorActionPreference = "Continue"
$repo = (Resolve-Path "$PSScriptRoot\..\..").Path
$logDir = Join-Path $PSScriptRoot "logs"
New-Item -ItemType Directory -Force $logDir | Out-Null
$log = Join-Path $logDir ("run_" + (Get-Date -Format "yyyy-MM-dd") + ".log")
$env:PYTHONIOENCODING = "utf8"

function Say($msg) { Add-Content -Path $log -Encoding UTF8 -Value "$(Get-Date -Format 'HH:mm:ss')  $msg" }
function Run($exe, [string[]]$argv) {
    # cmd /c keeps stderr as plain text in the log instead of PowerShell error records
    $line = "`"$exe`" " + (($argv | ForEach-Object { "`"$_`"" }) -join " ")
    cmd /c "$line >> `"$log`" 2>&1"
    return $LASTEXITCODE
}
function Fail($msg) { Say "FAILED: $msg"; exit 1 }

Set-Location $repo
Say "pull"
if ((Run "git" @("pull", "--rebase", "--quiet", "origin", "master")) -ne 0) { Fail "git pull" }

Say "crawl + build"
Set-Location $PSScriptRoot
if ((Run "python" @("-W", "ignore", "run_daily.py")) -ne 0) { Fail "run_daily.py" }

Set-Location $repo
Run "git" @("add", "imeos/data/regintel", "imeos/pipeline/state") | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Say "no changes"; exit 0 }
if ((Run "git" @("commit", "--quiet", "-m", ("RegIntel data update " + (Get-Date -Format "yyyy-MM-dd") + " (local)"))) -ne 0) { Fail "git commit" }
if ((Run "git" @("pull", "--rebase", "--quiet", "origin", "master")) -ne 0) { Fail "git pull before push" }
if ((Run "git" @("push", "--quiet", "origin", "master")) -ne 0) { Fail "git push" }
Say "pushed"
