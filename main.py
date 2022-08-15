from PIL import Image, ImageDraw, ImageFont
import requests
import datetime
import random
import time
import os

qualaty = 3

## Get ids of sender and recipian

print("User token (sender token)")
token = input(">> ")

auth = {"Authorization": token}
sender = requests.get(f"https://discord.com/api/users/@me", headers = auth).json()

print(f"\nLoaded {sender['username']}, avatar: {sender['avatar']}")

print("\nId of recipiant")
recID = input(">> ")

rec = requests.get(f"https://discord.com/api/users/{recID}", headers = auth).json()
print(f"\nLoaded {rec['username']}, avatar: {rec['avatar']}")

time.sleep(.4)

## Download avatars

print("\nDownloading avatars...")

url = f"https://cdn.discordapp.com/avatars/{sender['id']}/{sender['avatar']}.webp"
img_data = requests.get(url).content
with open('sender.wdbp', 'wb') as handler:
    handler.write(img_data)

url = f"https://cdn.discordapp.com/avatars/{rec['id']}/{rec['avatar']}.webp"
img_data = requests.get(url).content
with open('rec.wdbp', 'wb') as handler:
    handler.write(img_data)

## Build the image

# Open the profile pictures and apply mask
senderImg = Image.open('sender.wdbp').resize((40 * qualaty, 40 * qualaty))
recImg = Image.open('rec.wdbp').resize((40 * qualaty, 40 * qualaty))

nitroImg = Image.open('classic.png')
nitroImg = nitroImg.resize((int(nitroImg.width * 0.8695652173913043 * qualaty), int(nitroImg.height * 0.8695652173913043 * qualaty)))

# Create the round mask for cutting the inserted image
mask_im = Image.new("L", senderImg.size, 0)
draw = ImageDraw.Draw(mask_im)
draw.ellipse((0, 0, senderImg.size[0], senderImg.size[1]), fill=255)

# Create the canvas
img = Image.new('RGB', (900 * qualaty, 320 * qualaty), color = '#36393f')

# Paste profile pics onto canvas
img.paste(senderImg, (100, 50), mask_im)
img.paste(recImg, (100, 50 + nitroImg.height + 50 * qualaty), mask_im)
img.paste(nitroImg, (100 + (40 * qualaty) + 10 * qualaty, 50 + (20 * qualaty)))

# Insert text
draw = ImageDraw.Draw(img)

font = ImageFont.truetype("fonts/whitneysemibold.otf", 20 * qualaty)
draw.text((100 + (40 * qualaty) + 10 * qualaty, 50 - 5 * qualaty), sender["username"], font=font)
draw.text((100 + (40 * qualaty) + 10 * qualaty, 50 - 5 * qualaty + nitroImg.height + 50 * qualaty), rec["username"], font=font)

# Get text size for timestamp
senderSize = draw.textsize(sender["username"], font=font)[0]
recSize = draw.textsize(rec["username"], font=font)[0]

now = datetime.datetime.now().strftime("Today at %I:%M %P")

font = ImageFont.truetype("fonts/whitneylight.otf", 10 * qualaty)
draw.text((100 + (40 * qualaty) + 10 * qualaty + senderSize + 10 * qualaty, 50 - 5 * qualaty + (9.5 * qualaty)), now, font=font, fill="#9fa2a6")
draw.text((100 + (40 * qualaty) + 10 * qualaty + recSize + 10 * qualaty, 50 - 5 * qualaty + (9.5 * qualaty)+ nitroImg.height + 50 * qualaty), now, font=font, fill="#9fa2a6")

font = ImageFont.truetype("fonts/whitneybook.otf", 19 * qualaty)

## Generate random response
with open("responses.txt", "r") as file:
    data = [i.strip() for i in file.readlines()]
    print(data)

choice = random.choice(data)
print(choice)

draw.text(
    (
        100 + (40 * qualaty) + 10 * qualaty,
        50 - 5 * qualaty + (9.5 * qualaty)+ nitroImg.height + 63 * qualaty
    ), 
    choice, font=font, fill="#cfd0cf")



img.save('out.png')

os.remove("rec.wdbp")
os.remove("sender.wdbp")




