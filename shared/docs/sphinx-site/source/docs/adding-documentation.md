# Adding Documentation Guide

This guide explains how to add new documentation files to the Sphinx documentation site.

All documentation files should be placed in the following directory:

```
shared/docs/sphinx-site/source/docs/
```

## Creating New Documentation

Create a new `.md` file in the docs directory:

```bash
# Navigate to the docs directory
cd shared/docs/sphinx-site/source/docs/

# Create new documentation file
touch my-new-guide.md
```

Use Markdown syntax for your content. Here's a basic template:

```markdown
# My New Guide Title

Brief description of what this guide covers.

Content for the first section.

More detailed content with examples.

```bash
# Example command
echo "Hello World"
```

Another section with different content.

> **Pro Tip**
> 
> Use callouts to highlight important information!

References:

- [External Link](https://example.com)
- [Git Philosophy Guide](git-philosophy.md)
```

Edit `shared/docs/sphinx-site/source/docs/index.md` to include your new file:

```markdown
```{toctree}
:maxdepth: 2
:caption: Shared Documentation

learning-paths
git-philosophy
my-new-guide
adding-documentation
local-development
```
```

**Important**: Use the filename without the `.md` extension in the toctree.

Build the documentation to see your changes:

```bash
cd shared/docs/sphinx-site
python docs.py build
```

Start the development server to preview:

```bash
python docs.py serve
```

Visit http://127.0.0.1:8000/docs/ to see your new documentation.

## Markdown Syntax Reference

Use different numbers of # for different header levels:

```markdown
# Main Title

## Section Header

### Subsection

#### Subsubsection
```

For code examples:

````markdown
```python
def hello_world():
    print("Hello, World!")
```

```bash
git commit -m "Add new feature"
```
````

**Bullet lists:**

```markdown
- Item one
- Item two
  - Nested item
- Item three
```

**Numbered lists:**

```markdown
1. First step
2. Second step
3. Third step
```

**External links:**

```markdown
Visit the [Sphinx documentation](https://www.sphinx-doc.org/).
```

**Internal links:**

```markdown
See [git-philosophy](git-philosophy.md) for Git workflow guidance.
```

Use callouts for special content:

```markdown
> **📝 Note**
> 
> This is a note callout.

> **⚠️ Warning**
> 
> This is a warning callout.

> **💡 Pro Tip**
> 
> This is a tip callout.
```

Simple tables:

```markdown
| Feature | Basic | Pro | Enterprise |
|---------|-------|-----|------------|
| Users | 1 | 5 | Unlimited |
| Storage | 1GB | 10GB | 100GB |
```

Reference other sections within the same document:

```markdown
See [Markdown Syntax Reference](#markdown-syntax-reference) above.

For more details, refer to the [Creating New Documentation](#creating-new-documentation) section.
```

Add images to your documentation:

```markdown
![Screenshot description](/_static/images/screenshot.png)
```

Include code directly from source files:

````markdown
```{literalinclude} ../../../python/examples/hello.py
:language: python
:lines: 1-10
```
````

Include mathematical expressions:

```markdown
The quadratic formula is $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$.

$$
\sum_{i=1}^n x_i = x_1 + x_2 + \cdots + x_n
$$
```

## Documentation Standards

1. **Clear Titles**: Use descriptive, action-oriented titles
2. **Consistent Structure**: Follow the established pattern of emoji headers
3. **Code Examples**: Include practical, working examples
4. **Step-by-Step**: Break complex processes into numbered steps
5. **Cross-References**: Link to related documentation

**File Naming Conventions:**
- Use lowercase with hyphens: `my-guide.md`
- Be descriptive: `api-integration-guide.md` not `api.md`
- Avoid spaces and special characters
- Keep names concise but meaningful

**Emoji Guidelines:**

Use emojis consistently for visual navigation:

- 📋 for lists, overviews, or summaries
- 🚀 for getting started or quick actions  
- 🔧 for technical/advanced topics
- 💡 for tips and best practices
- 🎯 for goals or objectives
- 📚 for references or learning resources
- ⚠️ for warnings or important notes
- ✅ for completed items or success states

## Quick Start Workflow

Here's the complete workflow to add new documentation:

```bash
# 1. Navigate to docs directory
cd shared/docs/sphinx-site/source/docs/

# 2. Create new Markdown file
touch deployment-guide.md

# 3. Edit the file with your content
# (use your preferred text editor)

# 4. Add to docs/index.md toctree
# (edit the toctree section to include your new file)

# 5. Build and test
cd ..  # back to sphinx-site directory
python docs.py build
python docs.py serve

# 6. Verify at http://127.0.0.1:8000/docs/
```

## Troubleshooting

**File not appearing in navigation:**
   Check that you added the filename (without .md) to the toctree in `docs/index.md`

**Build errors:**
   - Verify Markdown syntax is correct
   - Check MyST parser directives are properly formatted
   - Ensure all referenced files exist

**Links not working:**
   - Use correct relative paths for internal links
   - Verify external URLs are accessible
   - Check that referenced documents exist

**Images not displaying:**
   - Place images in `_static/images/` directory
   - Use correct relative paths: `/_static/images/filename.png`
   - Verify image files exist and are accessible

The build process may show warnings for:
- Missing files referenced in toctrees
- Missing images
- Unknown document references

These don't prevent building but should be addressed for a clean documentation site.

## Resources

- [MyST Parser Documentation](https://myst-parser.readthedocs.io/)
- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Local Development Workflow](local-development.md)