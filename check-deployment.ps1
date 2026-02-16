# Deployment Readiness Checker
# Run this before deploying to verify everything is configured correctly

Write-Host ""
Write-Host "Checking deployment readiness..." -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check 1: Docker files exist
Write-Host "Checking configuration files..." -ForegroundColor Yellow
$requiredFiles = @(
    "docker-compose.yml",
    "render.yaml",
    ".dockerignore",
    "backend/Dockerfile",
    "backend/.dockerignore",
    "frontend/Dockerfile",
    "frontend/.dockerignore",
    "nlp-service/Dockerfile",
    "nlp-service/.dockerignore",
    "rag-service/Dockerfile",
    "rag-service/.dockerignore"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 2: Environment file exists
Write-Host "`nChecking environment variables..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ✅ .env file exists" -ForegroundColor Green
    
    # Check for OpenAI API key
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "  ✅ OpenAI API key found" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  OpenAI API key not found or invalid" -ForegroundColor Yellow
        Write-Host "     Add your key to .env: OPENAI_API_KEY=sk-..." -ForegroundColor Gray
    }
} else {
    Write-Host "  ⚠️  .env file not found (you'll need to set this in your cloud platform)" -ForegroundColor Yellow
}

# Check 3: Git repository
Write-Host "`nChecking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "  ✅ Git repository initialized" -ForegroundColor Green
    
    # Check if there are uncommitted changes
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-Host "  ⚠️  You have uncommitted changes" -ForegroundColor Yellow
        Write-Host "     Run: git add ." -ForegroundColor Gray
        Write-Host "     Then: git commit -m 'Prepare for deployment'" -ForegroundColor Gray
    } else {
        Write-Host "  ✅ All changes committed" -ForegroundColor Green
    }
    
    # Check for remote
    $gitRemote = git remote -v
    if ($gitRemote -match "github.com") {
        Write-Host "  ✅ GitHub remote configured" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  No GitHub remote found" -ForegroundColor Yellow
        Write-Host "     You'll need to push to GitHub for Railway/Render deployment" -ForegroundColor Gray
    }
} else {
    Write-Host "  ❌ Not a Git repository" -ForegroundColor Red
    Write-Host "     Run: git init" -ForegroundColor Gray
    Write-Host "     Then: git add . " -ForegroundColor Gray
    Write-Host "     Then: git commit -m 'Initial commit'" -ForegroundColor Gray
    $allGood = $false
}

# Check 4: Docker is running
Write-Host "`nChecking Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>$null
    if ($dockerVersion) {
        Write-Host "  ✅ Docker installed: $dockerVersion" -ForegroundColor Green
        
        # Check if Docker daemon is running
        $dockerPs = docker ps 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✅ Docker daemon is running" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  Docker daemon not running (only needed for local testing)" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "  ⚠️  Docker not installed (only needed for local testing)" -ForegroundColor Yellow
}

# Check 5: Node.js and Python (for local development)
Write-Host "`nChecking development tools..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "  ✅ Node.js installed: $nodeVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Node.js not found (not required for Docker deployment)" -ForegroundColor Yellow
}

try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "  ✅ Python installed: $pythonVersion" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠️  Python not found (not required for Docker deployment)" -ForegroundColor Yellow
}

# Check 6: Required dependencies in package.json
Write-Host "`nChecking package configurations..." -ForegroundColor Yellow
$packageFiles = @("backend/package.json", "frontend/package.json")
foreach ($pkg in $packageFiles) {
    if (Test-Path $pkg) {
        Write-Host "  ✅ $pkg exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $pkg missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 7: Python requirements
Write-Host "`nChecking Python requirements..." -ForegroundColor Yellow
$reqFiles = @("nlp-service/requirements.txt", "rag-service/requirements.txt")
foreach ($req in $reqFiles) {
    if (Test-Path $req) {
        Write-Host "  ✅ $req exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $req missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Final summary
Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ Ready for deployment!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:: git add ." -ForegroundColor Gray
    Write-Host "     Then:
    Write-Host "  1. Commit your changes: git add .; git commit -m 'Ready for deployment'" -ForegroundColor Gray
    Write-Host "  2. Push to GitHub: git push origin main" -ForegroundColor Gray
    Write-Host "  3. Choose a platform:" -ForegroundColor Gray
    Write-Host "     - Railway (easiest): https://railway.app" -ForegroundColor Gray
    Write-Host "     - Render (free tier): https://render.com" -ForegroundColor Gray
    Write-Host "     - Fly.io (advanced): https://fly.io" -ForegroundColor Gray
    Write-Host "  4. Follow steps in DEPLOYMENT.md" -ForegroundColor Gray
} else {
    Write-Host "⚠️  Some issues found. Please fix them before deploying." -ForegroundColor Yellow
}
Write-Host ("=" * 60) -ForegroundColor Cyan

Write-Host ""
Write-Host "📚 For detailed instructions, see: DEPLOYMENT.md" -ForegroundColor Cyan
Write-Host ""
