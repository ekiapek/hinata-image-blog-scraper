# hinata-image-blog-scraper
Simple Python script to download all the lovely Hinatazaka46 member's blog images.
This script will grab all images from the first page of each member's blog. I personally use this to download the latest image from all members, incorporating the use of Windows Task Scheduler which will execute the script automatically. Once triggered, the script will download all the images located on the first page from each member's personal blog and discard if the image already exist in your system.
## How-to
### Running as python file
To run the script as normal python script, run
```
python hinata-blog-scraper.py
```
The script will save the images in the same folder where the script is running. To specify where to save the images, supply the script with `-d` or `--dir` and type your destination folder.
Type `-h` or `--help` to see other possible commands.
### Portable executable file
This script is now available in portable executable format (Windows only). To run the executable, open command prompt and run `hinata-blog-scraper.exe`
## Requirements
Read this section only if you're running this as a Python file.
This script can only run on Python 3.5 or higher. You must have the installed library used by the script to run.
To get the required libraries, please run
```
pip install -r requirements.txt
```
### Incorporating Windows Task Scheduler
You can use Windows Task Scheduler to automate the script to run at specific time. If you want to schedule the script to run automatically, it is recommended to use the portable executable format.