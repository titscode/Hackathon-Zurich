<#
.SYNOPSIS
    Prepare un PC Windows pour le workflow mockups (skills, MCP, Playwright).

.DESCRIPTION
    Sans argument : mode verification. N'installe rien, affiche l'etat et les
    commandes winget a taper pour ce qui manque.

    Avec -Install : installe les composants Claude Code (skills, plugins, MCP,
    Playwright). N'installe jamais de logiciel systeme via winget : ces
    commandes-la restent a lancer a la main.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1
    powershell -ExecutionPolicy Bypass -File scripts\setup-windows.ps1 -Install
#>
[CmdletBinding()]
param(
    [switch]$Install
)

$ErrorActionPreference = 'Continue'
$missing = @()
$todo = @()

function Write-Head($text) {
    Write-Host ''
    Write-Host "=== $text ===" -ForegroundColor Cyan
}

function Test-Prereq {
    param($Name, $Command, $VersionArg = '--version', $Winget)

    $exe = Get-Command $Command -ErrorAction SilentlyContinue
    if ($exe) {
        $version = (& $Command $VersionArg 2>&1 | Select-Object -First 1)
        Write-Host ("  [OK]      {0,-10} {1}" -f $Name, $version) -ForegroundColor Green
        return $true
    }
    Write-Host ("  [MANQUE]  {0}" -f $Name) -ForegroundColor Red
    $script:missing += [pscustomobject]@{ Name = $Name; Command = "winget install $Winget" }
    return $false
}

# ---------------------------------------------------------------- 1. Prerequis
Write-Head '1. Prerequis'
$hasNode   = Test-Prereq 'node'   'node'   '--version' '-e OpenJS.NodeJS.LTS'
$hasNpm    = Test-Prereq 'npm'    'npm'    '--version' '-e OpenJS.NodeJS.LTS'
$hasPython = Test-Prereq 'python' 'python' '--version' '-e Python.Python.3.12'
$hasGit    = Test-Prereq 'git'    'git'    '--version' '-e Git.Git'
$hasGh     = Test-Prereq 'gh'     'gh'     '--version' '-e GitHub.cli'
$hasClaude = Test-Prereq 'claude' 'claude' '--version' '-e Anthropic.ClaudeCode'

if ($missing.Count -gt 0) {
    Write-Host ''
    Write-Host 'A installer toi-meme (je ne lance pas winget) :' -ForegroundColor Yellow
    $missing | ForEach-Object { Write-Host ("  {0}" -f $_.Command) }
    Write-Host '  Puis rouvrir le terminal et relancer ce script.' -ForegroundColor Yellow
    if (-not $Install) { Write-Host '' ; Write-Host 'Mode verification. Relance avec -Install une fois les prerequis presents.' -ForegroundColor Yellow ; exit 1 }
}

if (-not $Install) {
    Write-Host ''
    Write-Host 'Mode verification uniquement. Relance avec -Install pour installer :' -ForegroundColor Yellow
    Write-Host '  skill ui-ux-pro-max, plugin frontend-design, MCP playwright + figma, chromium'
    exit 0
}

# ------------------------------------------------------------------- 2. Skills
Write-Head '2. Skill ui-ux-pro-max (global)'
if ($hasNode) {
    npx --yes ui-ux-pro-max-cli init --ai claude --global
    $skillPath = Join-Path $HOME '.claude\skills\ui-ux-pro-max'
    if (Test-Path $skillPath) {
        Write-Host "  [OK] $skillPath" -ForegroundColor Green
        $searchPy = Join-Path $skillPath 'scripts\search.py'
        if ((Test-Path $searchPy) -and $hasPython) {
            Write-Host '  Test de search.py :'
            python $searchPy "mobile app" --domain style 2>&1 | Select-Object -First 8
        } else {
            Write-Host "  [ATTENTION] search.py introuvable a $searchPy" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [ECHEC] $skillPath absent apres init" -ForegroundColor Red
        $todo += 'npx ui-ux-pro-max-cli init --ai claude --global   (a relancer, a echoue)'
    }
}

Write-Head '3. Plugin frontend-design'
if ($hasClaude) {
    claude plugin install frontend-design@claude-plugins-official -y
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  [ECHEC] sous-commande indisponible ou marketplace absent' -ForegroundColor Yellow
        $todo += 'Dans un terminal Claude Code, taper : /plugin install frontend-design@claude-plugins-official'
    } else {
        Write-Host '  [OK] plugin installe' -ForegroundColor Green
    }
}

# ---------------------------------------------------------------------- 4. MCP
Write-Head '4. MCP (scope user)'
if ($hasClaude) {
    claude mcp add --scope user playwright -- npx @playwright/mcp@latest
    claude mcp add --scope user --transport http figma https://mcp.figma.com/mcp
    Write-Host '  [OK] serveurs ajoutes' -ForegroundColor Green
    Write-Host '  Figma demande une authentification : taper /mcp dans Claude Code.' -ForegroundColor Yellow
    $todo += 'Dans Claude Code : /mcp puis authentifier "figma" dans le navigateur'
    claude mcp list
}

Write-Head '5. Chromium (Playwright)'
if ($hasNode)   { npx --yes playwright install chromium }
if ($hasPython) {
    python -m pip install --quiet --upgrade playwright
    python -m playwright install chromium
    Write-Host '  [OK] playwright python + chromium' -ForegroundColor Green
}

# ----------------------------------------------------------------- 6. Cle API
Write-Head '6. Cle DeepInfra'
if ($env:DEEPINFRA_API_KEY) {
    Write-Host '  [OK] DEEPINFRA_API_KEY est definie' -ForegroundColor Green
} else {
    Write-Host '  [MANQUE] DEEPINFRA_API_KEY' -ForegroundColor Yellow
    $todo += 'setx DEEPINFRA_API_KEY "ta-cle"   puis rouvrir le terminal'
}

# ------------------------------------------------------------------ 7. Rapport
Write-Head 'Reste a faire a la main'
if ($todo.Count -eq 0) {
    Write-Host '  Rien. Setup complet.' -ForegroundColor Green
} else {
    $todo | ForEach-Object { Write-Host "  - $_" }
}
Write-Host ''
Write-Host 'Test de bout en bout :' -ForegroundColor Cyan
Write-Host '  python scripts\shot.py test'
Write-Host '  (doit produire out\test.png)'
