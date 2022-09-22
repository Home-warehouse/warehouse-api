param([string]$HW_VERSION, [string]$API_HOST)

if( $HW_VERSION_UI.Length -eq 0 ) {
    $HW_VERSION_UI = $HW_VERSION
}

git clone https://github.com/Home-warehouse/warehouse-api.git --depth 1 --branch $HW_VERSION home-warehouse-api
git clone https://github.com/Home-warehouse/warehouse-ui.git --depth 1 --branch $HW_VERSION_UI home-warehouse-ui

# Variables
$JWT_SECRET = Get-Random
$EVERNOTE_INTEGRATED = "true" 


# Update API .env
"PYTHONPATH=./home_warehouse_api
DEBUG=False
TEST=False
MOUNT_APP=True
DB_URL=mongodb://mongo-home-warehouse:27017/home-warehouse
API_HOST=0.0.0.0
API_PORT=8000
API_ORIGINS=['*']
API_JWT_SECRET=$JWT_SECRET" | Out-File -Encoding utf8 -FilePath .\home-warehouse-api\.env

if( $EVERNOTE_TOKEN.Length -gt 0 ) {
    Add-Content -Path .\home-warehouse-api\.env -Value (INTEGRATION_EVERNOTE_TOKEN=$EVERNOTE_TOKEN)
}else {
    $EVERNOTE_INTEGRATED='false'
}


# Update UI .env
"export const environment = {
    production: true,
    apiIP: 'api/',
    intergrations: [
        {
            name: 'EVERNOTE',
            integrated: ${EVERNOTE_INTEGRATED}
        }
    ]
 };" | Out-File -Encoding utf8 -FilePath .\home-warehouse-ui\src\environments\environment.prod.ts

cd home-warehouse-api/docker
docker-compose -f docker-compose.yml up -d --build