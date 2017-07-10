#!/usr/bin/env make -f
# -*- makefile -*-
#
# This makefile builds RPM packages for Campaign and Publisher management
# components. Examples:
#
#    make rpm  -  build RPM packages for all supported components
#    make azkaban-executor azkaban-web azkaban-solo  - build RPMs for selected services
#


# Path to source code
WORKSPACE ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST))))

# Path to build a directory where packages are built
BUILDSPACE ?= $(WORKSPACE)/.tmp

#################################################################################

# Setup shell program explicitly, bash specific is used further
SHELL := /bin/bash

# Path to directories with RPM specifications for services
SPECDIR := rpm/

#################################################################################
##
#################################################################################


# Build RPM packages for selected maven modules
%: %.rpm
	@echo Build phase for $* has been completed successfully

# Build all modules of this maven project
build:
	pushd $(WORKSPACE)/azkaban; \
	    ./gradlew installDist; \
	popd

clean: clean-rpm
	pushd $(WORKSPACE)/azkaban; \
	    ./gradlew clean; \
	popd

# Build RPM packages for all supported services
rpm: PACKAGES := $(subst $(SPECDIR),,$(shell find $(SPECDIR) -mindepth 1 -type d)) 
rpm: $(addsuffix .rpm,$(PACKAGES))

# Compose version and build RPM package for a component
 %.rpm: RPMV := $(shell $(WORKSPACE)/version cr_git)
%.rpm: $(WORKSPACE)/$(SPECDIR)%/service.spec
	@mkdir -p $(BUILDSPACE)/{BUILD,RPMS,SPECS,SRPMS}
	rpmbuild -D "_topdir $(BUILDSPACE)" -D "_sourcedir $(WORKSPACE)" \
		 -D "_version $(RPMV)" \
                 -bb $<
#-D "_release $(word 2, $(RPMV))" \
#-D "_version $(word 1, $(RPMV))" \

clean-rpm:
	@rm -rf $(BUILDSPACE)/{BUILD,BUILDROOT,RPMS,SPECS,SRPMS}

