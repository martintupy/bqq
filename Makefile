build:
	sh bin/build.sh

format:
	autoflake --in-place --remove-all-unused-imports bqq/**/*.py
	black .