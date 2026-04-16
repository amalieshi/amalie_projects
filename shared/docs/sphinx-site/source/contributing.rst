Contributing Guidelines
======================

Thank you for your interest in contributing to this portfolio documentation! This guide outlines how you can help improve the content, fix issues, or suggest enhancements.

🤝 **Ways to Contribute**
^^^^^^^^^^^^^^^^^^^^^^^^^

**Content Improvements**
************************

- Fix typos, grammar, or formatting issues
- Improve clarity and readability
- Add missing information or context
- Update outdated technical information
- Enhance code examples with better explanations

**Technical Enhancements**
**************************

- Improve site performance and loading speed
- Enhance responsive design and accessibility
- Add new Sphinx extensions or features
- Optimize build process and deployment
- Fix cross-browser compatibility issues

**New Content**
***************

- Suggest new project showcases
- Add learning resources and tutorials
- Contribute guest blog posts or insights
- Share alternative approaches or solutions
- Expand technical documentation

📋 **Before You Start**
^^^^^^^^^^^^^^^^^^^^^^

1. **Check existing issues**: Look for open issues that match your contribution idea
2. **Create an issue**: For significant changes, create an issue to discuss the proposal first
3. **Read the style guide**: Follow the established writing and formatting conventions
4. **Test locally**: Ensure your changes build correctly before submitting

🚀 **Getting Started**
^^^^^^^^^^^^^^^^^^^^^

**1. Fork and Clone**
*********************

.. code-block:: bash

   # Fork the repository on GitHub, then clone your fork
   git clone https://github.com/your-username/amalie_projects.git
   cd amalie_projects

   # Add upstream remote
   git remote add upstream https://github.com/original-username/amalie_projects.git

**2. Set Up Development Environment**
************************************

.. code-block:: bash

   # Navigate to documentation directory
   cd shared/docs/sphinx-site

   # Install dependencies
   pip install -r requirements.txt

   # Start development server
   make livehtml

**3. Create Feature Branch**
****************************

.. code-block:: bash

   # Create and switch to feature branch
   git checkout -b feature/your-contribution-name

   # Or for bug fixes
   git checkout -b fix/issue-description

📝 **Making Changes**
^^^^^^^^^^^^^^^^^^^^

**Documentation Structure**
***************************

Follow these guidelines when adding or modifying content:

- **File naming**: Use lowercase with hyphens (``my-new-page.rst``)
- **Folder organization**: Keep related content together in logical folders
- **Cross-references**: Link to related sections using Sphinx references
- **Consistent formatting**: Follow existing patterns for headings, lists, and code blocks

**Writing Style**
*****************

- **Tone**: Professional but approachable, first-person for personal experiences
- **Clarity**: Use clear, concise language; explain technical terms
- **Examples**: Include practical code examples with explanations
- **Structure**: Use headings, lists, and admonitions to organize content
- **Length**: Keep sections focused; break long content into multiple pages

**Code Examples**
*****************

.. code-block:: python

   # Good: Include context and explanation
   # This function calculates the accuracy of our model
   def calculate_accuracy(predictions, actual):
       """Calculate prediction accuracy as a percentage."""
       correct = sum(p == a for p, a in zip(predictions, actual))
       return (correct / len(actual)) * 100

**Technical Requirements**
**************************

- **Sphinx compatibility**: Ensure all reStructuredText syntax is valid
- **Build testing**: Run ``make html`` to verify no build errors
- **Link checking**: Use ``make linkcheck`` to verify external links
- **Mobile responsive**: Test on different screen sizes
- **Accessibility**: Include alt text for images, proper heading hierarchy

🔍 **Review Process**
^^^^^^^^^^^^^^^^^^^^

**Self-Review Checklist**
**************************

Before submitting your contribution:

.. list-table::
   :header-rows: 1
   :widths: 10 90

   * - ✓
     - Check Item
   * - ☐
     - Content is accurate and well-researched
   * - ☐
     - Writing follows the established style and tone
   * - ☐
     - Code examples are tested and properly formatted
   * - ☐
     - All links work correctly (internal and external)
   * - ☐
     - Images are optimized and have alt text
   * - ☐
     - Documentation builds without errors or warnings
   * - ☐
     - Changes are tested on mobile devices
   * - ☐
     - Commit messages are clear and descriptive

