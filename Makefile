.PHONY:
.ONESHELL:
SHELL := /bin/bash
CompEtyma :=

##include Makefile.d/Makefile-docker Makefile.d/Makefile-test Makefile.d/Makefile-devutil

##include Makefile.d/*.mk


run-dev:
	cd schema ; ./schematone.sh ; cd ..
	kill `lsof -t -i:5000`
	python3 app.py

git-subtree-add-burn:
	git subtree add --prefix burn --squash ssh://git@gitlab.rawstonedu.net:10022/sculptor/burn-xk-ms.git develop

add-meta-data:
	git subtree add --prefix meta-data --squash ssh://git@gitlab.rawstonedu.net:10022/sculptor/meta-data-xk.git develop

update-meta-data:
	git subtree pull --prefix meta-data --squash ssh://git@gitlab.rawstonedu.net:10022/sculptor/meta-data-xk.git develop
