import os
from pathlib import Path
import re


def get_readme_content_without_h1(readme_path: Path) -> str:
    """Return README content without the first H1 header line."""
    with open(readme_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Skip the first line if it's an H1 header
    if lines and lines[0].startswith("# "):
        return "".join(lines[1:]).lstrip()
    return "".join(lines)


#!/usr/bin/env python3
"""
Automatic project discovery and documentation generator for Sphinx site.
This script scans the repository for README files and generates RST files
that include them in the Sphinx documentation.
"""


def discover_project_directories(root_path: Path) -> list[str]:
    """Automatically discover project directories that contain README files."""
    project_dirs = []

    # Define top-level categories to scan
    top_level_dirs = [
        "python",
        "csharp",
        "frontend",
        "machine-learning",
        "fullstack-projects",
        "experiments",
    ]

    for top_dir in top_level_dirs:
        top_path = root_path / top_dir
        if top_path.exists():
            # For python directory, include ALL subdirectories (not just those with READMEs)
            if top_dir == "python":
                for item in top_path.iterdir():
                    if item.is_dir() and not item.name.startswith("."):
                        project_dirs.append(f"{top_dir}/{item.name}")
            else:
                # For other directories, only include if they have README files
                for item in top_path.iterdir():
                    if item.is_dir() and not item.name.startswith("."):
                        # Check if this subdirectory or its children have README files
                        has_readme = False

                        # Check immediate subdirectory
                        if (item / "README.md").exists():
                            has_readme = True

                        # Check nested subdirectories (one level deep)
                        if not has_readme:
                            for nested_item in item.iterdir():
                                if (
                                    nested_item.is_dir()
                                    and not nested_item.name.startswith(".")
                                    and (nested_item / "README.md").exists()
                                ):
                                    has_readme = True
                                    break

                        # Add to project_dirs if it has README files
                        if has_readme:
                            project_dirs.append(f"{top_dir}/{item.name}")

    # Sort for consistent ordering
    return sorted(project_dirs)


def find_project_readmes(root_path: Path) -> list[dict]:
    """Find all README files in project directories."""
    readmes = []

    # Automatically discover project directories
    project_dirs = discover_project_directories(root_path)
    print(f"Discovered project directories: {project_dirs}")

    for project_dir in project_dirs:
        full_path = root_path / project_dir
        if full_path.exists():
            # Look for README files in subdirectories, skip hidden dirs
            for item in full_path.iterdir():
                if item.is_dir() and not item.name.startswith("."):
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

                    # Special handling for multi-project directories (like django)
                    # Look for nested projects within directories that have their own README
                    if item.name.lower() in [
                        "django",
                        "fastapi",
                        "react",
                        "vue",
                        "mlflow",
                        "wpf",
                        "winui",
                        "maui",
                    ]:  # Add more as needed
                        for nested_item in item.iterdir():
                            if nested_item.is_dir() and not nested_item.name.startswith(
                                "."
                            ):
                                nested_readme_path = nested_item / "README.md"
                                if nested_readme_path.exists():
                                    # Calculate relative path for nested project
                                    nested_rel_path = os.path.relpath(
                                        nested_readme_path,
                                        root_path
                                        / "shared/docs/sphinx-site/source/projects",
                                    )
                                    nested_rel_path = nested_rel_path.replace("\\", "/")

                                    readmes.append(
                                        {
                                            "name": f"{item.name}-{nested_item.name}",
                                            "parent_category": item.name,
                                            "category": f"{project_dir.replace('/', '_')}_{item.name.lower()}",
                                            "path": nested_rel_path,
                                            "full_path": nested_readme_path,
                                            "title": create_title_from_readme(
                                                nested_readme_path
                                            ),
                                            "description": extract_project_description(
                                                nested_readme_path
                                            ),
                                            "technologies": extract_project_technologies(
                                                nested_readme_path
                                            ),
                                            "slug": f"{item.name.lower()}_{nested_item.name.lower()}".replace(
                                                "-", "_"
                                            ).replace(
                                                " ", "_"
                                            ),
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
                # Return complete sentence(s) - find end of sentence or reasonable break
                description = line

                # If line is very long (>300 chars), try to break at sentence end
                if len(description) > 300:
                    # Look for sentence endings within first 250 chars
                    sentence_ends = [".", "!", "?"]
                    for end_char in sentence_ends:
                        end_pos = description.find(end_char, 100, 250)
                        if end_pos != -1:
                            description = description[: end_pos + 1]
                            break
                    else:
                        # If no sentence end found, truncate at word boundary
                        words = description[:250].split()
                        description = " ".join(words[:-1]) + "..."

                return description

        return "A project showcasing development skills and best practices."
    except Exception:
        return "A project showcasing development skills and best practices."


def extract_project_technologies(readme_path: Path) -> list[str]:
    """Extract technologies/tech stack from README with deduplication and priority handling."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read().lower()

        # Technology patterns with priority (higher priority overrides lower)
        tech_patterns = {
            # Web Frameworks (high priority)
            "fastapi": ("FastAPI", 10),
            "django": ("Django", 10),
            "flask": ("Flask", 10),
            # Frontend Frameworks
            "react": ("React", 10),
            "vue": ("Vue.js", 10),
            "angular": ("Angular", 10),
            # Languages
            "typescript": ("TypeScript", 8),
            "javascript": ("JavaScript", 8),
            "python": ("Python", 8),
            "c#": ("C#", 8),
            # .NET Technologies
            "aspnet": ("ASP.NET", 9),
            "blazor": ("Blazor", 9),
            "wpf": ("WPF", 9),
            "maui": ("MAUI", 9),
            ".net": (".NET", 8),
            # ML/Data Science
            "pytorch": ("PyTorch", 9),
            "tensorflow": ("TensorFlow", 9),
            "scikit-learn": ("Scikit-learn", 9),
            "pandas": ("Pandas", 8),
            "numpy": ("NumPy", 8),
            # Infrastructure
            "docker": ("Docker", 7),
            "kubernetes": ("Kubernetes", 7),
            # Databases
            "postgresql": ("PostgreSQL", 7),
            "mongodb": ("MongoDB", 7),
            "redis": ("Redis", 7),
            "sqlite": ("SQLite", 7),
            # Testing (specific wins over general)
            "pywinauto": ("PyWinAuto", 10),
            "ui automation": ("UI Automation", 9),
            "performance testing": ("Performance Testing", 9),
            "pytest": ("PyTest", 8),
            "selenium": ("Selenium", 8),
            "test automation": ("Test Automation", 7),
            "automation": ("Automation", 6),
            "testing": ("Testing", 5),  # Most general, lowest priority
        }

        found_techs = {}  # Use dict to handle priorities

        # Find all matching technologies
        for pattern, (display_name, priority) in tech_patterns.items():
            if pattern in content:
                # Keep highest priority version
                if (
                    display_name not in found_techs
                    or found_techs[display_name] < priority
                ):
                    found_techs[display_name] = priority

        # Handle overlapping categories - remove less specific when more specific exists
        final_techs = set(found_techs.keys())

        # Remove general "Testing" if specific testing types exist
        if any(
            tech in final_techs
            for tech in [
                "PyTest",
                "Performance Testing",
                "UI Automation",
                "Test Automation",
            ]
        ):
            final_techs.discard("Testing")

        # Remove general "Automation" if specific automation types exist
        if any(tech in final_techs for tech in ["Test Automation", "UI Automation"]):
            final_techs.discard("Automation")

        return sorted(list(final_techs))  # Return deduplicated, sorted list
    except Exception:
        return []


def generate_project_rst(readmes: list[dict], output_dir: Path):
    """Generate individual project pages and category overview pages."""

    # Group readmes by category
    categories = {}
    all_readmes_by_category = {}  # Include nested projects for category pages

    for readme in readmes:
        cat = readme["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(readme)

        # Also group by main category for nested hierarchies
        main_cat = cat.split("_")[0] + "_" + cat.split("_")[1] if "_" in cat else cat
        if main_cat not in all_readmes_by_category:
            all_readmes_by_category[main_cat] = []
        all_readmes_by_category[main_cat].append(readme)

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
        # Skip nested categories - they'll be included in main category pages
        if any("parent_category" in p for p in projects):
            continue

        cat_name = category.replace("_", " ").title()
        cat_file = output_dir / f"{category}.rst"

        # Header
        rst_content = f"""
{cat_name} Projects  
{'=' * (len(cat_name) + 9)}

This section showcases all {cat_name.lower()} projects with their documentation and source code.

.. admonition:: Navigation Tip
   :class: tip

   Click on any project card to view its complete documentation, or use the dropdown to preview key information.

"""

        # Check if this category has nested projects
        nested_projects = []
        main_category_key = category
        for readme in readmes:
            if "parent_category" in readme and readme["category"].startswith(
                category + "_"
            ):
                nested_projects.append(readme)

        # Add toctree for nested projects if they exist
        if nested_projects:
            rst_content += f"""

**Projects in this Category**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 1
   :caption: {cat_name} Projects
   :hidden:

"""
            for project in nested_projects:
                nested_slug = f"{project['category']}_{project['slug']}"
                rst_content += f"   {nested_slug}\n"

        # Generate project cards (include both main projects and nested ones)
        all_projects = projects + nested_projects

        rst_content += f"""

.. grid:: 1 2 2 2
   :gutter: 3
   :margin: 2

"""

        for project in all_projects:
            project_slug = f"{project['category']}_{project['slug']}"
            tech_tags = ""
            if project["technologies"]:
                tech_tags = "\n   ".join(
                    [f":bdg-secondary:`{tech}`" for tech in project["technologies"]]
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
      
      .. dropdown:: Quick Preview
         :color: info
         :icon: book

         {preview_content}
         
         :doc:`View Full Documentation → <{category}_{project['slug']}>`

"""

        # Write category file
        with open(cat_file, "w", encoding="utf-8") as f:
            f.write(rst_content)

        print(f"Generated category page: {cat_file.name}")


def get_readme_preview(readme_path: Path, max_lines: int = 25) -> str:
    """Get a comprehensive preview of the README content, converting markdown to RST."""
    try:
        with open(readme_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        preview_lines = []
        code_block = False
        line_count = 0

        for line in lines:
            line = line.rstrip()

            # Track code blocks and convert to RST syntax
            if line.startswith("```"):
                code_block = not code_block
                if not code_block:  # Closing code block
                    # Don't add anything - RST code blocks end with unindented content
                    continue
                else:  # Opening code block
                    preview_lines.append("")
                    preview_lines.append(".. code-block:: text")
                    preview_lines.append("")
                continue

            # Inside code block - indent content
            if code_block:
                preview_lines.append(f"   {line}")
                continue

            # Skip title lines only
            if line.startswith("# ") and line_count == 0:
                line_count += 1
                continue

            # Convert markdown headers to RST format
            if line.startswith("## "):
                header_text = line[3:]  # Remove "## "
                preview_lines.append("")
                preview_lines.append(header_text)
                preview_lines.append("-" * len(header_text))
                preview_lines.append("")
                line_count += 1
                continue
            elif line.startswith("### "):
                header_text = line[4:]  # Remove "### "
                preview_lines.append("")
                preview_lines.append(header_text)
                preview_lines.append("^" * len(header_text))
                preview_lines.append("")
                line_count += 1
                continue

            # Include all other content
            if line.strip():
                preview_lines.append(line)
                line_count += 1

            # Stop at reasonable length but allow more content
            if line_count >= max_lines:
                break

        return "\n".join(preview_lines)
    except Exception:
        return "*Preview not available - view full documentation for details.*"


def update_projects_index(
    categories: list[str], readmes: list[dict], projects_index_path: Path
):
    """Update the main projects/index.rst to include all generated pages."""

    # Read existing content
    with open(projects_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Group readmes by main category (not sub-categories)
    main_categories = {}

    for readme in readmes:
        category = readme["category"]

        # Check if this is a nested project (has parent_category)
        if "parent_category" in readme:
            # This is a nested project - don't show it at top level
            continue
        else:
            # This is either a main category or an individual project
            main_category = (
                category.split("_")[0] + "_" + category.split("_")[1]
            )  # e.g., "python_web-frameworks"

            # Only include main framework/technology categories, not standalone projects
            if readme["name"].lower() in [
                "django",
                "fastapi",
                "react",
                "vue",
                "web-frameworks",
            ]:
                if main_category not in main_categories:
                    main_categories[main_category] = []
                main_categories[main_category].append(readme)
            # Skip standalone projects - they will be embedded in technology sections

    # Generate hierarchical toctree
    toctree_content = """

**Auto-Discovered Projects**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2
   :caption: Technologies & Projects
   :hidden:
   
"""

    # Add main category pages (these will contain nested projects)
    for main_category in sorted(main_categories.keys()):
        toctree_content += f"   {main_category}\n"

    # Always include C# documentation (manually created) - C# projects will be nested under this
    toctree_content += "   csharp\n"

    # Note: Standalone individual projects are NOT added here as they are embedded in technology sections

    # Add visual category grid (only main categories)
    toctree_content += f"""

.. grid:: 1 2 2 3
   :gutter: 3
   :margin: 3

"""

    category_display_names = {
        "python_web-frameworks": "Python Web Frameworks",
        "python_data-science": "Python Data Science",
        "python_utilities": "Python Utilities",
        "csharp": "C# Projects",
        "csharp_console-apps": "C# Console Apps",
        "csharp_desktop-apps": "C# Desktop Apps",
        "csharp_web-development": "C# Web Development",
        "frontend_react": "React Projects",
        "frontend_vue": "Vue.js Projects",
        "machine-learning_pytorch": "PyTorch Projects",
        "machine-learning_tensorflow": "TensorFlow Projects",
        "fullstack-projects": "Full-Stack Projects",
    }

    # Always include C# in the grid (manually created documentation)
    # Only include main framework/technology categories, not standalone projects
    grid_categories = list(main_categories.keys()) + ["csharp"]

    for category in sorted(set(grid_categories)):
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


def update_python_index(readmes: list[dict], python_index_path: Path, python_dir: Path):
    """Update the python/index.md file to maintain proper hierarchy matching project structure."""

    # Find Python projects
    python_projects = [
        readme for readme in readmes if readme["category"].startswith("python_")
    ]

    if not python_projects:
        return

    # Separate projects into hierarchy levels
    standalone_projects = []  # Top-level projects like automation-testing
    web_framework_projects = []  # Projects under web-frameworks

    for project in python_projects:
        category_base = project["category"].replace("python_", "")

        if "web-frameworks" in category_base:
            # This is a web framework subproject
            web_framework_projects.append(project)
        else:
            # This is a standalone top-level project
            standalone_projects.append(project)

            # Create individual page only for standalone projects
            project_filename = f"{category_base.replace('_', '-')}"
            project_file = python_dir / f"{project_filename}.md"

            # Generate project markdown content (strip H1 from README)
            tech_badges = ""
            if project["technologies"]:
                tech_list = " • ".join(project["technologies"])
                tech_badges = f"\n**Technologies:** {tech_list}\n"

            readme_content = get_readme_content_without_h1(project["full_path"])

            # Add extra blank lines for better spacing
            project_md_content = f"""# {project['title']}

{project['description']}

{tech_badges.strip() if tech_badges else ''}

{readme_content.strip()}

---

[← Back to Python Development](index.md)
"""

            with open(project_file, "w", encoding="utf-8") as f:
                f.write(project_md_content)

            print(f"Generated python project file: {project_file.name}")

    # Read existing python index content
    with open(python_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Build proper hierarchical toctree with deduplication
    toctree_entries = []
    seen = set()

    # Add main technology categories (these contain hierarchies)
    if web_framework_projects:
        if "web-frameworks" not in seen:
            toctree_entries.append("web-frameworks")
            seen.add("web-frameworks")

    # Add standalone projects
    for project in standalone_projects:
        project_filename = (
            f"{project['category'].replace('python_', '').replace('_', '-')}"
        )
        if project_filename not in seen:
            toctree_entries.append(project_filename)
            seen.add(project_filename)

    # Update toctree in content - remove individual web framework entries
    import re

    toctree_pattern = r"```{toctree}\n:maxdepth: 1\n:titlesonly:\n\n(.*?)```"
    toctree_content = "\n".join(toctree_entries)
    replacement = (
        f"```{{toctree}}\n:maxdepth: 1\n:titlesonly:\n\n{toctree_content}\n```"
    )

    if re.search(toctree_pattern, content, re.DOTALL):
        content = re.sub(toctree_pattern, replacement, content, flags=re.DOTALL)
    else:
        # Add toctree if it doesn't exist
        content += f"\n\n{replacement}"

    # Write updated content
    with open(python_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(
        f"Updated Python index with proper hierarchy: {len(toctree_entries)} main entries"
    )
    print(
        f"- Web framework projects: {len(web_framework_projects)} (nested under web-frameworks)"
    )
    print(f"- Standalone projects: {len(standalone_projects)}")


def update_csharp_index(readmes: list[dict], csharp_index_path: Path):
    """Update the csharp/index.md file to include discovered C# projects."""

    # Find C# projects
    csharp_projects = [
        readme for readme in readmes if readme["category"].startswith("csharp_")
    ]

    if not csharp_projects:
        return

    # Read existing content
    with open(csharp_index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Generate toctree entries for C# projects
    toctree_entries = ""
    for project in csharp_projects:
        project_slug = f"{project['category']}_{project['slug']}"
        toctree_entries += f"../projects/{project_slug}\n"

    # Update toctree in content
    import re

    toctree_pattern = r"```{toctree}\n:maxdepth: 2\n:hidden:\n\n(.*?)```"
    replacement = (
        f"```{{toctree}}\n:maxdepth: 2\n:hidden:\n\n{toctree_entries.strip()}\n```"
    )

    if re.search(toctree_pattern, content, re.DOTALL):
        content = re.sub(toctree_pattern, replacement, content, flags=re.DOTALL)
    else:
        # Add toctree if it doesn't exist (shouldn't happen after our fix)
        content += f"\n\n{replacement}"

    # Write updated content
    with open(csharp_index_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Updated C# index with {len(csharp_projects)} project(s)")


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

        # Update C# index with discovered C# projects
        update_csharp_index(readmes, sphinx_source / "csharp" / "index.md")

        # Update Python index with discovered Python projects
        update_python_index(
            readmes, sphinx_source / "python" / "index.md", sphinx_source / "python"
        )

        print("\nDocumentation generation complete!")
        print("Run 'sphinx-build source build/html' to rebuild documentation.")
    else:
        print("No README files found in project directories.")


if __name__ == "__main__":
    main()
