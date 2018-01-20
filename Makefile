
BUILD_DIR = .venv
OUTPUT_DIR = _website
SPHINX_DIR = .doctrees
ASCIINEMA_DIR = .asciinema

SPELLING_CMD = $(BUILD_DIR)/bin/sphinx-build -Q -b spelling -d .doctrees .
SPELLING_OUT_DIR = build/spelling
.DEFAULT_GOAL := help

.PHONY: remove clean build_dir build spelling start stop test


help:              ## Show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

remove:            ## Remove the build dir and all output.
	@rm -rf $(OUTPUT_DIR) $(BUILD_DIR) $(SPHINX_DIR) $(SPELLING_OUT_DIR) $(ASCIINEMA_DIR)
	@echo "===MAKE: Removed everything."

clean:             ## Clean the built blog output.
	@./scripts/remove_build_artifacts.sh

build_dir:         ## Create the build directory and install the dependencies.
	@./scripts/create_build_env.sh

build:             ## Build the blog sources.
	@$(BUILD_DIR)/bin/ablog build
	@echo "===MAKE: Built the blog sources."

spelling:          ## Check the spelling of the posts.
	@rm -rf build
	@$(SPELLING_CMD) $(SPELLING_OUT_DIR)
	# Show me all the spelling findings
	@cat $(SPELLING_OUT_DIR)/output.txt
	@rm -rf build
	@echo "===MAKE: Checked the spelling."

start:             ## Start the local server to serve the blog.
	@$(BUILD_DIR)/bin/ablog serve -r >/dev/null 2>&1 &
	@echo "===MAKE: Started the server."

stop:              ## Stop the local server.
	@pkill ablog; if [ $$? -eq 1 ] ; then echo "Already stopped." ; fi
	@echo "===MAKE: Stopped the server."

install_apt_deps:  ## Install the Ubuntu (*.deb) OS packages needed.
	@apt-get -qq update
	@apt-get install -y python-enchant  # for pypi package sphinxcontrib-spelling
	@apt-get install -y graphviz        # for sphinx directive graphviz
	@echo "===MAKE: Installed the deb OS packages."

install_rpm_deps:  ## Install the CentOS (*.rpm) OS packages needed.
	@yum install -y python-enchant  # for pypi package sphinxcontrib-spelling
	@yum install -y graphviz        # for sphinx directive graphviz
	@echo "===MAKE: Installed the rpm OS packages."

test:              ## Test for common mistakes.
	# Test for sorted spelling word list
	@sort -c spelling_wordlist.txt
	# Test for too long URLs
	@./scripts/test_url_lengths.sh
	# Test for spelling mistakes
	@$(SPELLING_CMD) $(SPELLING_OUT_DIR)
	@if [ -s $(SPELLING_OUT_DIR)/output.txt ] ; then cat $(SPELLING_OUT_DIR)/output.txt && exit 1 ; fi
	@echo "===MAKE: Checked for common mistakes."
