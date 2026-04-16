# Documentation Website

This directory contains the Sphinx documentation website for the development portfolio, showcasing projects and technical insights across multiple technology stacks.

## Live Documentation

Visit the documentation at: **https://yourusername.github.io/amalie_projects**

## Development Setup

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
| `python docs.py discover` | Auto-discover project README files |
| `python docs.py build` | Build HTML documentation (includes discovery) |
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
│   ├── projects/          # Auto-generated project showcases
│   ├── csharp/            # C# development content
│   ├── docs/              # Documentation guides
│   ├── conf.py            # Sphinx configuration
│   └── index.rst          # Homepage
├── build/                 # Generated HTML (ignored by git)
├── docs.py                # Cross-platform build script
├── generate_project_docs.py # Auto-discovery system
├── pyproject.toml         # Python project configuration & dependencies
└── README.md             # This file
```

## 🎨 Features

- **Modern Design**: Clean, responsive layout with the Furo theme
- **Auto-Discovery**: Automatically includes README files from your projects 
- **Technology Sections**: Organized by programming language and domain
- **Project Showcases**: Card-based layout with individual project pages
- **Learning Progress**: Skill development tracking and roadmaps
- **Auto-deployment**: Automatic GitHub Pages deployment via GitHub Actions
- **Search**: Full-text search functionality
- **Mobile Friendly**: Responsive design for all devices

## 🤖 Auto-Discovery System

The documentation site automatically discovers and includes README files from your projects, creating a scalable project showcase.

### Quick Commands
```bash
# Auto-discover projects and build (recommended)
python docs.py build

# Run only project discovery
python docs.py discover
```

### How It Works
1. **Scans** your repository for README files in project directories
2. **Extracts** project information (title, description, technologies)  
3. **Generates** individual project pages with full README content
4. **Creates** category overview pages with project cards
5. **Updates** navigation automatically


### Benefits
- ✅ **Automatic**: New projects appear instantly when you add README files
- ✅ **Organized**: Projects grouped by technology categories  
- ✅ **Scalable**: Handles unlimited projects with card-based navigation
- ✅ **Consistent**: Uniform styling and structure across all projects
- ✅ **Single Source**: README files remain your primary documentation

## 🔧 Adding Projects

### Automatic Discovery
Simply add a `README.md` file to any project in these directories:
- `python/web-frameworks/` - Python web development projects
- `python/data-science/` - Data analysis and ML projects  
- `csharp/desktop-apps/` - C# desktop applications
- `csharp/web-development/` - ASP.NET and web APIs
- `frontend/react/` - React applications
- `machine-learning/pytorch/` - PyTorch projects
- And more... (see `generate_project_docs.py` for full list)

### Manual Content
Add custom documentation by creating `.rst` or `.md` files in `source/` and adding them to the relevant `index.rst` toctree.

## 🎨 Customization

### Theme Options
The site uses the [Furo](https://pradyunsg.me/furo/) theme. Customize colors, layout, and navigation in `source/conf.py`.

### Custom CSS
Modify `source/_static/custom.css` to adjust styling, add animations, or enhance the visual design.

### Project Categories
Edit `generate_project_docs.py` to add new project directories or customize category names and display.

## �️ Technology Stack

- **Sphinx**: Documentation generator
- **Furo**: Modern, responsive theme
- **MyST Parser**: Markdown support in Sphinx
- **Auto-Discovery**: Custom project detection system
- **GitHub Actions**: Automated CI/CD
- **GitHub Pages**: Free static site hosting

### Key Extensions
- `sphinx-copybutton`: Copy button for code blocks
- `sphinx-design`: Enhanced UI components and cards
- `myst-parser`: Markdown parsing support
- `sphinx-tabs`: Tabbed content interface

## �🚀 Deployment

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

## 🤝 Contributing

1. **Fork the repository** and create a feature branch
2. **Make changes** to documentation or add new projects
3. **Test locally** using `python docs.py build`
4. **Submit a pull request** with clear description

### Content Contributions
- Add new project showcases (just create README files!)
- Fix typos or improve clarity
- Update learning progress and skills
- Enhance setup and deployment guides

---

**Questions or Issues?** 
- Check the [Sphinx documentation](https://www.sphinx-doc.org/)
- Review your project's README files that will be auto-discovered and added to the sphinx documentation site
- Create an issue in the main repository

**Last Updated**: April 2026