#!/usr/bin/env python3
"""
Automatic project discovery and documentation generator for Sphinx site.
This script scans the repository for README files and generates RST files
that include them in the Sphinx documentation.
"""

import os
from pathlib import Path
import re


def find_project_readmes(root_path: Path) -> list[dict]:
    """Find all README files in project directories."""
    readmes = []

    # Define project directories to scan
    project_dirs = [
        "python/web-frameworks",
        "python/data-science",
        "python/utilities",
        "csharp/console-apps",
        "csharp/desktop-apps",
        "csharp/web-development",
        "frontend/react",
        "frontend/vue",
        "frontend/vanilla-js",
        "machine-learning/pytorch",
        "machine-learning/tensorflow",
        "machine-learning/scikit-learn",
        "fullstack-projects",
    ]

    for project_dir in project_dirs:
        full_path = root_path / project_dir
        if full_path.exists():
            # Look for README files in subdirectories
            for item in full_path.iterdir():
                if item.is_dir():
                    readme_path = item / "README.md"
                    if readme_path.exists():
                        # Calculate relative path from sphinx source/projects directory (where RST files are generated)
                        rel_path = os.path.relpath(
                            readme_path,
                            root_path / "shared/docs/sphinx-site/source/projects",
                        )
                        # Ensure forward slashes for cross-platform compatibility
                        rel_path = rel_path.replace("\\", "/")

                        readmes.append(
                            {
                                "name": item.name,
                                "category": project_dir.replace("/", "_"),
                                "path": rel_path,
                                "full_path": readme_path,
                                "title": create_title_from_readme(readme_path),
                                "description": extract_project_description(readme_path),
                                "technologies": extract_project_technologies(
                                    readme_path
                                ),
                                "slug": item.name.lower()
                                .replace("-", "_")
                                .replace(" ", "_"),
                            }
                        )

    return readmes


def create_title_from_readme(readme_path: Path) -> str:
    """Extract the first heading from a README file."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line.startswith("#"):
                return first_line.lstrip("# ")
            return readme_path.parent.name.replace("-", " ").title()
    except Exception:
        return readme_path.parent.name.replace("-", " ").title()


def extract_project_description(readme_path: Path) -> str:
    """Extract a brief description from README (first paragraph after title)."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Skip title lines and find first paragraph
        for i, line in enumerate(lines):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("```"):
                # Return first meaningful paragraph, truncated
                description = line[:150]
                if len(line) > 150:
                    description += "..."
                return description

        return "A project showcasing development skills and best practices."
    except Exception:
        return "A project showcasing development skills and best practices."


def extract_project_technologies(readme_path: Path) -> list[str]:
    """Extract technologies/tech stack from README."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        # Common technology keywords to look for
        tech_patterns = {
            "fastapi": "FastAPI",
            "django": "Django",
            "flask": "Flask",
            "react": "React",
            "vue": "Vue.js",
            "angular": "Angular",
            "typescript": "TypeScript",
            "javascript": "JavaScript",
            "python": "Python",
            "c#": "C#",
            "aspnet": "ASP.NET",
            "blazor": "Blazor",
            "wpf": "WPF",
            "maui": "MAUI",
            "pytorch": "PyTorch",
            "tensorflow": "TensorFlow",
            "scikit-learn": "Scikit-learn",
            "pandas": "Pandas",
            "numpy": "NumPy",
            "docker": "Docker",
            "kubernetes": "Kubernetes",
            "postgresql": "PostgreSQL",
            "mongodb": "MongoDB",
            "redis": "Redis",
            "sqlite": "SQLite",
        }

        found_techs = []
        for pattern, display_name in tech_patterns.items():
            if pattern in content:
                found_techs.append(display_name)

        return found_techs[:5]  # Limit to 5 technologies
    except Exception:
        return []


def generate_project_rst(readmes: list[dict], output_dir: Path):
    """Generate individual project pages and category overview pages."""

    # Group readmes by category
    categories = {}
    for readme in readmes:
        cat = readme["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(readme)

    # Create individual project pages
    for readme in readmes:
        project_slug = f"{readme['category']}_{readme['slug']}"
        project_file = output_dir / f"{project_slug}.rst"

        # Generate individual project page
        tech_badges = ""
        if readme["technologies"]:
            tech_list = " • ".join(readme["technologies"])
            tech_badges = f"\n**Technologies:** {tech_list}\n"

        project_content = f"""
{readme['title']}
{'=' * len(readme['title'])}

{readme['description']}
{tech_badges}

.. include:: {readme['path']}
   :parser: myst_parser.sphinx_

----

:doc:`← Back to {readme['category'].replace('_', ' ').title()} Projects <{readme['category']}>`

"""

        with open(project_file, "w", encoding="utf-8") as f:
            f.write(project_content)

        print(f"Generated project page: {project_file.name}")

    # Generate category overview pages with project cards
    for category, projects in categories.items():
        cat_name = category.replace("_", " ").title()
        cat_file = output_dir / f"{category}.rst"

        # Header
        rst_content = f"""
{cat_name} Projects  
{'=' * (len(cat_name) + 9)}

This section showcases all {cat_name.lower()} projects with their documentation and source code.

.. admonition:: 💡 Navigation Tip
   :class: tip

   Click on any project card to view its complete documentation, or use the dropdown to preview key information.

"""

        # Generate project cards
        rst_content += f"""
.. grid:: 1 2 2 2
   :gutter: 3
   :margin: 2

