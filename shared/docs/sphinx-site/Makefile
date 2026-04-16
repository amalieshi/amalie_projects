# Minimal makefile for Sphinx documentation

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD  ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile setup-external-docs

# Setup external documentation before building
setup-external-docs:
	@echo "🔧 Setting up external documentation..."
	@python setup_external_docs.py

# Development server with auto-reload
livehtml: setup-external-docs
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O) \
		--host 0.0.0.0 \
		--port 8000 \
		--watch ../../../ \
		--ignore "*.git/*" \
		--ignore "*/__pycache__/*" \
		--ignore "*/build/*" \
		--open-browser

# Clean build with link checking
clean-build: setup-external-docs
	@make clean
	@make html
	@make linkcheck

# Quick development build
dev: setup-external-docs
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" -W --keep-going

# Production build with strict checking
production: setup-external-docs
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" -W -E -a --keep-going
	@echo "Production build complete. Files in $(BUILDDIR)/html"

# Check for common issues
check:
	@echo "Running documentation checks..."
	@doc8 "$(SOURCEDIR)" --max-line-length 100
	@rstcheck -r "$(SOURCEDIR)"
	@echo "Documentation checks passed!"

# Install development dependencies
install-dev:
	@pip install -e ".[dev,enhanced,quality]"
	@echo "Development dependencies installed!"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile setup-external-docs
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)