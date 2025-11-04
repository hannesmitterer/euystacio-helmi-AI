# Deployment Instructions

Complete guide for deploying the Nexus Platform to Render, Netlify, Docker, and cloud providers.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Variables](#environment-variables)
3. [Render Deployment](#render-deployment)
4. [Netlify Deployment](#netlify-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Kubernetes Deployment](#kubernetes-deployment)
7. [Cloud Provider Deployment](#cloud-provider-deployment)
8. [Post-Deployment](#post-deployment)

---

## Prerequisites

Before deploying, ensure you have:

- [ ] Account on your chosen platform (Render, Netlify, etc.)
- [ ] PostgreSQL database (or compatible)
- [ ] Redis instance (for caching and pub/sub)
- [ ] SSL/TLS certificates (for production)
- [ ] API keys and secrets generated
- [ ] Domain name configured (optional but recommended)

---

## Environment Variables

Create a `.env` file or configure these variables in your deployment platform:

### Required Variables

```bash
# Core API Configuration
NEXUS_API_KEY=generate_strong_random_key_here
NEXUS_BASE_URL=https://your-domain.com/v1
NEXUS_WS_URL=wss://your-domain.com/v1
NODE_ENV=production

# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/nexus_db
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10
DATABASE_SSL=true

# Redis Configuration
REDIS_URL=redis://username:password@host:6379
REDIS_TLS=true

# Security & Encryption
JWT_SECRET=generate_strong_jwt_secret_min_32_chars
SESSION_SECRET=generate_strong_session_secret_min_32_chars
ENCRYPTION_KEY=generate_256_bit_encryption_key
API_KEY_SALT=generate_random_salt_for_api_keys

# OAuth 2.0 (if using)
OAUTH_CLIENT_ID=your_oauth_client_id
OAUTH_CLIENT_SECRET=your_oauth_client_secret
OAUTH_REDIRECT_URI=https://your-domain.com/oauth/callback
OAUTH_SCOPE=openid profile email
```

### Optional Variables

```bash
# Rate Limiting
RATE_LIMIT_WINDOW_MS=60000
RATE_LIMIT_MAX_TELEMETRY=1000
RATE_LIMIT_MAX_COMMANDS=100
RATE_LIMIT_MAX_TASKS=200
RATE_LIMIT_MAX_AI=500

# Feature Flags
ENABLE_WEBSOCKET=true
ENABLE_GRPC=false
ENABLE_AI_COORDINATION=true
ENABLE_TELEMETRY=true
ENABLE_EVENTS=true

# Logging & Monitoring
LOG_LEVEL=info
LOG_FORMAT=json
ENABLE_REQUEST_LOGGING=true
METRICS_PORT=9090
HEALTH_CHECK_PORT=8080
HEALTH_CHECK_PATH=/health

# External Services
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your_app_specific_password
SMTP_FROM=noreply@your-domain.com

# Webhook Configuration
WEBHOOK_SECRET=generate_webhook_secret
WEBHOOK_TIMEOUT_MS=5000
WEBHOOK_RETRY_COUNT=3

# Storage (if using file uploads)
S3_BUCKET=your-bucket-name
S3_REGION=us-west-2
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key

# APM & Error Tracking
SENTRY_DSN=https://xxx@sentry.io/yyy
NEW_RELIC_LICENSE_KEY=your_key
DATADOG_API_KEY=your_key
```

### Generating Secrets

Use these commands to generate secure secrets:

```bash
# Generate random API key
openssl rand -hex 32

# Generate JWT secret
openssl rand -base64 48

# Generate encryption key (256-bit)
openssl rand -hex 32

# Generate UUID-based secret
uuidgen | tr '[:upper:]' '[:lower:]' | tr -d '-'
```

---

## Render Deployment

### Step 1: Create New Web Service

1. Log in to [Render](https://render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `nexus-api`
   - **Environment**: `Node` (or `Python` if using Python)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Plan**: Choose based on needs (Starter: $7/mo, Standard: $25/mo)

### Step 2: Configure Environment Variables

In Render dashboard, go to **Environment** tab and add:

```
NODE_ENV=production
NEXUS_API_KEY=<generated_key>
DATABASE_URL=<your_postgres_url>
REDIS_URL=<your_redis_url>
JWT_SECRET=<generated_secret>
SESSION_SECRET=<generated_secret>
ENCRYPTION_KEY=<generated_key>
```

### Step 3: Add PostgreSQL Database

1. In Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `nexus-db`
   - **Database**: `nexus_db`
   - **User**: `nexus_user`
   - **Region**: Same as web service
   - **Plan**: Choose based on needs
3. Copy the **Internal Database URL**
4. Add to web service environment as `DATABASE_URL`

### Step 4: Add Redis Instance

1. Click **"New +"** → **"Redis"**
2. Configure:
   - **Name**: `nexus-redis`
   - **Region**: Same as web service
   - **Plan**: Choose based on needs
3. Copy the **Internal Redis URL**
4. Add to web service environment as `REDIS_URL`

### Step 5: Configure Custom Domain (Optional)

1. In web service settings, go to **"Settings"** → **"Custom Domain"**
2. Add your domain: `api.your-domain.com`
3. Configure DNS:
   - Type: `CNAME`
   - Name: `api`
   - Value: `<your-app>.onrender.com`
4. Wait for SSL certificate provisioning

### Step 6: Deploy

1. Click **"Manual Deploy"** → **"Deploy latest commit"**
2. Monitor logs in **"Logs"** tab
3. Verify deployment at `https://<your-app>.onrender.com/health`

### Render.yaml Configuration

Create `render.yaml` for infrastructure-as-code:

```yaml
services:
  - type: web
    name: nexus-api
    env: node
    region: oregon
    plan: starter
    buildCommand: npm install && npm run build
    startCommand: npm start
    healthCheckPath: /health
    envVars:
      - key: NODE_ENV
        value: production
      - key: NEXUS_API_KEY
        generateValue: true
      - key: DATABASE_URL
        fromDatabase:
          name: nexus-db
          property: connectionString
      - key: REDIS_URL
        fromRedis:
          name: nexus-redis
          property: connectionString
    autoDeploy: true

databases:
  - name: nexus-db
    databaseName: nexus_db
    user: nexus_user
    plan: starter

redis:
  - name: nexus-redis
    plan: starter
    maxmemoryPolicy: allkeys-lru
```

---

## Netlify Deployment

**Note**: Netlify is primarily for static sites. For the Nexus API backend, use Netlify Functions (serverless) or deploy the frontend only.

### Frontend Deployment (Static Dashboard)

1. Log in to [Netlify](https://netlify.com)
2. Click **"Add new site"** → **"Import an existing project"**
3. Connect GitHub repository
4. Configure:
   - **Build command**: `npm run build:frontend`
   - **Publish directory**: `dist` or `build`
   - **Branch**: `main`

### Netlify Functions (Serverless API)

For serverless API deployment:

1. Create `netlify/functions/` directory
2. Create function files:

```javascript
// netlify/functions/telemetry.js
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  const data = JSON.parse(event.body);
  // Process telemetry data
  
  return {
    statusCode: 201,
    body: JSON.stringify({ success: true })
  };
};
```

3. Configure `netlify.toml`:

```toml
[build]
  command = "npm run build"
  publish = "dist"
  functions = "netlify/functions"

[build.environment]
  NODE_VERSION = "18"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[functions]
  node_bundler = "esbuild"

[context.production.environment]
  NODE_ENV = "production"
```

4. Add environment variables in Netlify dashboard:
   - Go to **Site settings** → **Environment variables**
   - Add required variables

### Deploy

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login
netlify login

# Deploy
netlify deploy --prod
```

---

## Docker Deployment

### Dockerfile

Create `Dockerfile`:

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine

WORKDIR /app

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./

# Create non-root user
RUN addgroup -g 1001 -S nexus && \
    adduser -S nexus -u 1001

USER nexus

# Expose ports
EXPOSE 3000 9090 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:8080/health', (r) => process.exit(r.statusCode === 200 ? 0 : 1))"

CMD ["node", "dist/index.js"]
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: nexus-api
    ports:
      - "3000:3000"
      - "9090:9090"
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://nexus:password@postgres:5432/nexus_db
      - REDIS_URL=redis://redis:6379
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    restart: unless-stopped
    networks:
      - nexus-network

  postgres:
    image: postgres:15-alpine
    container_name: nexus-postgres
    environment:
      - POSTGRES_DB=nexus_db
      - POSTGRES_USER=nexus
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped
    networks:
      - nexus-network

  redis:
    image: redis:7-alpine
    container_name: nexus-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped
    networks:
      - nexus-network

  nginx:
    image: nginx:alpine
    container_name: nexus-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped
    networks:
      - nexus-network

volumes:
  postgres-data:
  redis-data:

networks:
  nexus-network:
    driver: bridge
```

### Build and Run

```bash
# Build image
docker build -t nexus-api:latest .

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Kubernetes Deployment

### Create Kubernetes Manifests

**deployment.yaml:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nexus-api
  namespace: nexus
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nexus-api
  template:
    metadata:
      labels:
        app: nexus-api
    spec:
      containers:
      - name: api
        image: your-registry/nexus-api:latest
        ports:
        - containerPort: 3000
          name: http
        - containerPort: 9090
          name: metrics
        - containerPort: 8080
          name: health
        env:
        - name: NODE_ENV
          value: "production"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: redis-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: nexus-secrets
              key: jwt-secret
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**service.yaml:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: nexus-api
  namespace: nexus
spec:
  selector:
    app: nexus-api
  ports:
  - name: http
    port: 80
    targetPort: 3000
  - name: metrics
    port: 9090
    targetPort: 9090
  type: LoadBalancer
```

**secrets.yaml:**

```bash
# Create secrets from environment variables
kubectl create secret generic nexus-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=redis-url=$REDIS_URL \
  --from-literal=jwt-secret=$JWT_SECRET \
  --from-literal=session-secret=$SESSION_SECRET \
  --from-literal=encryption-key=$ENCRYPTION_KEY \
  --namespace=nexus
```

### Deploy to Kubernetes

```bash
# Create namespace
kubectl create namespace nexus

# Apply manifests
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Check status
kubectl get pods -n nexus
kubectl get services -n nexus

# View logs
kubectl logs -f deployment/nexus-api -n nexus

# Scale deployment
kubectl scale deployment nexus-api --replicas=5 -n nexus
```

---

## Cloud Provider Deployment

### AWS (Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p node.js-18 nexus-api

# Create environment
eb create nexus-production

# Deploy
eb deploy

# Set environment variables
eb setenv NODE_ENV=production DATABASE_URL=$DATABASE_URL REDIS_URL=$REDIS_URL
```

### Google Cloud Platform (Cloud Run)

```bash
# Build and push image
gcloud builds submit --tag gcr.io/PROJECT-ID/nexus-api

# Deploy
gcloud run deploy nexus-api \
  --image gcr.io/PROJECT-ID/nexus-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars NODE_ENV=production,DATABASE_URL=$DATABASE_URL
```

### Azure (App Service)

```bash
# Create resource group
az group create --name nexus-rg --location eastus

# Create App Service plan
az appservice plan create --name nexus-plan --resource-group nexus-rg --sku B1 --is-linux

# Create web app
az webapp create --resource-group nexus-rg --plan nexus-plan --name nexus-api --runtime "NODE|18-lts"

# Configure environment variables
az webapp config appsettings set --resource-group nexus-rg --name nexus-api --settings NODE_ENV=production DATABASE_URL=$DATABASE_URL

# Deploy
az webapp deployment source config-zip --resource-group nexus-rg --name nexus-api --src deploy.zip
```

---

## Post-Deployment

### 1. Verify Deployment

```bash
# Check health endpoint
curl https://your-domain.com/health

# Test API
curl -X POST https://your-domain.com/v1/telemetry/frames \
  -H "Authorization: Bearer $NEXUS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test","metrics":{"test":1}}'
```

### 2. Configure Monitoring

- Set up application monitoring (New Relic, Datadog, etc.)
- Configure log aggregation (CloudWatch, Stackdriver, etc.)
- Set up error tracking (Sentry, Rollbar, etc.)
- Enable performance monitoring

### 3. Set Up Alerts

- API response time > 500ms
- Error rate > 1%
- Database connection failures
- Memory/CPU usage > 80%
- Rate limit violations

### 4. Configure Backups

- Database: Automated daily backups
- Redis: Persistence enabled (AOF or RDB)
- Configuration: Version controlled in Git

### 5. Security Checklist

- [ ] SSL/TLS certificates configured
- [ ] Environment variables secured
- [ ] API keys rotated regularly
- [ ] Rate limiting enabled
- [ ] CORS configured properly
- [ ] Security headers enabled
- [ ] Database access restricted
- [ ] Firewall rules configured

### 6. Performance Optimization

- Enable caching (Redis)
- Configure CDN for static assets
- Enable compression (gzip/brotli)
- Optimize database queries
- Set up connection pooling

---

## Troubleshooting

### Common Issues

**Database Connection Failed:**
```bash
# Check DATABASE_URL format
# PostgreSQL: postgresql://user:password@host:port/database
# Ensure SSL is configured if required
```

**WebSocket Connection Refused:**
```bash
# Ensure WebSocket support is enabled on load balancer
# Check firewall rules allow WebSocket upgrade
# Verify WS_URL uses wss:// protocol
```

**High Memory Usage:**
```bash
# Adjust Node.js memory limit
NODE_OPTIONS="--max-old-space-size=4096"

# Monitor memory leaks
node --inspect dist/index.js
```

**Rate Limiting Too Aggressive:**
```bash
# Adjust limits in environment variables
RATE_LIMIT_MAX_TELEMETRY=2000
RATE_LIMIT_WINDOW_MS=60000
```

---

## Support

For deployment assistance:

- **Documentation**: https://docs.nexus.example.com/deployment
- **Email**: support@nexus.example.com
- **Slack**: #nexus-deployment

---

**Last Updated**: 2025-11-03
