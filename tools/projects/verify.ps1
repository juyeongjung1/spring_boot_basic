param(
    [string]$JavaHome = $env:JAVA_HOME,
    [int]$DatabasePort = 3306
)
$ErrorActionPreference = 'Stop'
if (-not $JavaHome -or -not (Test-Path -LiteralPath (Join-Path $JavaHome 'bin/javac.exe'))) {
    throw 'JDK 21の場所を -JavaHome で指定してください。'
}
$env:JAVA_HOME = (Resolve-Path -LiteralPath $JavaHome).Path
$env:Path = "$env:JAVA_HOME/bin;$env:Path"
$versionText = (& (Join-Path $env:JAVA_HOME 'bin/java.exe') --version | Out-String)
if ($LASTEXITCODE -ne 0 -or $versionText -notmatch '(?m)^(?:openjdk|java)\s+21\.') { throw 'Java 21を指定してください。' }
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../projects')).Path
Push-Location -LiteralPath $projectRoot
try {
    foreach ($group in @('spring_answer', 'spring_exercise', 'enshu_answer', 'enshu_exercise')) {
        $database = if ($group.StartsWith('enshu_')) { 'spring_exercise' } else { 'spring_sample' }
        $url = "jdbc:mysql://127.0.0.1:${DatabasePort}/${database}?serverTimezone=Asia/Tokyo"
        & './mvnw.cmd' -B -ntp -f "$group/pom.xml" "-Dspring.datasource.url=$url" verify
        if ($LASTEXITCODE -ne 0) { throw "$group の検証に失敗しました。" }
    }
}
finally { Pop-Location }
