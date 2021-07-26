==========================
Start guide (with docker):
==========================

    #. Pull API ``git clone https://github.com/Home-warehouse/warehouse-api.git``
    #. Pull UI ``git clone https://github.com/Home-warehouse/warehouse-ui.git``
    #. Edit ``./warehouse-api/.env`` and ``./warehouse-ui/src/environments/environment.prod.ts``
    #. Go to ``./warehouse-api/docker/`` directory and edit .env file
    #. In the same directory run both ``docker-compose build`` and ``docker-compose up -d``
    #. Access HomeWarehouse from web browser under given host