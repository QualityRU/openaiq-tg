run:
	docker run -it -d --env-file .env --restart=unless-stopped --name openaiq_bot openaiq_bot_image
stop:
	docker stop openaiq_bot
attach:
	docker attach openaiq_bot
dell:
	docker rm eopenaiq_bot