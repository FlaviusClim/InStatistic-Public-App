# InStatistic

InStatistic is a simple application developed in Python using the Streamlit library, which provides useful information about Instagram profiles.

## Description

This application allows you to obtain detailed information about a specific Instagram profile, including the number of followers, the number of posts, the biography, the most used hashtags, and more. It also provides an analysis of user engagement based on the number of likes and comments.

## How to Use?

1. **Authentication**: Make sure you have authenticated with your Instagram account before using the application. Enter your username and password in the `authenticate_instagram()` function in the `main.py` file.

2. **Execution**: Run the application using the command `streamlit run main.py`.

3. **Profile Search**: Enter the Instagram username of the profile you want to analyze in the sidebar and click the "Get Profile Info" button.

4. **View Results**: The analysis results, including profile information, the most used hashtags, and relevant charts, will be displayed in the right-hand columns and respective subpages.

## Libraries and Tools Used

- [Streamlit](https://streamlit.io/): A library for rapidly creating interactive web applications in Python.
- [Instaloader](https://instaloader.github.io/): A Python library for downloading and analyzing data from Instagram.
- [Pandas](https://pandas.pydata.org/): A library for data manipulation in Python.
- [Altair](https://altair-viz.github.io/): A Python library for interactive data visualization.

## Setup and Installation

1. Install all necessary libraries using the command:
```bash
pip install -r requirements.txt
```
2. Make sure you are authenticated on Instagram before running the application.

3. Run the application using the command:
```bash
streamlit run main.py
```

## Author
Clim Flavius

## Contributions
Contributions are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.