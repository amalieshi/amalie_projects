#!/usr/bin/env python3
"""
Build script to automatically include markdown files from shared/docs
into the Sphinx documentation site.
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime


def setup_external_docs():
    """Copy markdown files from shared/docs to source directory and create index."""

    # Get directories
    script_dir = Path(__file__).parent
    source_dir = script_dir / "source"
    docs_root = script_dir.parent  # This should be shared/docs
    external_docs_dir = source_dir / "docs"

    print(f"🔍 Looking for markdown files in: {docs_root}")

    # Create docs directory in source if it doesn't exist
    external_docs_dir.mkdir(exist_ok=True)

    # Find all markdown files in shared/docs (excluding sphinx-site)
    md_files = []
    for md_file in docs_root.glob("*.md"):
        print(f"📄 Found file: {md_file}")
        if md_file.is_file() and "sphinx-site" not in str(md_file):
            # Copy file to source/docs
            dest_file = external_docs_dir / md_file.name
            shutil.copy2(md_file, dest_file)

            # Add to list for index generation
            md_files.append(
                {
                    "name": md_file.stem,
                    "filename": md_file.name,
                    "title": md_file.stem.replace("-", " ").replace("_", " ").title(),
                    "path": f"docs/{md_file.name}",
                }
            )

            print(f"✅ Copied: {md_file.name}")

    # Generate index file for external docs
    if md_files:
        generate_docs_index(external_docs_dir, md_files)
        print(f"📄 Generated index for {len(md_files)} documentation files")

    return md_files


def generate_docs_index(docs_dir, md_files):
    """Generate an index.rst file for the external documentation."""

    index_content = f"""Documentation Collection
========================

This section contains additional documentation files from the shared docs directory.
These files are automatically discovered and included during the build process.

*Last updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*

📚 **Available Documentation**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grid:: 1 1 2 2

"""

    # Add grid items for each doc
    for doc in md_files:
        index_content += f"""   .. grid-item-card:: **{doc['title']}**
      :link: {doc['name']}
      :link-type: doc
      :text-align: center
      :class-card: doc-card

      View the {doc['title'].lower()} documentation.

"""

    # Add toctree
    index_content += f"""

📋 **Complete Documentation List**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2
   :caption: Shared Documentation

"""

    # Add each file to toctree
    for doc in md_files:
        index_content += f"   {doc['name']}\n"

    # Add usage instructions
    index_content += f"""

🔄 **How This Works**
^^^^^^^^^^^^^^^^^^^^

.. admonition:: Auto-Discovery Process
   :class: tip

   1. **Add markdown files** to ``shared/docs/`` directory
   2. **Build the site** with ``python docs.py build`` or push to GitHub
   3. **Files are automatically** copied and indexed
   4. **Navigation is updated** to include new content

**Supported File Types:**
- ``.md`` - Markdown files with MyST extensions
- Automatic title generation from filename
- Cross-references between documentation files

**File Naming:**
- Use descriptive filenames: ``learning-paths.md``, ``setup-guide.md``
- Avoid spaces (use hyphens or underscores)
- Use lowercase for consistency

---

*These files are synchronized from ``shared/docs/`` during each build.*
"""

    # Write the index file
    index_file = docs_dir / "index.rst"
    with open(index_file, "w", encoding="utf-8") as f:
        f.write(index_content)


if __name__ == "__main__":
    print("🔧 Setting up external documentation...")
    try:
        md_files = setup_external_docs()
        if md_files:
            print(f"✅ Successfully processed {len(md_files)} documentation files")
        else:
            print("ℹ️  No markdown files found in shared/docs")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