"""

        for project in projects:
            project_slug = f"{category}_{project['slug']}"
            tech_tags = ""
            if project["technologies"]:
                tech_tags = "\n   ".join(
                    [f":bdg-secondary:`{tech}`" for tech in project["technologies"][:4]]
                )
                if tech_tags:
                    tech_tags = f"\n   \n   {tech_tags}"

            rst_content += f"""   .. grid-item-card:: {project['title']}
      :link: {project_slug}
      :link-type: doc
      :class-card: project-card
      :text-align: left

      {project['description']}{tech_tags}
      
      +++
      
      .. button-link:: {project_slug}
         :color: primary
         :outline:
         :expand:
         
         View Details →

"""

        # Add collapsible quick preview section
        rst_content += f"""

**Quick Preview**
^^^^^^^^^^^^^^^^^^

.. tab-set::

"""

        for project in projects:
            # Get first few lines of README for preview
            preview_content = get_readme_preview(project["full_path"])

            rst_content += f"""
   .. tab-item:: {project['title']}

      {project['description']}
      
      **Technologies:** {', '.join(project['technologies']) if project['technologies'] else 'Various'}
      
      .. dropdown:: 📖 Quick Preview
         :color: info
         :icon: book

         {preview_content}
         
         :doc:`View Full Documentation → <{category}_{project['slug']}>`

"""

        # Write category file
        with open(cat_file, "w", encoding="utf-8") as f:
            f.write(rst_content)

        print(f"Generated category page: {cat_file.name}")


def get_readme_preview(readme_path: Path, max_lines: int = 10) -> str:
    """Get a preview of the README content (first few meaningful lines)."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        preview_lines = []
        code_block = False

        for line in lines[
            : max_lines + 5
        ]:  # Read a bit more to find good stopping point
            line = line.rstrip()

            # Track code blocks
            if line.startswith("```"):
                code_block = not code_block
                continue

            # Skip if we're in a code block or line is just formatting
            if code_block or line.startswith("#") or not line.strip():
                continue

            preview_lines.append(line)

            # Stop at a good breaking point
            if len(preview_lines) >= max_lines:
                break

        preview = "\n".join(preview_lines[:max_lines])
        if len(lines) > max_lines:
            preview += "\n\n*... (view full documentation for complete details)*"

        return preview
    except Exception:
        return "*Preview not available - view full documentation for details.*"


def update_projects_index(
    categories: list[str], readmes: list[dict], projects_index_path: Path
):
    """Update the main projects/index.rst to include all generated pages."""

    # Read existing content
    with open(projects_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate toctree for auto-discovered projects
    toctree_content = """

**Auto-Discovered Projects**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1
   :caption: Project Categories
   :hidden:
   
"""

    # Add category pages
    for category in sorted(categories):
        toctree_content += f"   {category}\n"

    # Add individual project pages
    toctree_content += "\n.. toctree::\n   :maxdepth: 1\n   :caption: Individual Projects\n   :hidden:\n\n"

    for readme in readmes:
        project_slug = f"{readme['category']}_{readme['slug']}"
        toctree_content += f"   {project_slug}\n"

    # Add visual category grid
    toctree_content += f"""

.. grid:: 1 2 2 3
   :gutter: 3
   :margin: 3

"""

    category_display_names = {
        "python_web-frameworks": "🐍 Python Web Frameworks",
        "python_data-science": "📊 Python Data Science",
        "python_utilities": "🔧 Python Utilities",
        "csharp_console-apps": "💻 C# Console Apps",
        "csharp_desktop-apps": "🖥️ C# Desktop Apps",
        "csharp_web-development": "🌐 C# Web Development",
        "frontend_react": "⚛️ React Projects",
        "frontend_vue": "💚 Vue.js Projects",
        "machine-learning_pytorch": "🔥 PyTorch Projects",
        "machine-learning_tensorflow": "🧠 TensorFlow Projects",
        "fullstack-projects": "🚀 Full-Stack Projects",
    }

    for category in sorted(categories):
        display_name = category_display_names.get(
            category, category.replace("_", " ").title()
        )

        toctree_content += f"""   .. grid-item-card:: {display_name}
      :link: {category}
      :link-type: doc
      :text-align: center
      :class-card: category-card

      Explore projects and documentation
      
      +++
      
      Explore →

"""

    # Append or update the auto-discovered section
    if "Auto-Discovered Projects" in content:
        # Replace existing section
        pattern = r"\*\*Auto-Discovered Projects\*\*.*?(?=\*\*|\Z)"
        content = re.sub(pattern, toctree_content.strip(), content, flags=re.DOTALL)
    else:
        # Append to end
        content += toctree_content

    # Write updated content
    with open(projects_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated: {projects_index_path}")


def main():
    """Main execution function."""
    # Get paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent.parent  # Go up to repo root
    sphinx_source = script_dir / "source"
    projects_dir = sphinx_source / "projects"

    print(f"Scanning for README files in: {repo_root}")

    # Find all project READMEs
    readmes = find_project_readmes(repo_root)
    print(f"Found {len(readmes)} project README files")

    if readmes:
        # Generate RST files
        generate_project_rst(readmes, projects_dir)

        # Update main projects index
        categories = list(set(readme["category"] for readme in readmes))
        update_projects_index(categories, readmes, projects_dir / "index.rst")

        print("\nDocumentation generation complete!")
        print("Run 'sphinx-build source build/html' to rebuild documentation.")
    else:
        print("No README files found in project directories.")


if __name__ == "__main__":
    main()