**Submitting Changes**
**********************

1. **Commit your changes**:
   
   .. code-block:: bash

      git add .
      git commit -m "Add: Clear description of your changes"

2. **Push to your fork**:
   
   .. code-block:: bash

      git push origin feature/your-contribution-name

3. **Create pull request**:
   - Go to GitHub and create a pull request
   - Use the pull request template
   - Describe your changes and motivation
   - Link any related issues

**Pull Request Guidelines**
***************************

- **Title**: Clear, descriptive title summarizing the change
- **Description**: Detailed explanation of what changed and why
- **Screenshots**: Include before/after screenshots for visual changes
- **Testing**: Describe how you tested the changes
- **Breaking changes**: Clearly note any breaking changes

🎨 **Design Guidelines**
^^^^^^^^^^^^^^^^^^^^^^^

**Visual Consistency**
**********************

- Follow the established color scheme and typography
- Use consistent spacing and alignment
- Maintain the grid system for layouts
- Ensure proper contrast ratios for accessibility

**User Experience**
*******************

- **Navigation**: Ensure clear navigation paths between sections
- **Loading**: Optimize images and minimize build output size
- **Search**: Structure content to be easily searchable
- **Mobile**: Test on various devices and screen sizes

📊 **Content Standards**
^^^^^^^^^^^^^^^^^^^^^^^

**Project Showcases**
*********************

When adding new project showcases:

- Include clear problem statement and solution approach
- Provide technical details and architecture decisions
- Add links to live demos and source code
- Explain lessons learned and future improvements
- Use consistent template structure

**Learning Content**
********************

For educational content:

- Start with clear learning objectives
- Provide step-by-step instructions
- Include troubleshooting tips
- Add practical exercises or challenges
- Link to additional resources

**Code Documentation**
**********************

- Comment code examples thoroughly
- Explain design patterns and architectural choices
- Include error handling examples
- Show both basic and advanced usage
- Keep examples up to date with latest versions

🐛 **Reporting Issues**
^^^^^^^^^^^^^^^^^^^^^^

**Bug Reports**
***************

When reporting bugs:

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** with all required information
3. **Include screenshots** for visual issues
4. **Provide reproduction steps** when possible
5. **Specify environment** (OS, browser, Python version, etc.)

**Feature Requests**
********************

For feature suggestions:

1. **Search existing requests** to avoid duplicates
2. **Describe the use case** and motivation
3. **Suggest implementation approach** if applicable
4. **Consider backwards compatibility** impact
5. **Provide examples** of similar features elsewhere

🎯 **Recognition**
^^^^^^^^^^^^^^^^^

**Contributors**
****************

All contributors are recognized in the documentation:

- Listed in the changelog for their contributions
- Mentioned in relevant sections they helped create
- Added to the contributors list in the repository
- Invited to provide feedback on future changes

**Types of Contributions**
**************************

We value all types of contributions:

- **Content creation**: New articles, tutorials, project showcases
- **Editing**: Grammar, clarity, and structure improvements  
- **Technical**: Bug fixes, performance improvements, new features
- **Design**: Visual improvements, UX enhancements
- **Community**: Helping other contributors, answering questions

📞 **Getting Help**
^^^^^^^^^^^^^^^^^^

**Support Channels**
********************

- **GitHub Issues**: For bugs, feature requests, and technical questions
- **Discussions**: For general questions and community conversation
- **Email**: For private or sensitive matters
- **Documentation**: Check the setup guide and troubleshooting section

**Response Times**
******************

- **Bug reports**: Within 48 hours
- **Pull requests**: Within 1 week for initial review
- **Feature requests**: Within 1 week for initial feedback
- **Questions**: Within 24-48 hours

---

**Thank you for contributing!** Your efforts help make this documentation better for everyone who visits and learns from it.

*Last updated: April 2026*