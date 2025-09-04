# Netlify CMS Integration

This directory contains the Netlify CMS configuration for managing Jekyll posts in the Euystacio-Helmi AI project.

## Files

- `index.html` - Netlify CMS admin interface loader
- `config.yml` - CMS configuration for Jekyll posts and content management

## Features

The CMS is configured to manage:

1. **Blog Posts** (`_posts/`) - Jekyll blog posts with:
   - Title and date
   - Featured images
   - Tags and categories  
   - Full markdown content
   - Rating system (1-5 scale)

2. **Pages** (`pages/`) - Static pages with:
   - Custom permalinks
   - Markdown content

3. **Manifesto** (`manifesto/`) - Philosophical content with:
   - Title and markdown content

## Usage

1. Navigate to `/admin/` on your deployed site
2. Authenticate using Netlify Identity
3. Create and edit content through the visual interface
4. Changes are committed automatically to the repository

## Setup Requirements

For full functionality, the site needs:

1. Netlify deployment with Git Gateway enabled
2. Netlify Identity service configured
3. Editorial workflow enabled for content review

## Media Management

- Media files are stored in `static/images/uploads/`
- Images are accessible at `/static/images/uploads/` in posts
- Automatic image optimization and responsive handling

This integration maintains the sacred flow of collaborative creation while providing an intuitive content management experience.