# Documentation Website

This directory contains the Sphinx documentation website for Amalie's Development Portfolio. The site showcases projects, learning progress, and technical insights across C#, Python, machine learning, and web development.

## 🌐 Live Site

Visit the documentation at: **https://yourusername.github.io/amalie_projects**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (recommended: Python 3.11+)
- pip (Python package manager)

### Installation Options

#### Option 1: Using pyproject.toml (Recommended)
```bash
# Install basic dependencies
pip install -e .

# Install with development tools
pip install -e ".[dev,enhanced,quality]" 

# Install all optional dependencies
pip install -e ".[all]"
```

#### Option 2: Using requirements.txt (Legacy)
```bash
pip install -r requirements.txt
```

### Local Development

#### Using the docs.py script (Cross-platform)
```bash
# Install dependencies
python docs.py install --dev

# Build documentation
python docs.py build

# Serve with auto-reload (recommended for development)
python docs.py serve

# Run quality checks
python docs.py lint

# Clean build files
python docs.py clean
```

#### Using traditional commands
```bash
# Build the site
python -m sphinx -b html source build/html

# Start development server (if sphinx-autobuild is installed)
python -m sphinx_autobuild source build/html --host 127.0.0.1 --port 8000

# Run quality checks
python -m rstcheck --recursive source/
python -m doc8 source/
```

### Available Commands

#### Build Commands (Cross-Platform)
| Command | Description |
|---------|-------------|
| `python docs.py install` | Install basic dependencies |
| `python docs.py install --dev` | Install development dependencies |
| `python docs.py build` | Build HTML documentation |
| `python docs.py serve` | Development server with auto-reload |
| `python docs.py lint` | Run documentation quality checks |
| `python docs.py clean` | Remove build artifacts |

## 📁 Structure

```
sphinx-site/
├── source/                 # Source files
│   ├── _static/           # Static assets (CSS, images, etc.)
│   ├── _templates/        # Custom templates
│   ├── about/             # About section
│   ├── projects/          # Project showcases
│   ├── csharp/            # C# development content
│   ├── python/            # Python and data science content
│   ├── machine-learning/  # ML/AI projects
│   ├── frontend/          # Frontend development
│   ├── setup/             # Setup and deployment guides
│   ├── conf.py            # Sphinx configuration
│   └── index.rst          # Homepage
├── build/                 # Generated HTML (ignored by git)
├── pyproject.toml         # Python project configuration & dependencies
├── Makefile              # Build commands
└── README.md             # This file
```

## 🎨 Features

- **Modern Design**: Clean, responsive layout with the Furo theme
- **Technology Sections**: Organized by programming language and domain
- **Project Showcases**: Detailed project descriptions with code examples
- **Learning Progress**: Skill development tracking and roadmaps
- **Auto-deployment**: Automatic GitHub Pages deployment via GitHub Actions
- **Search**: Full-text search functionality
- **Mobile Friendly**: Responsive design for all devices

## 🔧 Customization

### Theme Options
The site uses the [Furo](https://pradyunsg.me/furo/) theme. Customize colors, layout, and navigation in `source/conf.py`.

### Custom CSS
Modify `source/_static/custom.css` to adjust styling, add animations, or enhance the visual design.

### Adding Content
1. Create new `.rst` or `.md` files in appropriate sections
2. Add to the relevant `index.rst` toctree
3. Build locally to test
4. Commit changes to trigger auto-deployment

## 🚀 Deployment

### Automatic (GitHub Pages)
- Push changes to `main` branch
- GitHub Actions builds and deploys automatically
- Site available at `https://yourusername.github.io/amalie_projects`

### Manual Deployment
```bash
# Build production version
make production

# Deploy to gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
cp -r build/html/* .
git add .
git commit -m "Deploy documentation"
git push origin gh-pages
```

### Custom Domain
1. Add `CNAME` file to `source/_static/` with your domain
2. Configure DNS settings for your domain
3. Enable custom domain in GitHub repository settings

## 📚 Content Guidelines

### Writing Style
- Use clear, concise language
- Include practical code examples
- Add cross-references between related sections
- Follow consistent formatting and tone

### File Organization
- Use descriptive folder and file names
- Keep related content together
- Maintain consistent naming conventions
- Add README files for complex sections

### Images and Media
- Store in `source/_static/images/`
- Optimize for web (< 500KB recommended)
- Use descriptive alt text
- Include proper attribution

## 🛠️ Technology Stack

- **Sphinx**: Documentation generator
- **Furo**: Modern, responsive theme
- **MyST Parser**: Markdown support in Sphinx
- **GitHub Actions**: Automated CI/CD
- **GitHub Pages**: Free static site hosting

### Key Extensions
- `sphinx-copybutton`: Copy button for code blocks
- `sphinx-design`: Enhanced UI components
- `myst-parser`: Markdown parsing support
- `sphinx-external-toc`: External table of contents

## 🤝 Contributing

1. **Fork the repository** and create a feature branch
2. **Make changes** to documentation or code
3. **Test locally** using `make livehtml`
4. **Submit a pull request** with clear description
5. **Review process** includes automated checks and manual review

### Content Contributions
- Fix typos or improve clarity
- Add new project showcases
- Update learning progress and skills
- Enhance setup and deployment guides

## 🔍 SEO and Analytics

### Search Engine Optimization
- Semantic HTML structure
- Meta descriptions and titles
- Sitemap.xml generation
- Clean URL structure

### Analytics Integration
Configure Google Analytics in `conf.py`:
```python
html_theme_options = {
    "analytics_id": "G-XXXXXXXXXX",
}
```

## 📊 Performance

### Build Optimization
- Caching enabled for faster rebuilds
- Optimized image processing
- Minified CSS and JavaScript
- CDN-ready static assets

### Monitoring
- GitHub Actions build time tracking
- Page load speed monitoring
- Mobile-first responsive design
- Accessibility compliance

---

**Questions or Issues?** 
- Check the [Setup Guide](source/setup/index.rst) for detailed instructions
- Review the [Sphinx documentation](https://www.sphinx-doc.org/)
- Create an issue in the main repository

**Last Updated**: April 2026