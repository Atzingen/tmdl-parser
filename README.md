<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
    <img src="images/parser_image.webp" alt="Logo" width="80" height="80">

  <h3 align="center">TMDLParser</h3>

  <p align="center">
    A Python library designed to parse and process TMDL (Table Metadata Description Language) files
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
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
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project


**TMDLParser** is a Python library designed to parse and process TMDL (Table Metadata Description Language) files. It provides a structured way to handle data descriptions, properties, and calculations with an easy-to-use API.

- Parses TMDL files into structured Python objects.
- Handles multiple levels of nested properties.
- Supports detailed descriptions, elements, properties, and calculations.
- Easily integrates with other Python applications.
- Lightweight and easy to install.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Install the library directly from PyPI:

```bash
pip install tmdl-parser
```

### Prerequisites

python>=3.10
Library uses only standart library and no 3th party.

<!-- USAGE EXAMPLES -->
## Usage

### Basic Example

```python
from tmdlparser import TMLDParser

# Initialize the parser with a TMDL file path
parser = TMLDParser("path/to/tmdl/file.tmdl")

# Print the parsed structure
print(parser)
```

Results:

```bash
Description: Table Description
Element: Table Name
Properties:
    ----------
    Description: Column Description
    Element: Column Name
    Props: ['property_1', 'property_2']
    Calcs: ['calculation_1']
Calculation: ['Calculation Formula']
--------------------
```



<!-- ROADMAP -->
## Roadmap

* [ ] Publish to pip
* [ ] Create tests
* [ ] Better return format for parsed files

See the [open issues](https://github.com/Atzingen/tmdl-parser/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact


Project Link: [https://github.com/Atzingen/tmdl-parser](https://github.com/Atzingen/tmdl-parser)

gustavo.von.atzingen@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Atzingen/tmdl-parser.svg?style=for-the-badge
[contributors-url]: https://github.com/Atzingen/tmdl-parser/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Atzingen/tmdl-parser.svg?style=for-the-badge
[forks-url]: https://github.com/Atzingen/tmdl-parser/network/members
[stars-shield]: https://img.shields.io/github/stars/Atzingen/tmdl-parser.svg?style=for-the-badge
[stars-url]: https://github.com/Atzingen/tmdl-parser/stargazers
[issues-shield]: https://img.shields.io/github/issues/Atzingen/tmdl-parser.svg?style=for-the-badge
[issues-url]: https://github.com/Atzingen/tmdl-parser/issues
[license-shield]: https://img.shields.io/github/license/Atzingen/tmdl-parser.svg?style=for-the-badge
[license-url]: https://github.com/Atzingen/tmdl-parser/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[product-screenshot]: images/screenshot.png
