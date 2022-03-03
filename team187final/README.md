# Team 187 CSE 6242 Project
## Description
  This package contains NBA shot data, examples of experiments run in Python and R, persisted models in the form of pickle files, and files needed to support the web browser based interactive visualization. The goal of this package is to allow for an end user to interact with a state of the art predictive model without the need for additional software. The visualization is built on top of a basketball court SVG built from geoJSON and it presents the user with two moveable nodes - one representing an offensive player and one representing a defensive player. A user can move nodes, or update one of the non-spatial features represented below the court in order to make predictions on trained models. The output is a probablisitic measure of the quality of the shot. Our models were trained on more than 200,000 shots taken from 2014 to 2016 in the NBA and achieved up to 65.9% accuracy measured through 10 fold cross validation. The end user can choose between multiple types of trained models, and can interact with those models in real-time to build intuition regarding how various features of a shot affect the outcome.
  We leveraged Pyodide to make a Python environment available within the web browser to facilitate our interaction with trained models. D3 is used to project the basketball court onto an SVG, and is reponsible for the moveable nodes and lines between nodes. We used HTML to create the user interface representing the model output, non-spatial features, and types of models below the court.

## Installation
- You will need to install an http web server to run the web browser based visualization. We suggest Python's http.server in the Python Standard Library.
- To continue with experiments, you will need Python and/or R installed. 

## Execution
- To continue with experiments, you can load data in the form of csv's from the data folder structure, and you can then leverage any Python or R package for stastical analysis or visualization.
- Visit our GitHub Pages at https://github.gatech.edu/pages/rcurran7/CSE6242-Project/ to view the visualization.
- Or to run the web based visualization locally:
  - Start an http server in the code/visuals directory.
  - Open your web browser (Chrome or Firefox) and navigate to localhost:port.
  - The web page will begin loading the embedded python environment and necessary packages.
  - Once the page has finished loading, you will see a basketball court with moveable nodes that represent an offensive player and defensive player

## Demo Video
https://youtu.be/a68ItIzAN8U

## Known Issues
- When running the visualization locally, you may encounter errors in the console such as "cannot convert string to float" and "invalid literal for int() with base 10: '1L\r\n'. These are being thrown by the call to pickle.loads(). You can always visit 
