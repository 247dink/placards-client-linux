DOCKER_COMPOSE=docker compose
XAUTH_COOKIE := $(shell xauth list | head -n 1 | awk ' { print $$3 } ')


.venv: Pipfile.lock
	PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
	touch .venv


.PHONY: image
image:
	${DOCKER_COMPOSE} build


# --security-opt seccomp=unconfined
# --security-opt seccomp=chrome.json
run:
	XAUTH_COOKIE=${XAUTH_COOKIE} ${DOCKER_COMPOSE} up

#	docker run -ti \
		   -v /tmp/.X11-unix:/tmp/.X11-unix \
		   -v ./d_sign_client:/app/d_sign_client:ro \
		   -v ./docker/entrypoint.sh:/entrypoint.sh:ro \
		   --network host \
		   --security-opt seccomp=unconfined \
		   -e DISPLAY=${DISPLAY} d-sign-client


bump: .venv
	pipenv run bumpversion patch


package: .venv
	pipenv run python3 -m build --wheel


publish: .venv
	pipenv run twine upload dist/*


lint: .venv
	pipenv run flake8 placards


test: .venv
	pipenv run python3 -m unittest tests/*


ci: test lint


clean:
	rm -rf *.egg-info dist build
