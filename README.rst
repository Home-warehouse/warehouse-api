==============
How to install
==============

----------------------------------------------------------------------
With `docker <https://docs.docker.com/engine/install/>`_ (recommended)
----------------------------------------------------------------------

-----------------------------
Installation Scripts (docker)
-----------------------------
- Linux/macOS

  #. Run from terminal: ``bash <(curl -s https://raw.githubusercontent.com/Home-warehouse/warehouse-api/master/install_nix.sh) 'v0.3.4-alpha' 'localhost'``
  #. Go to http://localhost:8000/
  #. See home-warehouse logs to copy generated password
  #. Login to admin account with email: ``home-warehouse@mail.com`` and generated password, after it, it is advised to change account password

- Windows

  #. Run from PowerShell: ``Invoke-WebRequest https://raw.githubusercontent.com/Home-warehouse/warehouse-api/master/install_windows.ps1 -OutFile .\install_windows.ps1; .\install_windows.ps1 'v0.3.4-alpha' 'localhost'``
  #. Go to http://localhost:8000/
  #. See home-warehouse logs to copy generated password
  #. Login to admin account with email: ``home-warehouse@mail.com`` and generated password, after it, it is advised to change account password

--------------
Docker Compose
--------------
1. Create docker-compose.yml file
::
  version: "3.0"
  services:
    home-warehouse:
      container_name: home-warehouse
      build: 
        context: ../../
        dockerfile: home-warehouse-api/dockerfile
      hostname: home-warehouse
      ports:
        - 8000:8000
      networks:
        - home_warehouse_be

    mongo-home-warehouse:
      container_name: home-warehouse-db
      hostname: mongo-home-warehouse
      image: mongo:latest
      volumes:
        - home_warehouse_db:/data/db
      networks:
        - home_warehouse_be

  networks:
    home_warehouse_be:

  volumes:
    home_warehouse_db:

2. Go to http://localhost:8000/
3. See home-warehouse logs to copy generated password
4. Login to admin account with email: ``home-warehouse@mail.com`` and generated password, after it, it is advised to change account password



**Use evernote integration**

#. Generate evernote `developer token <https://sandbox.evernote.com/api/DeveloperToken.action>`_
#. Set generated token as system env var on Linux/macOS: ``export EVERNOTE_TOKEN="<token goes here>"``
#. Set generated token as system env var on Windows: ``$Env:EVERNOTE_TOKEN="<token goes here>"``
#. Run installation script

--------------------------------
Standalone - without docker (Advanced)
--------------------------------
#. Install git, node, python3.9, nginx, mongoDB
#. Git clone ``https://github.com/Home-warehouse/warehouse-api`` to 'home-warehouse-api'
#. Install requirements.txt in 'home-warehouse-api'
#. Edit home-warehouse-api/.env
#. Run ``python3 home_warehouse_api/main.py``
#. Git clone ``https://github.com/Home-warehouse/warehouse-ui`` to 'home-warehouse-ui'
#. Edit home-warehouse-ui/environments/environment.prod.ts
#. Install dependencies ``npm install``
#. Build UI ``npm run build``
#. Setup nginx server (example config is in ``home-warehouse-ui/nginx``)
#. Move files from ``dist`` directory to nginx hosted files directory
#. Go to http://localhost:8000/
#. See home-warehouse logs to copy generated password
#. Login to admin account with email: ``home-warehouse@mail.com`` and generated password, after it, it is advised to change account password


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