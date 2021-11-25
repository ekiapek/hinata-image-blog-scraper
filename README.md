# hinata-image-blog-scraper
Simple Python script to download all the lovely Hinatazaka46 member's blog images.
This script will grab all images from the first page of each member's blog. I personally use this to download the latest image from all members, incorporating the use of Windows Task Scheduler which will execute the script automatically. Once triggered, the script will download all the images located on the first page from each member's personal blog and discard if the image already exist in your system.
If you're hoping that this script will download all the images from the very beginning of each member's blog, I'm afraid that this script is not capable yet. But probably it will be added as a feature. If you want to contribute, just fork me!

## Requirements
This script requires Python 3.5 or higher with dependencies located in requirements.txt. Just run 
```
pip install -r requirements.txt
```
to get all the dependencies required.

## How-to
First you have to specify to which folder you want to save the images to. Edit the configuration file in [config.json](config.json) and fill in the value for `basePath`. This will be the base folder for the script to work on as the script will download the image according to the member.
### Running as python file
To run the script as normal python script, run
```
python hinata-blog-scraper.py
```
### Incorporating Windows Task Scheduler
You can use Windows Task Scheduler to automate the script to run at specific time. I've set mine to run every 8 hours.
