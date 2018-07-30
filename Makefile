PACKAGE_NAME = "AdaGardenController.zip"
PACKAGE_PATH = "${CURDIR}/${PACKAGE_NAME}"

.PHONY: package
ifeq (package,$(firstword $(MAKECMDGOALS)))
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif

package: ## lambda package : ## make package
	@echo -e "${PACKAGE_PATH}"
	@echo "===> cleaning... " && \
	rm -f $(PACKAGE_PATH)
	@echo "===> package creating... " && \
	zip -r9 $(PACKAGE_PATH) lambda_function.py && \
	(cd venv/lib/python3.7/site-packages && zip $(PACKAGE_PATH) -r9 .)
	@echo "===> package created "

deploy: ## deploy : ## deploy with terraform
	(cd terraform && terraform apply -auto-approve)

.PHONY: help
help: ## Show this help message : ## make help
	@echo -e "\nUsage: make [command] [args]\n"

.DEFAULT_GOAL := help
