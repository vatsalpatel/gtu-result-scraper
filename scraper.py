from selenium import webdriver
from PIL import Image
from io import BytesIO
from time import sleep
import pytesseract

# URL for result (Summer 2021 - BE Sem 4)
URL = "https://www.gturesults.in/Default.aspx?ext=S2021&rof=2951"
# Enrollment numbers to scrap
# I have left only my own enrollment number to maintain privacy of others
enrs = [
    200540107523,
]
results = []


def binirize(image_to_transform, threshold):
    # Convert image to black-and-white
    image = image_to_transform.convert("L")
    w = image.width
    h = image.height
    for x in range(w):
        for y in range(h):
            if image.getpixel((x, y)) < threshold:
                image.putpixel((x, y), 0)
            else:
                image.putpixel((x, y), 255)
    return image


def text_captcha(captcha_image):
    # Solve the captcha
    new_size = (captcha_image.width * 3, captcha_image.height * 3)
    bigcaptcha = captcha_image.resize(new_size)
    img = binirize(bigcaptcha, 160)
    w = img.width
    # remove black line from captcha (pixels 68 to 73)
    for y in range(68, 73):
        for x in range(0, w):
            if img.getpixel((x, y - 1)) < 100:
                continue
            img.putpixel((x, y), 255)
    return pytesseract.image_to_string(img, lang="eng")


def extract_captcha(fox):
    # Extract captcha image for solving
    element = fox.find_element_by_id("imgCaptcha")
    location = element.location
    size = element.size
    png = fox.get_screenshot_as_png()

    im = Image.open(BytesIO(png))

    left = location["x"]
    top = location["y"]
    right = location["x"] + size["width"]
    bottom = location["y"] + size["height"]

    im = im.crop((left, top, right, bottom))  # crop and return captcha image
    return im


def extract_data(fox, num):
    # Submit form and Extract result data
    sln = text_captcha(extract_captcha(fox))
    enroll = fox.find_element_by_id("txtenroll")
    enroll.clear()
    enroll.send_keys(str(num))
    captcha = fox.find_element_by_id("CodeNumberTextBox")
    captcha.clear()
    captcha.send_keys(str(sln[:-2]))
    submit = fox.find_element_by_id("btnSearch")
    submit.click()

    try:
        # In case of wrong captcha submission
        fox.find_element_by_id("lblSPI")
    except Exception:
        if fox.find_element_by_id("lblmsg").text[0] == "O":
            # In case the data is not available
            return
        sleep(0.5)
        extract_data(fox, num)
        return

    flag = "Pass"
    if fox.find_element_by_id("lblmsg").text[0] == "S":
        flag = "Fail"
    results.append(
        (
            f'"{num}"',
            fox.find_element_by_id("lblName").text,
            fox.find_element_by_id("lblSPI").text,
            fox.find_element_by_id("lblCPI").text,
            flag,
        )
    )


fox = webdriver.Firefox()
fox.get(URL)
for num in enrs:
    try:
        extract_data(fox, num)
    except Exception as e:
        print(e)
fox.quit()


with open("data.csv", "a") as f:
    for line in results:
        f.write(", ".join(line))
        f.write("\n")
