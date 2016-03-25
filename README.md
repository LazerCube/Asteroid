#   Vesta - multiplayer asteroids game

Early development build for Vesta

New File structure!!

```
Asteroid/
|-- bin
|   |-- main.py
|   |-- settings.py
|   |-- world.py
|   |-- utilites/
|   |   |-- __init__.py
|   |   |-- util.py
|   |   
|   |--objects/
|       |-- __init__.py
|       |-- objects.py
|       |--gui/
|       |   |-- __init__.py
|       |   |-- button.py
|       |   |-- label.py
|       |
|       |-- sprite/
|       |   |-- __init__.py
|       |   |-- playership.py
|
|-- vesta/
|   |--test/
|   |   |-- __init__.py
|   |   |-- __test_main.py
|   |       
|   |-- __init__.py
|   |-- run.py
|   
|-- setup.py
|-- README.md
|-- .gitignore

```

##  Todo

*   Fix problems with current object class
*   Add buttons to gui
*   Implement proper debug system
*   Add code for setup.py
*   Move some variables into settings.py
*   Netwoking
*   Server
*   Gameplay
*   Testing
*   Improve hitboxes on sprites
*   Fix hover depth issue
