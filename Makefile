up:
	docker compose -f compose.dev.yaml up --build -d bot_tgc
down:
	docker compose -f compose.dev.yaml down
restart:
	docker compose -f compose.dev.yaml restart
bot:
	docker exec -it bot_tgc bash
