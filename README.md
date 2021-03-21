<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project automates the collection of API data that can be used for machine learning.
It's primary source is Spotify track and artist data. Since the recently played tracks for
a user are limited to 50 tracks, it is necessary to regularly pull the data and store it
in a Postgres database.

There is also a simple API call to get Google forms survey data to correlate with the
Spotify data. Over time, even more API calls will be added.



### Built With

* [Python](https://www.python.org/)
* [Spotipy](https://spotipy.readthedocs.io/en/2.17.1/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.



### Prerequisites

The requirements.txt file can be used to install all dependencies for the project.
Make sure to create a virtual environment before installing the requirements file.
See here for further instructions: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/SteamedHams722/automatic-octopus.git
   ```
2. ``sh
    Create a Spotify account: https://www.spotify.com/us/signup/
    ```



<!-- USAGE EXAMPLES -->
## Usage

The primary use case for this project is to pull a user's recently played tracks in
Spotify and store it in a Postgres database. Overtime, connections to additional APIs
will be added.

_For more examples, please refer to the [Documentation](https://example.com)_



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/SteamedHams722/automatic-octopus) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE` for more information.



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Automate the Boring Stuff with Python](https://automatetheboringstuff.com/)
* [Python Crash Course](https://nostarch.com/pythoncrashcourse2e)
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)