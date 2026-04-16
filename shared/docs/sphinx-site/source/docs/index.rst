Documentation Collection
========================

This section contains additional documentation files from the shared docs directory.
These files are automatically discovered and included during the build process.

*Last updated: April 16, 2026 at 02:03 PM*

📚 **Available Documentation**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. grid:: 1 1 2 2

   .. grid-item-card:: **Learning Paths**
      :link: learning-paths
      :link-type: doc
      :text-align: center
      :class-card: doc-card

      View the learning paths documentation.



📋 **Complete Documentation List**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. toctree::
   :maxdepth: 2
   :caption: Shared Documentation

   learning-paths


🔄 **How This Works**
^^^^^^^^^^^^^^^^^^^^

.. admonition:: Auto-Discovery Process
   :class: tip

   1. **Add markdown files** to ``shared/docs/`` directory
   2. **Build the site** with ``make html`` or push to GitHub
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
