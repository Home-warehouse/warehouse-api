==========================
Start guide (with docker):
==========================

#. Pull API ``git clone https://github.com/Home-warehouse/warehouse-api.git``
#. Pull UI ``git clone https://github.com/Home-warehouse/warehouse-ui.git``
#. Move ``./warehouse-api/.env.prod`` to ``./warehouse-api/.env``
#. Edit  ``./warehouse-api/.env`` and ``./warehouse-ui/src/environments/environment.prod.ts``
#. Go to ``./warehouse-api/docker/`` directory and edit .env file
#. In the same directory run both ``docker-compose build`` and ``docker-compose up -d``
#. Access HomeWarehouse from web browser under given host

===========
Development
===========

It is recommended to use tool `Poetry
<https://python-poetry.org/>`_ with python 3.9


-----------
With poetry
-----------
#. Pull repository to desired directory
#. Run ``poetry install``
#. Copy ``./warehouse-api/.env.prod`` to ``./warehouse-api/.env`` and edit to match your requirements
#. From repository directory run ``poetry run python home_warehouse_api/main.py``

--------------
Without poetry
--------------
#. Setup python for version 3.9
#. Pull repository to desired directory
#. Install packages from requirements file
#. Copy ``./warehouse-api/.env.prod`` to ``./warehouse-api/.env`` and edit to match your requirements
#. From repository directory run ``poetry run python home_warehouse_api/main.py``


-------
Testing
-------
#. Make sure you have installed API with steps listed before.
#. While tesiting export path for API files ``export PYTHONPATH=home_warehouse_api``
#. Run command with poetry ``poetry run pytest`` or without poetry ``pytest``


**Take part in development! 😊**