CONFIG_ENV=default
DEPLOY_OPTS=

STACK_NAME=cfn-api-tracer
SAM_CONFIG_FILE=samconfig.toml

.PHONY: default
default: deploy

.PHONY: deploy
deploy:
	( \
		sam build && \
		sam deploy \
			--stack-name $(STACK_NAME) \
			--config-env $(CONFIG_ENV) \
			$(DEPLOY_OPTS) \
	)
