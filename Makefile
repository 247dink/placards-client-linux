DOCKER_COMPOSE=docker compose


build:
	${DOCKER_COMPOSE} build


# --security-opt seccomp=unconfined
# --security-opt seccomp=chrome.json
run:
	${DOCKER_COMPOSE} up

#	docker run -ti \
		   -v /tmp/.X11-unix:/tmp/.X11-unix \
		   -v ./d_sign_client:/app/d_sign_client:ro \
		   -v ./docker/entrypoint.sh:/entrypoint.sh:ro \
		   --network host \
		   --security-opt seccomp=unconfined \
		   -e DISPLAY=${DISPLAY} d-sign-client


test:
	pipenv run python3 -m unittest tests/*
