# ShinyDetector
The odds of a shiny starter in brilliant diamond and shining pearl is ~ 1/4100 so I automated the process of looking for one while I went to class using the following pseudocode:

1. Simulates keyboard inputs with specific timing to walk through intro and begin starter pokemon battle

2. Uses camera to take a photo and check for certain colour ranges(shiny pokemon colour) using the CV2 library.

3. Based on photo taken, restart the switch and try again or shutdown program

# Required 
- a bluetooth switch controller emulator to send inputs (i used [nxbt](https://github.com/Brikwerk/nxbt))
- webcam setup to monitor the switch screen
