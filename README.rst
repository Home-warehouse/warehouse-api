==============
How to install
==============

----------------------------------------------------------------------
With `docker <https://docs.docker.com/engine/install/>`_ (recommended)
----------------------------------------------------------------------
- Linux/macOS

  #. Run from terminal: ``bash <(curl -s https://raw.githubusercontent.com/Home-warehouse/warehouse-api/master/install_nix.sh) './hw' 'v0.3.2-alpha' 'localhost' 5001 5000``
  #. Go to http://localhost:5000/
  #. Login to admin account, email: ``home-warehouse@mail.com``; password: ``home-warehouse-supervisor`` and change account data

- Windows

  #. Run from PowerShell: ``Invoke-WebRequest https://raw.githubusercontent.com/Home-warehouse/warehouse-api/master/install_windows.ps1 -OutFile .\install_windows.ps1; .\install_windows.ps1 './hw' 'v0.3.2-alpha' 'localhost' 5001 5000``
  #. Go to http://localhost:5000/
  #. Login to admin account, email: ``home-warehouse@mail.com``; password: ``home-warehouse-supervisor`` and change account data

**Use evernote integration**

#. Generate evernote `developer token <https://sandbox.evernote.com/api/DeveloperToken.action>`_
#. Set generated token as system env var on Linux/macOS: ``export EVERNOTE_TOKEN="<token goes here>"``
#. Set generated token as system env var on Windows: ``$Env:EVERNOTE_TOKEN="<token goes here>"``
#. Run installation script

--------------------------------
Standalone (Advanced)
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
#. Go to http://localhost:5000/
#. Login to admin account, email: ``home-warehouse@mail.com``; password: ``home-warehouse-supervisor`` and change account data


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