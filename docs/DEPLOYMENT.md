# Deployment Guide - Euystacio Bidirectional Dashboard

This guide covers deployment of the bidirectional dashboard to both GitHub Pages and Netlify platforms.

## 🚀 GitHub Pages Deployment

### Automatic Deployment (Recommended)

The repository is configured for automatic deployment via GitHub Actions:

1. **Workflow Location**: `.github/workflows/deploy.yml`
2. **Trigger**: Push to `main` branch or pull request
3. **Build Command**: `python build_static.py`
4. **Source Directory**: `/docs`
5. **Live URL**: `https://[username].github.io/euystacio-helmi-AI/dashboard/`

### Manual Setup

If you need to configure GitHub Pages manually:

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs`
4. The dashboard will be available at `/dashboard/` path

### Build Process

```bash
# Install dependencies
pip install -r requirements.txt

# Build static version
python build_static.py

# Files are generated in docs/ directory:
# - docs/index.html (Classic dashboard)
# - docs/dashboard/index.html (Bidirectional dashboard)
# - docs/api/ (Static API endpoints)
```

## 🌐 Netlify Deployment

### Configuration

The repository includes `netlify.toml` for automatic Netlify deployment:

```toml
[build]
  publish = "docs"
  command = "python build_static.py"

[build.environment]
  PYTHON_VERSION = "3.8"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

### Deployment Steps

1. **Connect Repository**: Link your GitHub repo to Netlify
2. **Build Settings**:
   - Build command: `python build_static.py`
   - Publish directory: `docs`
   - Environment: Python 3.8+
3. **Custom Domain** (Optional): Configure your domain in Netlify settings
4. **Deploy**: Netlify will automatically build and deploy on git push

### Performance Features

- **CDN**: Global content delivery network
- **SSL**: Automatic HTTPS certificates
- **Branch Previews**: Deploy preview for pull requests
- **Form Handling**: Enhanced form processing capabilities

## 📱 Access Points

### Primary Dashboard
- **GitHub Pages**: `https://[username].github.io/euystacio-helmi-AI/dashboard/`
- **Netlify**: `https://[site-name].netlify.app/dashboard/`
- **Local**: `docs/dashboard/index.html`

### Classic Dashboard
- **GitHub Pages**: `https://[username].github.io/euystacio-helmi-AI/`
- **Netlify**: `https://[site-name].netlify.app/`
- **Local**: `docs/index.html`

## 🔐 Access Control Configuration

### Public Features (No Authentication)
- Real-time bidirectional communication
- Live emotional pulse exchange
- Public analytics and metrics
- AI response generation

### Protected Features (Authentication Required)
- Detailed interaction summaries
- Advanced analytics and patterns
- System administration tools
- Historical data access

### Demo Authentication
- **Username**: `demo`
- **Password**: `euystacio2025`
- **Session Duration**: 24 hours
- **Storage**: Client-side localStorage

## ⚙️ Technical Requirements

### Dependencies
- Python 3.8+
- Flask (for development server)
- No external JavaScript libraries (vanilla JS)

### Browser Support
- Modern browsers with ES6+ support
- Chrome 60+, Firefox 55+, Safari 12+, Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

### Performance
- **Load Time**: < 2 seconds on 3G
- **Bundle Size**: < 500KB total
- **Offline**: Basic functionality via localStorage
- **Responsive**: Works on all screen sizes

## 🔧 Environment Configuration

### Development
```bash
# Local development server
cd docs
python -m http.server 8000
# Access: http://localhost:8000/dashboard/

# Flask development (dynamic features)
python app.py
# Access: http://localhost:5000
```

### Production
Both GitHub Pages and Netlify serve static files:
- No server-side processing required
- All functionality works client-side
- Data persistence via localStorage
- Authentication handled in JavaScript

## 🔍 Testing

### Functional Testing
- ✅ Bidirectional pulse sending/receiving
- ✅ Authentication flow (demo credentials)
- ✅ Protected section access control
- ✅ Real-time state updates
- ✅ Responsive design across devices

### Cross-Platform Testing
- ✅ GitHub Pages deployment
- ✅ Netlify deployment
- ✅ Local development server
- ✅ Mobile device compatibility

## 🚨 Troubleshooting

### Common Issues

**Build Fails**: Ensure Python 3.8+ and required dependencies are installed
```bash
pip install -r requirements.txt
python build_static.py
```

**Dashboard Not Loading**: Check browser console for JavaScript errors
- Verify file paths are correct
- Ensure HTTPS is used for external fonts

**Authentication Not Working**: Clear localStorage and try again
```javascript
localStorage.removeItem('euystacio_auth');
```

**Protected Sections Inaccessible**: Verify authentication status
- Use demo credentials: `demo` / `euystacio2025`
- Check browser network tab for issues

### Debug Mode
Add `?debug=1` to URL for verbose console logging
```
https://[site]/dashboard/?debug=1
```

## 📊 Analytics & Monitoring

### Available Metrics
- Pulse sending/receiving rates
- Authentication success rates
- Session duration tracking
- Feature usage analytics
- Real-time connection monitoring

### Performance Monitoring
- Page load times
- JavaScript execution times
- localStorage usage
- Browser compatibility issues

## 🔄 Updates & Maintenance

### Automated Updates
- GitHub Actions rebuilds on every push
- Netlify rebuilds on git push
- Static assets cached with versioning

### Manual Updates
```bash
# Update static build
python build_static.py

# Commit changes
git add docs/
git commit -m "Update dashboard build"
git push origin main
```

## 🛡️ Security Considerations

### Client-Side Security
- All authentication handled locally
- No sensitive data transmitted
- Session timeout enforced
- Local storage cleaned on logout

### Deployment Security
- HTTPS enforced on both platforms
- No server vulnerabilities (static-only)
- Content Security Policy headers
- XSS protection via HTML sanitization

---

*For support or questions about deployment, please refer to the project's main documentation or create an issue in the repository.*