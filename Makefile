prod:
	- ( \
	  docker-compose  -f docker-compose.yml up --build redis rabbitmq flask webserver \
    )


removetest:
	- ( \
       docker rmi -f tests;\
    )
  
remove:
	- ( \
        docker-compose stop;\
        docker-compose down; \
        docker volume prune; \
        docker image prune; \
        )
        
test:
	- ( \
       .  build/bin/activate; \
	   FLASK_APP=autoapp flask test;\
       docker-compose stop testerabbitmq testeredis; \
    )

install:
	- virtualenv -p python3.8 ../desafio-cortex/build
	- ( \
        .  build/bin/activate; \
        pip3 install -r requirements.txt; \
    )

run:
	- ( \
       .  build/bin/activate; \
	   FLASK_APP=autoapp   FLASK_DEBUG=true flask run\
    )

workers:
	- ( \
       .  build/bin/activate; \
	   docker-compose run flask sh -c 'FLASK_APP=autoapp   FLASK_DEBUG=true flask init-workers;'\
    )
