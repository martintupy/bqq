build:
	sh bin/build.sh

container:
	docker run --rm -it bqq bash

format:
	autoflake --in-place --remove-all-unused-imports bqq/**/*.py
	black .