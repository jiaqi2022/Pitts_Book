# PittsBook Documentation
The project aims to connect consumers with Pittsburgh’s tourist attractions and surrounding restaurants with security information to provide a better travel experience.

Group Members:
Name: Veronica Wang   AndrewID: yujiewan
Name: Qi Zheng        AndrewID: qzheng2
Name: Jiaqi Li        AndrewID: jiaqil4
Name: Yi Zhou         AndrewID: yzhou7


## Functionality
The PittsBook project supports three functions: 

1. Recommend restaurants in Pittsburgh according to below three categories:
    * Different cuisine types;
    * Previous customers’ ratings on yelp from highest to lowest;
    * Different districts.

2. Recommend attraction tourisms in Pittsburgh according below two modes:
    * Specific region selected by users;
    * Random region randomly selected.

3. Provide the safety information of the relevant areas: connect Google map API to mark the places where incidents occurred on the map in the past month


## Installation
You can use Anaconda3 or VsCode to run the project.

### Anaconda3:
* The version of Anaconda should be Anaconda3-2022.05-Windows- 64.
* After launching Spyder 5.1.5, click ‘Projects’ and then click ‘open project’ and open the directory where you download our project. If it prompts it is not a Spyder project, you should first create a Spyder project and copy the .spyproject folder of the Spyder project created by yourself to the folder where downloaded our project and then try to open our project again.
* In the terminal, enter ‘pip install googlemaps’ and ‘pip install gmplot’.
* driver.py file is the main program file. Run driver.py to launch the project.

### Visual Studio Code:
* You should first execute the below commands in the terminal to install the modules:
        pip3 install lxml parser library gmplot googlemaps pandas numpy requests bs4    
* Then you can run the main program driver.py from the terminal:
        python3 driver.py


## Video Demonstration 
Here is the link of a short video demonstrating our project being run: https://youtu.be/WaIlgiN38CI
