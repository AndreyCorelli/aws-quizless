.PHONY : start stop

start:
		docker-compose up -d

stop:
		docker-compose down

test:
		cd src && python -m pytest tests