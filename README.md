# google_maps_scraper

This project is built for extracting business information from Google Maps dynamically by accepting two parameters when called:
1. Business needed (e.g., banks, hotels, consultants, etc.)
2. Location you want it at

## Installation

To set up this project, follow these steps:

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/google_maps_scraper.git
   ```

2. **Check into directory:**
	```sh
   cd google_maps_scraper
   ```

3. **Create a virtual environment:**
	```sh
	python -m venv venv
	```

4. **Activate virtual environment: (On windows)**
	```sh
	source venv\Scripts\activate
	```

5. **Install the required dependencies:**
	```sh
	pip install -r requirements.txt
	```

## USAGE

1. To run the google maps scraper, run this command rom your terminal:
```sh
	pytest scraper.py
```

2. When you run the script, it will prompt you to enter the service required and the location.
```
Enter the service required: <tax advisors>
Enter the location: <New York>
```
