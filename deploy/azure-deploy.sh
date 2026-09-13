#!/usr/bin/env bash
set -euo pipefail

# ╔════════════════════════════════════════════════════════════════════╗
# ║  STUMP Platform — Azure Deployment Script                        ║
# ║  Deploys: Backend (App Service) + Frontend (App Service) + PG DB ║
# ╚════════════════════════════════════════════════════════════════════╝

export PATH="$HOME/Library/Python/3.13/bin:$PATH"

# ── Configuration ─────────────────────────────────────────────────────
RESOURCE_GROUP="rg-stump-platform"
LOCATION="eastus"
APP_SERVICE_PLAN="asp-stump-platform"
BACKEND_APP="stump-api"
FRONTEND_APP="stump-app"
PG_SERVER="stump-platform-db"
PG_DB="stump_db"
PG_ADMIN="stumpadmin"
PG_PASSWORD=""
ACR_NAME="stumpplatformacr"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
info() { echo -e "${CYAN}[→]${NC} $1"; }
warn() { echo -e "${YELLOW}[!]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; exit 1; }

# ── Pre-flight checks ────────────────────────────────────────────────
command -v az >/dev/null 2>&1 || err "Azure CLI not installed. Run: brew install azure-cli"

info "Checking Azure login..."
az account show >/dev/null 2>&1 || {
    warn "Not logged in. Opening browser for Azure login..."
    az login
}

SUBSCRIPTION=$(az account show --query name -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
log "Logged in to: $SUBSCRIPTION ($SUBSCRIPTION_ID)"

# ── Generate DB password if not set ───────────────────────────────────
if [ -z "$PG_PASSWORD" ]; then
    PG_PASSWORD="Stump$(openssl rand -hex 8)!"
    warn "Generated DB password (save this): $PG_PASSWORD"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Deployment Plan                                         ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Resource Group:    $RESOURCE_GROUP"
echo "║  Location:          $LOCATION"
echo "║  Backend App:       $BACKEND_APP.azurewebsites.net"
echo "║  Frontend App:      $FRONTEND_APP.azurewebsites.net"
echo "║  PostgreSQL Server:  $PG_SERVER.postgres.database.azure.com"
echo "║  Database:           $PG_DB"
echo "║  Container Registry: $ACR_NAME.azurecr.io"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
read -p "Proceed with deployment? (y/N) " -n 1 -r
echo
[[ $REPLY =~ ^[Yy]$ ]] || { echo "Cancelled."; exit 0; }

# ═════════════════════════════════════════════════════════════════════
# STEP 1: Create Resource Group
# ═════════════════════════════════════════════════════════════════════
info "Creating resource group: $RESOURCE_GROUP..."
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" -o none
log "Resource group created."

# ═════════════════════════════════════════════════════════════════════
# STEP 2: Create Azure Container Registry
# ═════════════════════════════════════════════════════════════════════
info "Creating container registry: $ACR_NAME..."
az acr create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$ACR_NAME" \
    --sku Basic \
    --admin-enabled true \
    -o none
log "Container registry created."

ACR_SERVER="$ACR_NAME.azurecr.io"
ACR_USER=$(az acr credential show --name "$ACR_NAME" --query username -o tsv)
ACR_PASS=$(az acr credential show --name "$ACR_NAME" --query "passwords[0].value" -o tsv)

# ═════════════════════════════════════════════════════════════════════
# STEP 3: Create PostgreSQL Flexible Server
# ═════════════════════════════════════════════════════════════════════
info "Creating PostgreSQL Flexible Server: $PG_SERVER..."
az postgres flexible-server create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$PG_SERVER" \
    --location "$LOCATION" \
    --admin-user "$PG_ADMIN" \
    --admin-password "$PG_PASSWORD" \
    --sku-name "Standard_B1ms" \
    --tier "Burstable" \
    --storage-size 32 \
    --version 16 \
    --yes \
    -o none
log "PostgreSQL server created."

info "Configuring firewall: allow Azure services..."
az postgres flexible-server firewall-rule create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$PG_SERVER" \
    --rule-name "AllowAzureServices" \
    --start-ip-address "0.0.0.0" \
    --end-ip-address "0.0.0.0" \
    -o none

# Allow current IP for seeding
MY_IP=$(curl -s https://api.ipify.org)
az postgres flexible-server firewall-rule create \
    --resource-group "$RESOURCE_GROUP" \
    --name "$PG_SERVER" \
    --rule-name "AllowDeployMachine" \
    --start-ip-address "$MY_IP" \
    --end-ip-address "$MY_IP" \
    -o none

info "Creating database: $PG_DB..."
az postgres flexible-server db create \
    --resource-group "$RESOURCE_GROUP" \
    --server-name "$PG_SERVER" \
    --database-name "$PG_DB" \
    -o none
log "Database created."

# Build the connection strings
PG_HOST="$PG_SERVER.postgres.database.azure.com"
DATABASE_URL="postgresql+asyncpg://${PG_ADMIN}:${PG_PASSWORD}@${PG_HOST}:5432/${PG_DB}?ssl=require"
log "Database URL configured."

# ═════════════════════════════════════════════════════════════════════
# STEP 4: Build & Push Backend Docker Image
# ═════════════════════════════════════════════════════════════════════
info "Building backend Docker image..."
cd "$(dirname "$0")/.."

az acr build \
    --registry "$ACR_NAME" \
    --image stump-backend:latest \
    --file Dockerfile.backend \
    . \
    --no-logs
log "Backend image pushed to $ACR_SERVER/stump-backend:latest"

# ═════════════════════════════════════════════════════════════════════
# STEP 5: Create App Service Plan + Backend App
# ═════════════════════════════════════════════════════════════════════
info "Creating App Service Plan: $APP_SERVICE_PLAN (B1 Linux)..."
az appservice plan create \
    --name "$APP_SERVICE_PLAN" \
    --resource-group "$RESOURCE_GROUP" \
    --sku B1 \
    --is-linux \
    -o none

info "Creating backend App Service: $BACKEND_APP..."
az webapp create \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$APP_SERVICE_PLAN" \
    --name "$BACKEND_APP" \
    --docker-registry-server-url "https://$ACR_SERVER" \
    --docker-registry-server-user "$ACR_USER" \
    --docker-registry-server-password "$ACR_PASS" \
    --deployment-container-image-name "$ACR_SERVER/stump-backend:latest" \
    -o none

info "Configuring backend environment..."
az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$BACKEND_APP" \
    --settings \
        DATABASE_URL="$DATABASE_URL" \
        AZURE_OPENAI_API_KEY="B4bAodtFGuc8mZrAL6byEmlDAHFAAMgPxanfzK75BCK9kXngdX2MJQQJ99BLACHYHv6XJ3w3AAABACOGXx4F" \
        AZURE_OPENAI_ENDPOINT="https://techmod-azureopenai.openai.azure.com/" \
        AZURE_OPENAI_DEPLOYMENT="gpt-4o" \
        AZURE_OPENAI_API_VERSION="2024-02-15-preview" \
        WEBSITES_PORT="8000" \
        SCM_DO_BUILD_DURING_DEPLOYMENT="false" \
    -o none

az webapp config set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$BACKEND_APP" \
    --always-on true \
    -o none

BACKEND_URL="https://$BACKEND_APP.azurewebsites.net"
log "Backend deployed: $BACKEND_URL"

# ═════════════════════════════════════════════════════════════════════
# STEP 6: Build & Push Frontend Docker Image
# ═════════════════════════════════════════════════════════════════════
info "Building frontend Docker image..."
az acr build \
    --registry "$ACR_NAME" \
    --image stump-frontend:latest \
    --file Dockerfile.frontend \
    --build-arg "VITE_API_URL=" \
    . \
    --no-logs
log "Frontend image pushed to $ACR_SERVER/stump-frontend:latest"

# ═════════════════════════════════════════════════════════════════════
# STEP 7: Create Frontend App Service
# ═════════════════════════════════════════════════════════════════════
info "Creating frontend App Service: $FRONTEND_APP..."
az webapp create \
    --resource-group "$RESOURCE_GROUP" \
    --plan "$APP_SERVICE_PLAN" \
    --name "$FRONTEND_APP" \
    --docker-registry-server-url "https://$ACR_SERVER" \
    --docker-registry-server-user "$ACR_USER" \
    --docker-registry-server-password "$ACR_PASS" \
    --deployment-container-image-name "$ACR_SERVER/stump-frontend:latest" \
    -o none

az webapp config appsettings set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP" \
    --settings \
        BACKEND_URL="$BACKEND_URL" \
        WEBSITES_PORT="80" \
    -o none

az webapp config set \
    --resource-group "$RESOURCE_GROUP" \
    --name "$FRONTEND_APP" \
    --always-on true \
    -o none

FRONTEND_URL="https://$FRONTEND_APP.azurewebsites.net"
log "Frontend deployed: $FRONTEND_URL"

# ═════════════════════════════════════════════════════════════════════
# STEP 8: Update Backend CORS
# ═════════════════════════════════════════════════════════════════════
info "Updating backend CORS for frontend URL..."
az webapp cors add \
    --resource-group "$RESOURCE_GROUP" \
    --name "$BACKEND_APP" \
    --allowed-origins "$FRONTEND_URL" \
    -o none
log "CORS configured."

# ═════════════════════════════════════════════════════════════════════
# STEP 9: Seed Database
# ═════════════════════════════════════════════════════════════════════
info "Seeding database with demo data..."
cd "$(dirname "$0")/.."
python deploy/seed_azure_db.py "$DATABASE_URL"
log "Database seeded."

# ═════════════════════════════════════════════════════════════════════
# STEP 10: Verify Deployment
# ═════════════════════════════════════════════════════════════════════
info "Waiting for services to start (30s)..."
sleep 30

info "Verifying backend health..."
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" "$BACKEND_URL/api/v1/health" 2>/dev/null || echo "000")
if [ "$HEALTH" = "200" ]; then
    log "Backend is healthy!"
else
    warn "Backend returned HTTP $HEALTH — it may still be starting up. Check logs: az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP"
fi

info "Verifying frontend..."
FRONT=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" 2>/dev/null || echo "000")
if [ "$FRONT" = "200" ]; then
    log "Frontend is live!"
else
    warn "Frontend returned HTTP $FRONT — it may still be starting up."
fi

# ═════════════════════════════════════════════════════════════════════
# DONE
# ═════════════════════════════════════════════════════════════════════
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║  🎉 STUMP Platform Deployed Successfully!                   ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Frontend:  $FRONTEND_URL"
echo "║  Backend:   $BACKEND_URL"
echo "║  API Docs:  $BACKEND_URL/docs"
echo "║                                                              ║"
echo "║  Database:  $PG_HOST"
echo "║  DB Name:   $PG_DB"
echo "║  DB Admin:  $PG_ADMIN"
echo "║  DB Pass:   $PG_PASSWORD"
echo "║                                                              ║"
echo "║  Resource Group: $RESOURCE_GROUP"
echo "║  Azure Portal:   https://portal.azure.com/#browse/Microsoft.Web%2Fsites"
echo "║                                                              ║"
echo "║  To view logs:                                               ║"
echo "║    az webapp log tail --name $BACKEND_APP --resource-group $RESOURCE_GROUP"
echo "║    az webapp log tail --name $FRONTEND_APP --resource-group $RESOURCE_GROUP"
echo "║                                                              ║"
echo "║  To tear down:                                               ║"
echo "║    az group delete --name $RESOURCE_GROUP --yes              ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Save deployment info
cat > deploy/.deploy-info.json <<EOF
{
  "frontend_url": "$FRONTEND_URL",
  "backend_url": "$BACKEND_URL",
  "database_host": "$PG_HOST",
  "database_name": "$PG_DB",
  "database_admin": "$PG_ADMIN",
  "database_password": "$PG_PASSWORD",
  "resource_group": "$RESOURCE_GROUP",
  "acr_name": "$ACR_NAME",
  "subscription": "$SUBSCRIPTION",
  "deployed_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
log "Deployment info saved to deploy/.deploy-info.json"
