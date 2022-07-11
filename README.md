<h1 align="center">Welcome to Reckon Audit Log Download 👋</h1>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
</p>

> A simple bot designed to automatically download Audit Log from Reckon.

## Prerequisite

Python 3.10
pipenv
pyinstaller
selenium

## Build sript

```sh
pyinstaller ./main.py --onefile --noconsole --add-binary "./src/chromedriver.exe;./driver"
```

## Usage

Download the .exe file in the release channel\
Make sure the meta_data.json is in the same directory as the .exe file\
Fill in your username & password for Reckon and the starting position of the calendar

## Screenshots

![Screenshot for meta_data.json](./src//screenshot.PNG)

## Author

👤 **EpicPants**

- Github: [@EpicPant](https://github.com/EpicPant)

## Show your support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
