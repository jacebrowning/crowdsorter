# Project settings
PROJECT := CrowdSorter
PACKAGE := crowdsorter
REPOSITORY := jacebrowning/crowdsorter

# Project paths
PACKAGES := $(PACKAGE) tests
CONFIG := $(wildcard *.py)
MODULES := $(wildcard $(PACKAGE)/*.py)

# Python settings
ifndef TRAVIS
	PYTHON_MAJOR ?= 3
	PYTHON_MINOR ?= 6
endif

# System paths
PLATFORM := $(shell python -c 'import sys; print(sys.platform)')
ifneq ($(findstring win32, $(PLATFORM)), )
	WINDOWS := true
	SYS_PYTHON_DIR := C:\\Python$(PYTHON_MAJOR)$(PYTHON_MINOR)
	SYS_PYTHON := $(SYS_PYTHON_DIR)\\python.exe
	# https://bugs.launchpad.net/virtualenv/+bug/449537
	export TCL_LIBRARY=$(SYS_PYTHON_DIR)\\tcl\\tcl8.5
else
	ifneq ($(findstring darwin, $(PLATFORM)), )
		MAC := true
	else
		LINUX := true
	endif
	SYS_PYTHON := python$(PYTHON_MAJOR)
	ifdef PYTHON_MINOR
		SYS_PYTHON := $(SYS_PYTHON).$(PYTHON_MINOR)
	endif
endif

# Virtual environment paths
ifdef TRAVIS
	ENV := $(shell dirname $(shell dirname $(shell which $(SYS_PYTHON))))/
else
	ENV := env
endif
ifneq ($(findstring win32, $(PLATFORM)), )
	BIN := $(ENV)/Scripts
	ACTIVATE := $(BIN)/activate.bat
	OPEN := cmd /c start
else
	BIN := $(ENV)/bin
	ACTIVATE := . $(BIN)/activate
	ifneq ($(findstring cygwin, $(PLATFORM)), )
		OPEN := cygstart
	else
		OPEN := open
	endif
endif

# Virtual environment executables
PYTHON := $(BIN)/python
PIP := $(BIN)/pip
EASY_INSTALL := $(BIN)/easy_install
SNIFFER := $(BIN)/sniffer

# MAIN TASKS ###################################################################

.PHONY: all
all: install

.PHONY: ci
ci: check test ## Run all tasks that determine CI status

.PHONY: watch
watch: install .clean-test ## Continuously run all CI tasks when files chanage
	$(SNIFFER)

# SERVER TARGETS ###############################################################

HONCHO := $(ACTIVATE) && $(BIN)honcho

export MONGODB_URI ?= mongodb://localhost:27017/crowdsorter_dev
IP ?= $(shell ipconfig getifaddr en0 || ipconfig getifaddr en1)

.PHONY: run
run: install data
	status=1; while [ $$status -eq 1 ]; do FLASK_ENV=dev $(PYTHON) manage.py run; status=$$?; sleep 1; done

.PHONY: run-prod
run-prod: install
	FLASK_ENV=prod make data
	FLASK_ENV=prod $(HONCHO) start

.PHONY: launch
launch: install
	eval "sleep 3; open http://$(IP):5000" &
	$(MAKE) run

# SYSTEM DEPENDENCIES ##########################################################

.PHONY: doctor
doctor:  ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES #########################################################

DEPS_CI := $(ENV)/.install-ci
DEPS_DEV := $(ENV)/.install-dev
DEPS_BASE := $(ENV)/.install-base

.PHONY: install
install: $(DEPS_CI) $(DEPS_DEV) $(DEPS_BASE) ## Install all project dependencies

$(DEPS_CI): requirements/ci.txt $(PIP)
	$(PIP) install --upgrade -r $<
	@ touch $@  # flag to indicate dependencies are installed

$(DEPS_DEV): requirements/dev.txt $(PIP)
	$(PIP) install --upgrade -r $<
ifdef WINDOWS
	@ echo "Manually install pywin32: https://sourceforge.net/projects/pywin32/files/pywin32"
else ifdef MAC
	$(PIP) install --upgrade pync MacFSEvents
else ifdef LINUX
	$(PIP) install --upgrade pyinotify
endif
	@ touch $@  # flag to indicate dependencies are installed

$(DEPS_BASE): requirements.txt $(PYTHON)
	$(PIP) install --upgrade -r $<
	@ touch $@  # flag to indicate dependencies are installed

$(PIP): $(PYTHON)
	$(PYTHON) -m pip install --upgrade pip
	@ touch $@

$(PYTHON):
	$(SYS_PYTHON) -m venv $(ENV)

# DATA GENERATION ##############################################################

.PHONY: data
ifdef VIRTUAL_ENV
data:
	scripts/generate_sample_data.py
else
data: install
	PYTHONPATH=. source env/bin/activate && scripts/generate_sample_data.py
endif

# CHECKS #######################################################################

PYLINT := $(BIN)/pylint
PYCODESTYLE := $(BIN)/pycodestyle
PYDOCSTYLE := $(BIN)/pydocstyle

.PHONY: check
check: pycodestyle pydocstyle ## Run linters and static analysis

.PHONY: pylint
pylint: install
	$(PYLINT) $(PACKAGES) $(CONFIG) --rcfile=.pylint.ini

.PHONY: pycodestyle
pycodestyle: install
	$(PYCODESTYLE) $(PACKAGES) $(CONFIG) --config=.pycodestyle.ini

.PHONY: pydocstyle
pydocstyle: install
	$(PYDOCSTYLE) $(PACKAGES) $(CONFIG)

# TESTS ########################################################################

PYTEST := FLASK_ENV=test $(BIN)/py.test
COVERAGE := $(BIN)/coverage
COVERAGE_SPACE := $(BIN)/coverage.space

RANDOM_SEED ?= $(shell date +%s)

PYTEST_CORE_OPTS := -ra -vv
PYTEST_COV_OPTS := --cov=$(PACKAGE) --no-cov-on-fail --cov-report=term-missing:skip-covered --cov-report=html
PYTEST_RANDOM_OPTS := --random --random-seed=$(RANDOM_SEED)

PYTEST_OPTS := $(PYTEST_CORE_OPTS) $(PYTEST_COV_OPTS) $(PYTEST_RANDOM_OPTS)
PYTEST_OPTS_FAILFAST := $(PYTEST_OPTS) --last-failed --exitfirst

FAILURES := .cache/v/cache/lastfailed
REPORTS ?= xmlreport

.PHONY: test
test: test-all ## Run unit and integration tests

.PHONY: test-unit
test-unit: install
	@- mv $(FAILURES) $(FAILURES).bak
	$(PYTEST) $(PYTEST_OPTS) $(PACKAGE) --junitxml=$(REPORTS)/unit.xml
	@- mv $(FAILURES).bak $(FAILURES)
	$(COVERAGE_SPACE) $(REPOSITORY) unit

.PHONY: test-int
test-int: install
	@ if test -e $(FAILURES); then $(PYTEST) $(PYTEST_OPTS_FAILFAST) tests; fi
	@ rm -rf $(FAILURES)
	$(PYTEST) $(PYTEST_OPTS) tests --junitxml=$(REPORTS)/integration.xml
	$(COVERAGE_SPACE) $(REPOSITORY) integration

.PHONY: test-all
test-all: install
	@ if test -e $(FAILURES); then $(PYTEST) $(PYTEST_OPTS_FAILFAST) $(PACKAGES); fi
	@ rm -rf $(FAILURES)
	$(PYTEST) $(PYTEST_OPTS) $(PACKAGES) --junitxml=$(REPORTS)/overall.xml
	$(COVERAGE_SPACE) $(REPOSITORY) overall

.PHONY: read-coverage
read-coverage:
	$(OPEN) htmlcov/index.html

# DOCUMENTATION ################################################################

.PHONY: doc
doc:  ## Generate documentation

# CLEANUP ######################################################################

.PHONY: clean
clean: .clean-dist .clean-test .clean-doc .clean-build ## Delete all generated and temporary files

.PHONY: clean-all
clean-all: clean .clean-env .clean-workspace

.PHONY: .clean-build
.clean-build:
	find $(PACKAGES) -name '*.pyc' -delete
	find $(PACKAGES) -name '__pycache__' -delete
	rm -rf *.egg-info

.PHONY: .clean-doc
.clean-doc:
	rm -rf README.rst docs/apidocs *.html docs/*.png site

.PHONY: .clean-test
.clean-test:
	rm -rf .cache .pytest .coverage htmlcov xmlreport

.PHONY: .clean-dist
.clean-dist:
	rm -rf *.spec dist build

.PHONY: .clean-env
.clean-env: clean
	rm -rf $(ENV)

.PHONY: .clean-workspace
.clean-workspace:
	rm -rf *.sublime-workspace

# HELP #########################################################################

.PHONY: help
help: all
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
