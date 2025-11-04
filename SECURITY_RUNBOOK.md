# Security Runbook

Comprehensive security guide and checklist for the Nexus Platform covering authentication, authorization, secret management, session handling, rate limiting, and incident response.

## Table of Contents

1. [Security Checklist](#security-checklist)
2. [Authentication & Authorization](#authentication--authorization)
3. [Secret Management](#secret-management)
4. [Session Management](#session-management)
5. [Rate Limiting & DDoS Protection](#rate-limiting--ddos-protection)
6. [Data Protection](#data-protection)
7. [API Security](#api-security)
8. [Vulnerability Management](#vulnerability-management)
9. [Incident Response](#incident-response)
10. [Compliance](#compliance)

---

## Security Checklist

### Pre-Deployment Checklist

- [ ] All secrets stored in environment variables or secret manager
- [ ] No credentials committed to version control
- [ ] SSL/TLS certificates configured and valid
- [ ] HTTPS enforced for all endpoints
- [ ] API keys use cryptographically secure random generation
- [ ] JWT secrets are strong (min 32 bytes)
- [ ] Database connections use SSL
- [ ] Rate limiting enabled on all endpoints
- [ ] CORS configured with specific origins
- [ ] Security headers enabled
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection enabled
- [ ] Session timeout configured
- [ ] Password hashing uses bcrypt/argon2
- [ ] API versioning implemented
- [ ] Error messages don't leak sensitive info
- [ ] Logging excludes sensitive data
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security headers tested

### Runtime Security Checklist

- [ ] Monitor failed authentication attempts
- [ ] Alert on rate limit violations
- [ ] Review access logs daily
- [ ] Rotate API keys quarterly
- [ ] Rotate JWT secrets monthly
- [ ] Update dependencies monthly
- [ ] Review user permissions monthly
- [ ] Test backup restoration quarterly
- [ ] Conduct security audits annually
- [ ] Review and update this runbook quarterly

---

## Authentication & Authorization

### API Key Authentication

#### Generation

```javascript
const crypto = require('crypto');

function generateAPIKey() {
  // Generate 32 bytes of random data
  const key = crypto.randomBytes(32).toString('hex');
  
  // Prefix for identification
  return `nxs_${key}`;
}

// Example: nxs_a1b2c3d4e5f6...
```

#### Storage

**Never store plain text API keys**. Always hash before storage:

```javascript
const bcrypt = require('bcrypt');

async function hashAPIKey(apiKey) {
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(apiKey, salt);
  return hash;
}

async function verifyAPIKey(apiKey, hash) {
  return await bcrypt.compare(apiKey, hash);
}
```

#### Validation

```javascript
const jwt = require('jsonwebtoken');

function validateAPIKey(req, res, next) {
  const authHeader = req.headers['authorization'];
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Missing or invalid authorization header'
      }
    });
  }
  
  const apiKey = authHeader.replace('Bearer ', '');
  
  // Validate format
  if (!apiKey.startsWith('nxs_') || apiKey.length !== 68) {
    return res.status(401).json({
      error: {
        code: 'INVALID_API_KEY',
        message: 'Invalid API key format'
      }
    });
  }
  
  // Verify against database
  const user = await verifyAPIKeyInDatabase(apiKey);
  
  if (!user) {
    return res.status(401).json({
      error: {
        code: 'INVALID_API_KEY',
        message: 'API key not found or inactive'
      }
    });
  }
  
  // Attach user to request
  req.user = user;
  next();
}
```

### OAuth 2.0 / JWT

#### Token Generation

```javascript
const jwt = require('jsonwebtoken');

function generateJWT(user) {
  const payload = {
    user_id: user.id,
    email: user.email,
    roles: user.roles,
    scopes: user.scopes
  };
  
  const token = jwt.sign(payload, process.env.JWT_SECRET, {
    algorithm: 'HS256',
    expiresIn: '1h',
    issuer: 'nexus-api',
    audience: 'nexus-clients'
  });
  
  return token;
}

function generateRefreshToken(user) {
  const payload = {
    user_id: user.id,
    type: 'refresh'
  };
  
  return jwt.sign(payload, process.env.JWT_REFRESH_SECRET, {
    algorithm: 'HS256',
    expiresIn: '7d'
  });
}
```

#### Token Validation

```javascript
function validateJWT(req, res, next) {
  const authHeader = req.headers['authorization'];
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: {
        code: 'UNAUTHORIZED',
        message: 'Missing authorization header'
      }
    });
  }
  
  const token = authHeader.replace('Bearer ', '');
  
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'nexus-api',
      audience: 'nexus-clients'
    });
    
    req.user = decoded;
    next();
  } catch (error) {
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({
        error: {
          code: 'TOKEN_EXPIRED',
          message: 'JWT token has expired'
        }
      });
    }
    
    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid JWT token'
      }
    });
  }
}
```

### Role-Based Access Control (RBAC)

```javascript
const permissions = {
  admin: ['*'],
  operator: [
    'telemetry:read',
    'telemetry:write',
    'command:execute',
    'task:read',
    'task:write'
  ],
  viewer: [
    'telemetry:read',
    'task:read'
  ]
};

function checkPermission(requiredPermission) {
  return (req, res, next) => {
    const userRoles = req.user.roles || [];
    const userPermissions = new Set();
    
    // Collect all permissions from user roles
    userRoles.forEach(role => {
      const rolePerms = permissions[role] || [];
      rolePerms.forEach(perm => userPermissions.add(perm));
    });
    
    // Check if user has required permission
    if (userPermissions.has('*') || userPermissions.has(requiredPermission)) {
      next();
    } else {
      res.status(403).json({
        error: {
          code: 'FORBIDDEN',
          message: `Missing required permission: ${requiredPermission}`
        }
      });
    }
  };
}

// Usage
app.post('/telemetry/frames', 
  validateJWT,
  checkPermission('telemetry:write'),
  handleTelemetryFrame
);
```

---

## Secret Management

### Environment Variables

**Never commit secrets to version control**

`.gitignore`:
```
.env
.env.local
.env.*.local
secrets/
credentials.json
*.pem
*.key
```

### Secret Rotation

#### API Key Rotation

```javascript
async function rotateAPIKey(userId) {
  // Generate new key
  const newKey = generateAPIKey();
  const newHash = await hashAPIKey(newKey);
  
  // Store with grace period
  await db.apiKeys.create({
    user_id: userId,
    key_hash: newHash,
    created_at: new Date(),
    expires_at: new Date(Date.now() + 90 * 24 * 60 * 60 * 1000), // 90 days
    status: 'active'
  });
  
  // Mark old key for deprecation
  await db.apiKeys.update({
    where: { user_id: userId, status: 'active' },
    data: {
      status: 'deprecated',
      deprecation_date: new Date(),
      expires_at: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 day grace period
    }
  });
  
  return newKey;
}
```

#### JWT Secret Rotation

```javascript
// Use multiple secrets during rotation
const jwtSecrets = [
  process.env.JWT_SECRET_CURRENT,
  process.env.JWT_SECRET_PREVIOUS
];

function verifyJWTWithRotation(token) {
  for (const secret of jwtSecrets) {
    try {
      return jwt.verify(token, secret);
    } catch (error) {
      continue;
    }
  }
  
  throw new Error('Invalid token');
}
```

### Encryption at Rest

```javascript
const crypto = require('crypto');

const ALGORITHM = 'aes-256-gcm';
const KEY = Buffer.from(process.env.ENCRYPTION_KEY, 'hex');

function encrypt(plaintext) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, KEY, iv);
  
  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    iv: iv.toString('hex'),
    encrypted,
    authTag: authTag.toString('hex')
  };
}

function decrypt(encryptedData) {
  const decipher = crypto.createDecipheriv(
    ALGORITHM,
    KEY,
    Buffer.from(encryptedData.iv, 'hex')
  );
  
  decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
  
  let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

// Store encrypted data
async function storeSecret(key, value) {
  const encrypted = encrypt(value);
  
  await db.secrets.create({
    key,
    iv: encrypted.iv,
    encrypted: encrypted.encrypted,
    auth_tag: encrypted.authTag
  });
}

// Retrieve and decrypt
async function getSecret(key) {
  const secret = await db.secrets.findUnique({ where: { key } });
  
  if (!secret) return null;
  
  return decrypt({
    iv: secret.iv,
    encrypted: secret.encrypted,
    authTag: secret.auth_tag
  });
}
```

---

## Session Management

### Session Configuration

```javascript
const session = require('express-session');
const RedisStore = require('connect-redis')(session);
const redis = require('redis');

const redisClient = redis.createClient({
  url: process.env.REDIS_URL,
  tls: process.env.NODE_ENV === 'production' ? {} : undefined
});

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: process.env.SESSION_SECRET,
  name: 'nexus.sid',
  resave: false,
  saveUninitialized: false,
  cookie: {
    secure: process.env.NODE_ENV === 'production', // HTTPS only
    httpOnly: true, // Prevent XSS
    sameSite: 'strict', // CSRF protection
    maxAge: 3600000, // 1 hour
    domain: process.env.COOKIE_DOMAIN
  },
  rolling: true // Reset expiration on activity
}));
```

### Session Cleanup

```javascript
// Automatic cleanup job
const cron = require('node-cron');

// Run every 15 minutes
cron.schedule('*/15 * * * *', async () => {
  console.log('Running session cleanup...');
  
  const now = Date.now();
  const expiredSessions = await redis.keys('sess:*');
  
  let cleanedCount = 0;
  
  for (const key of expiredSessions) {
    const session = await redis.get(key);
    
    if (session) {
      const data = JSON.parse(session);
      const expiresAt = data.cookie?.expires || data.cookie?.maxAge + data.cookie?._createdAt;
      
      if (expiresAt && new Date(expiresAt) < now) {
        await redis.del(key);
        cleanedCount++;
      }
    }
  }
  
  console.log(`Cleaned ${cleanedCount} expired sessions`);
});
```

### Force Logout

```javascript
async function forceLogout(userId) {
  // Invalidate all sessions for user
  const sessions = await redis.keys('sess:*');
  
  for (const key of sessions) {
    const session = await redis.get(key);
    
    if (session) {
      const data = JSON.parse(session);
      
      if (data.user_id === userId) {
        await redis.del(key);
        console.log(`Invalidated session for user ${userId}`);
      }
    }
  }
  
  // Revoke all JWT refresh tokens
  await db.refreshTokens.deleteMany({
    where: { user_id: userId }
  });
}
```

---

## Rate Limiting & DDoS Protection

### Implementation

```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const redisClient = redis.createClient({
  url: process.env.REDIS_URL
});

// General API rate limit
const apiLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:api:'
  }),
  windowMs: 60 * 1000, // 1 minute
  max: 100, // 100 requests per minute
  message: {
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later'
    }
  },
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests',
        retry_after: req.rateLimit.resetTime
      }
    });
  }
});

// Telemetry endpoint (higher limit)
const telemetryLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:telemetry:'
  }),
  windowMs: 60 * 1000,
  max: 1000,
  keyGenerator: (req) => req.user.id || req.ip
});

// Auth endpoint (stricter limit)
const authLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:'
  }),
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 attempts per 15 minutes
  skipSuccessfulRequests: true
});

// Apply to routes
app.use('/v1/', apiLimiter);
app.post('/v1/telemetry/frames', telemetryLimiter, handleTelemetry);
app.post('/v1/auth/login', authLimiter, handleLogin);
```

### IP Blocking

```javascript
const blockedIPs = new Set();

async function checkIPBlock(req, res, next) {
  const ip = req.ip || req.connection.remoteAddress;
  
  if (blockedIPs.has(ip)) {
    return res.status(403).json({
      error: {
        code: 'IP_BLOCKED',
        message: 'Your IP address has been blocked'
      }
    });
  }
  
  next();
}

async function blockIP(ip, reason, duration = 3600000) {
  blockedIPs.add(ip);
  
  await db.blockedIPs.create({
    ip,
    reason,
    blocked_at: new Date(),
    expires_at: new Date(Date.now() + duration)
  });
  
  // Auto-unblock after duration
  setTimeout(() => {
    blockedIPs.delete(ip);
  }, duration);
}

// Detect and block suspicious activity
async function detectSuspiciousActivity(req) {
  const ip = req.ip;
  const userId = req.user?.id;
  
  // Check failed auth attempts
  const failedAttempts = await redis.get(`failed_auth:${ip}`);
  
  if (failedAttempts >= 10) {
    await blockIP(ip, 'Too many failed authentication attempts', 3600000);
    return true;
  }
  
  return false;
}
```

---

## Data Protection

### Input Validation

```javascript
const Joi = require('joi');

const telemetrySchema = Joi.object({
  device_id: Joi.string().alphanum().max(50).required(),
  timestamp: Joi.date().iso().required(),
  metrics: Joi.object().pattern(
    Joi.string(),
    Joi.alternatives(Joi.number(), Joi.string(), Joi.boolean())
  ).required(),
  tags: Joi.object().pattern(
    Joi.string(),
    Joi.string().max(100)
  ),
  metadata: Joi.object()
});

function validateInput(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true
    });
    
    if (error) {
      return res.status(400).json({
        error: {
          code: 'VALIDATION_ERROR',
          message: 'Invalid request data',
          details: error.details.map(d => ({
            field: d.path.join('.'),
            message: d.message
          }))
        }
      });
    }
    
    req.body = value;
    next();
  };
}

app.post('/v1/telemetry/frames',
  validateJWT,
  validateInput(telemetrySchema),
  handleTelemetry
);
```

### SQL Injection Prevention

```javascript
// Use parameterized queries
async function getUserByEmail(email) {
  // SAFE - uses parameterized query
  return await db.query(
    'SELECT * FROM users WHERE email = $1',
    [email]
  );
  
  // UNSAFE - vulnerable to SQL injection
  // return await db.query(`SELECT * FROM users WHERE email = '${email}'`);
}

// Use ORM with prepared statements
const user = await db.users.findUnique({
  where: { email }
});
```

### XSS Prevention

```javascript
const validator = require('validator');

function sanitizeInput(input) {
  if (typeof input === 'string') {
    return validator.escape(input);
  }
  
  if (typeof input === 'object') {
    const sanitized = {};
    for (const [key, value] of Object.entries(input)) {
      sanitized[key] = sanitizeInput(value);
    }
    return sanitized;
  }
  
  return input;
}

// Output encoding in templates
// Use templating engines with auto-escaping
// Or manually encode
const encoded = validator.escape(userInput);
```

---

## API Security

### Security Headers

```javascript
const helmet = require('helmet');

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", 'data:', 'https:'],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"]
    }
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true
  },
  referrerPolicy: {
    policy: 'strict-origin-when-cross-origin'
  }
}));

// Additional security headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Permissions-Policy', 'geolocation=(), microphone=(), camera=()');
  next();
});
```

### CORS Configuration

```javascript
const cors = require('cors');

const corsOptions = {
  origin: (origin, callback) => {
    const whitelist = process.env.CORS_ORIGINS.split(',');
    
    if (!origin || whitelist.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  credentials: true,
  optionsSuccessStatus: 200,
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  exposedHeaders: ['X-RateLimit-Limit', 'X-RateLimit-Remaining'],
  maxAge: 86400 // 24 hours
};

app.use(cors(corsOptions));
```

---

## Vulnerability Management

### Dependency Scanning

```bash
# Run npm audit
npm audit

# Fix vulnerabilities
npm audit fix

# Force fix (may introduce breaking changes)
npm audit fix --force

# Check for outdated packages
npm outdated

# Update dependencies
npm update
```

### Automated Security Scans

```yaml
# .github/workflows/security-scan.yml
name: Security Scan

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0' # Weekly

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run npm audit
        run: npm audit --audit-level=moderate
      
      - name: Run Snyk scan
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

---

## Incident Response

### Security Incident Playbook

#### 1. Detection & Triage

- Monitor security alerts
- Review suspicious activity logs
- Assess severity (Critical/High/Medium/Low)

#### 2. Containment

```javascript
// Immediate actions for security breach
async function emergencyContainment() {
  // 1. Block suspicious IPs
  await blockSuspiciousIPs();
  
  // 2. Revoke compromised API keys
  await revokeCompromisedKeys();
  
  // 3. Force logout all users (if needed)
  await forceLogoutAllUsers();
  
  // 4. Enable read-only mode
  await enableReadOnlyMode();
  
  // 5. Notify security team
  await notifySecurityTeam();
}
```

#### 3. Investigation

- Review access logs
- Identify affected systems
- Determine breach scope
- Collect evidence

#### 4. Remediation

- Patch vulnerabilities
- Reset compromised credentials
- Update security policies
- Deploy fixes

#### 5. Recovery

- Restore from clean backups
- Verify system integrity
- Re-enable services gradually
- Monitor for recurrence

#### 6. Post-Incident

- Document incident
- Update runbook
- Notify affected users
- Conduct post-mortem
- Implement preventive measures

---

## Compliance

### Audit Logging

```javascript
async function logAuditEvent(event) {
  await db.auditLog.create({
    timestamp: new Date(),
    user_id: event.user_id,
    action: event.action,
    resource: event.resource,
    ip_address: event.ip,
    user_agent: event.user_agent,
    status: event.status,
    metadata: event.metadata
  });
}

// Middleware to log all API calls
app.use((req, res, next) => {
  const start = Date.now();
  
  res.on('finish', () => {
    logAuditEvent({
      user_id: req.user?.id,
      action: `${req.method} ${req.path}`,
      resource: req.path,
      ip: req.ip,
      user_agent: req.headers['user-agent'],
      status: res.statusCode,
      metadata: {
        duration_ms: Date.now() - start,
        request_size: req.headers['content-length'],
        response_size: res.getHeader('content-length')
      }
    });
  });
  
  next();
});
```

### Data Retention

```javascript
// Clean up old audit logs
cron.schedule('0 0 * * 0', async () => {
  const retentionDays = 90;
  const cutoff = new Date(Date.now() - retentionDays * 24 * 60 * 60 * 1000);
  
  await db.auditLog.deleteMany({
    where: {
      timestamp: { lt: cutoff }
    }
  });
  
  console.log(`Deleted audit logs older than ${retentionDays} days`);
});
```

---

## Contact Information

**Security Team:**
- Email: security@nexus.example.com
- Emergency Hotline: +1-XXX-XXX-XXXX
- PGP Key: https://nexus.example.com/security.asc

**Responsible Disclosure:**
- Email: security@nexus.example.com
- Bug Bounty: https://nexus.example.com/security/bounty

---

**Last Updated**: 2025-11-03  
**Next Review**: 2026-02-03
