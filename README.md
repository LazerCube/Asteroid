#   Vesta - multiplayer asteroids game

Early development build for Vesta, a simple asteroids game.

# Requirements

*   Python 2.7      
*   Pygame

## Recently added

*   New file structure
*   Basic Debug mode(more to come!)

## Command line args

Optional arguments:
```
python main.py [-h] [-d]
```
## Branch information - Notes to myself - Current Issues

*   Need to add basic menu system.
*   Can't add state switching to button objects due to crappy state handling
*   *State Handling needs fixing*
*   Buttons need on click as well as on hold.
*   Buttons need to be able to access some low level engine functions via import. e.g. exit program
*   *Create Exit function in main.py*

##  Todo

*   Fix problems with current object class
*   Add buttons to gui
*   Implement proper debug system
*   Add code for setup.py
*   Move some variables into settings.py
*   Networking
*   Command line args
    *   Switch to argparser for command line args
    *   add more args
    *   clean up code
*   Server
*   Debug mode / gui objects
    *   Add container objects to store gui objects
    *   auto generate hitboxes for gui objects
    *   Add proper logging
    *   hover information on objects
*   Gameplay
*   Testing
*   Improve hitboxes on sprites
*   Fix hover depth issue


##  New File structure!!

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
