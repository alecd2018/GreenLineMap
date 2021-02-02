



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/alecdean/green-line-map">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Green Line Map</h3>

  <p align="center">
    A RaspberryPi project that displays a live visualization of trains on Boston's MBTA Green Line.
    <br />
    <br />
    <a href="https://github.com/alecdean/green-line-map">View Demo</a>
  </p>
</p>

- [About The Project](#about-the-project)
  - [Built With](#built-with)
    - [Hardware](#hardware)
    - [Software](#software)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)


<!-- ABOUT THE PROJECT -->
## About The Project


This project uses a RaspberryPi computer to pull live train data from the MBTA's API, and display it on a set of LED lights. Currently, the project is configured to display *only* the Green Line C route. See the video above for its various modes. Using a button, a user can alternate between the following modes:
* Trains (default): displays live train locations on the Green Line.
* Party: Showcases the usage of the WS2812B lights by playing with the colors
* Off: Pauses the program until another button press

Follow the steps below for cloning and running a local copy.

### Built With

#### Hardware
* [RaspberryPi 4B]()
* [WS2812B individually addressable LED strip]()
* Custom wood frame

#### Software
* [Anaconda Python](https://docs.conda.io/en/latest/miniconda.html)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps. *Note*: the following steps are for running a local demo of the live map *without* the RaspberryPi and LEDs. Since the LED's require an extra library, please use the **demo** branch for this section.

The following instructions were tested and executed on Ubuntu Linux, and they may differ for different OS's.

### Prerequisites

This project requires the following software:
- [Anaconda](https://www.anaconda.com/): I used [miniconda](https://docs.conda.io/en/latest/miniconda.html).


### Installation

Copy and paste the following script into your terminal to run the installation.
  ```sh
  # Clone the repo
  git clone https://github.com/alecdean/green-line-map.git
  cd green-line-map

  # Create and launch virtual conda environment
  conda create -n mbta python=3.7
  conda activate mbta

  # Install dependent libraries
  pip install flask requests
  ```


<!-- USAGE EXAMPLES -->
## Usage

To run a local copy *with no LED lights*, run the following:

```
conda activate mbta
sudo <PATH_TO_MINICONDA_INSTALLATION>/envs/mbta/bin/python src/main.py
```

While in use, you can pause and resume the program via a Flask web server. Go to *localhost:8080/toggle/off* to pause the prgoram, and go to *localhost:8080/toggle/on* to resume it.

To stop the program, press **Ctrl+C** twice. Once to stop the trains thread and the other to stop the flask server thread.


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

The idea for this project was borrowed from [idreyn's mbta-realtime-led project](https://github.com/idreyn/mbta-realtime-led)