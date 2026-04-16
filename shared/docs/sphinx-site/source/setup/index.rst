Setup Instructions
==================

This guide will help you set up and build the documentation site locally or deploy it to GitHub Pages.

📋 **Prerequisites**
^^^^^^^^^^^^^^^^^^^

Before you begin, ensure you have the following installed:

- **Python 3.9+** (recommended: Python 3.11)
- **Git** for version control
- **Make** (usually pre-installed on macOS/Linux, available via chocolatey on Windows)

🚀 **Quick Start**
^^^^^^^^^^^^^^^^^^

1. **Clone the repository**:
   ::

      git clone https://github.com/yourusername/amalie_projects.git
      cd amalie_projects

2. **Navigate to the documentation directory**:
   ::

      cd shared/docs/sphinx-site

3. **Install dependencies**:
   ::

      pip install -r requirements.txt

4. **Build the documentation**:
   ::

      make html

5. **View locally**:
   Open ``build/html/index.html`` in your browser, or use the development server:
   ::

      make livehtml

   This will start a development server at ``http://localhost:8000`` with auto-reload.

🛠️ **Development Workflow**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Available Make Commands**
***************************

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Command
     - Description
   * - ``make html``
     - Build HTML documentation
   * - ``make livehtml``
     - Start development server with auto-reload
   * - ``make clean``
     - Remove build artifacts
   * - ``make dev``
     - Quick development build with warnings
   * - ``make production``
     - Production build with strict checking
   * - ``make check``
     - Run documentation quality checks
   * - ``make linkcheck``
     - Check for broken links

**Development Server**
**********************

For active development, use the live reload server:

::

   make livehtml

This will:
- Start a local server at ``http://localhost:8000``
- Watch for file changes and auto-rebuild
- Automatically refresh your browser
- Watch the entire repository for changes

**Content Creation Guidelines**
*******************************

1. **File Organization**:
   - Use descriptive folder names (``projects/``, ``learning/``, etc.)
   - Keep related content together
   - Use consistent naming conventions

2. **Writing Style**:
   - Use reStructuredText (``.rst``) or Markdown (``.md``) format
   - Include clear headings and navigation
   - Add code examples with proper syntax highlighting
   - Use admonitions for important notes

3. **Images and Media**:
   - Store images in ``source/_static/images/``
   - Use descriptive filenames
   - Optimize images for web (< 500KB recommended)
   - Include alt text for accessibility

🌐 **GitHub Pages Deployment**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The documentation is automatically deployed to GitHub Pages when you push to the main branch.

**Automatic Deployment**
************************

The ``.github/workflows/docs.yml`` workflow:

1. Triggers on pushes to ``main`` branch
2. Installs Python and dependencies
3. Builds the Sphinx documentation
4. Deploys to GitHub Pages
5. Available at: ``https://yourusername.github.io/amalie_projects``

**Manual Deployment**
*********************

If you need to deploy manually:

1. **Build the documentation**:
   ::

      make production

2. **Deploy to gh-pages branch**:
   ::

      # Create and switch to gh-pages branch
      git checkout --orphan gh-pages
      git rm -rf .
      
      # Copy build files
      cp -r shared/docs/sphinx-site/build/html/* .
      echo "yourdomain.com" > CNAME  # Optional: custom domain
      
      # Commit and push
      git add .
      git commit -m "Deploy documentation"
      git push origin gh-pages

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Set source to "Deploy from a branch"
   - Select ``gh-pages`` branch
   - Click Save

🎨 **Customization**
^^^^^^^^^^^^^^^^^^^

**Theme Configuration**
***********************

The site uses the modern `Furo <https://pradyunsg.me/furo/>`_ theme. Key customization options in ``conf.py``:

.. code-block:: python

   html_theme_options = {
       "sidebar_hide_name": True,
       "light_css_variables": {
           "color-brand-primary": "#2563eb",
           # Add more custom colors
       },
       # Add footer icons, navigation, etc.
   }

**Custom CSS**
**************

Modify ``source/_static/custom.css`` to:
- Adjust colors and typography
- Add custom components
- Enhance responsive design
- Improve accessibility

**Adding Extensions**
*********************

To add Sphinx extensions:

1. Install the extension: ``pip install sphinx-extension-name``
2. Add to ``conf.py``:
   ::

      extensions = [
          # existing extensions
          'new_extension_name',
      ]
3. Configure extension options as needed
4. Update dependencies in ``pyproject.toml``

🔧 **Troubleshooting**
^^^^^^^^^^^^^^^^^^^^^

**Common Issues**
*****************

.. admonition:: Build Errors
   :class: warning

   If you encounter build errors:
   
   1. Check Python version (3.9+ required)
   2. Ensure all dependencies are installed
   3. Clear build cache: ``make clean``
   4. Check for syntax errors in ``.rst`` files

.. admonition:: GitHub Pages Not Updating
   :class: warning

   If changes don't appear on GitHub Pages:
   
   1. Check the Actions tab for workflow status
   2. Ensure the workflow has proper permissions
   3. Verify the gh-pages branch exists and is set as source
   4. Clear browser cache

**Performance Optimization**
****************************

For large documentation sites:

1. **Optimize Images**: Compress images and use appropriate formats
2. **Enable Caching**: Configure Sphinx caching for faster builds
3. **Lazy Loading**: Use sphinx-design for progressive loading
4. **CDN**: Consider using a CDN for static assets

📊 **Analytics and Monitoring**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Google Analytics Integration**
********************************

Add to ``conf.py``:

.. code-block:: python

   html_theme_options = {
       # other options
       "analytics_id": "G-XXXXXXXXXX",  # Your GA4 tracking ID
   }

**GitHub Pages Analytics**
**************************

Monitor site performance through:
- GitHub Insights → Traffic
- Google Search Console
- GitHub Pages build logs

🤝 **Contributing to Documentation**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Adding New Sections**
***********************

1. Create new folder in ``source/``
2. Add ``index.rst`` with content
3. Update main ``index.rst`` toctree
4. Test locally before committing

**Writing Guidelines**
**********************

- Use clear, concise language
- Include code examples with explanations
- Add cross-references to related sections
- Follow the established style and tone

**Review Process**
******************

1. Create feature branch for changes
2. Test build locally
3. Submit pull request
4. Review automated checks
5. Merge after approval

---

**Need Help?** Check the `Sphinx documentation <https://www.sphinx-doc.org/>`_ or create an issue in the repository for assistance.