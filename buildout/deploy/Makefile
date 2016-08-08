REQUIREMENTS_TIMESTAMP := ./requirements.timestamp

.PHONY: all
all: requirements


.PHONY: install-staging
install-staging:
	ansible-playbook -i inventories/staging site.yml


.PHONY: update-staging
update-staging:
	ansible-playbook -i inventories/staging site.yml --tags=update


.PHONY: requirements
requirements: $(REQUIREMENTS_TIMESTAMP)


$(REQUIREMENTS_TIMESTAMP): requirements.txt
	@echo "Installing pre-requirements..."
	pip install -r requirements.txt | grep --line-buffered -v '^   '
	ansible-galaxy install -p roles ANXS.postgresql
	@touch $@
