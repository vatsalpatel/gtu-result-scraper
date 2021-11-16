# gtu-result-scraper
Automated GTU Result Scraper using Selenium and Tesseract OCR to bypass text based captcha.

## Requirements
Python 3<br/>
Tesseract OCR<br/> 
pytesseract<br/>
Selenium(With gecko driver for firefox)<br/>
Gecko Driver Executable(included .exe file)
Pillow<br/>

## Setup
Download and install Tesseract OCR<br/>
`Tesseract OCR`: https://github.com/tesseract-ocr/tesseract/releases/tag/4.1.1 <br/><br/>
`Python libraries`:
```
pip install pytesseract selenium Pillow
```
Executable is included in the repo but you may have to add it to PATH. No need to download again.
`Gecko Driver for Firefox(Included)`: https://github.com/mozilla/geckodriver/releases<br/>

## Run
Change the result URL and populate the enrs list with desired enrollment numbers and simply run the file `scraper.py`.
```
python scraper.py
```

## Captcha
GTU Captchas are text and digit based which allows us to use Optical Character Recognition(OCR) <br/><br/>
However, The captcha characters are crossed out so we need to remove this line for OCR to be able to parse the image.<br/>

#### Before:
![Before](/before.jpg "Before line is removed")

The y co-ordinate of the line will depend on device being used to scrape the website and mainly the viewport of the browser we are using. For me, it was row 68 to 73. You can easily check this using paint. If you have a difference y co-ordinate for the black line then change the row values in `text_captcha()` function in `scraper.py`.
#### After:
![After](/after.jpg "After line is removed")

OCR can easily parse this but the success rate isn't 100% so scraper is built to auto retry wrong captchas.

## Output
Output will be appended to a csv file named `data.csv` at the end <br/>
Open it in excel for manipulation<br/>
Since enrollment numbers are 12 digits long, saving the excel file will convert them to exponential format and original enrollment number will be lost.

## If the script freezes
Script may freeze on some enrollment number trying the captcha again and again.<br/>
Cause of this is still unknown but is likely to be GTU website not being able to keep up with speed of the script.<br/>
Simply hit the captcha reset button next to captcha image on the headless window and it will start working again.<br/>
