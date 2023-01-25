# skaffold
https://skaffold.dev/docs/environment/templating/

https://skaffold.dev/docs/pipeline-stages/builders/custom/#dockerfile
## Installation
- skaffold init
- Select Dockerfile and Buildpacks
-- yaml files should be in the same directory as the project.

### Global config
skaffold config set --global collect-metrics false

### Build
skaffold  build --push=false

### Execute in debugging mode
skaffold  build -v debug

### Build, watch and deploy in Kubernetes
skaffold dev --namespace private

## Push to remote
- docker login
- skaffold  build --push=true -v debug

## Configure environment variables of the app
export APP_ENV_DEV="{ 
    \"APP_NAME\":\"private-API\", 
    \"NODE_ENV\":\"dev\", 
    \"NODE_PORT\":\"3002\",
    \"TOKEN_LIMIT\":\"7d\", <!-- Authentication token -->
    \"TOKEN_SECRET\":\"PASS\" 
}"

### Test

 - kubectl -n private port-forward service/svc-private-api 3002:3002
 - curl http://localhost:3002/healthcheck

### Destroy the resources
Ctl + C

### Review logs in cache
 cat ~/.skaffold/cache
 skaffold delete
 skaffold dev
<!-- Rebuild and deploy without cache -->
- skaffold dev --no-prune=false --cache-artifacts=false
<!-- Rebuild and deploy with port forward -->
skaffold dev --port-forward
<!-- Rebuild and deploy without watching -->
skaffold run --port-forward
<!-- Clean resources -->
skaffold delete


<!-- Option 1: environment variable -->
SET APP_VERSION=4.0.0
  tagPolicy:
    envTemplate:
      template: "{{.APP_VERSION}}"

skaffold dev --tag=4.0.1

export APP_ENV_STAGE="{ \"APP_NAME\":\"private-API\", \"NODE_ENV\":\"stage\", \"NODE_PORT\":\"3002\", \"TOKEN_LIMIT\":\"7d\", \"TOKEN_SECRET\":\"PASS\" }"