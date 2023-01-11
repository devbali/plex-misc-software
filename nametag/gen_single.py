# Generate singular flyer
from PIL import Image, ImageDraw, ImageFont, ImageFilter

width = 507
height = 300

background = "WHITE"
getfont = lambda size: ImageFont.truetype("font.ttf", size)

def add_middle_aligned_text (d, y, text, fontsize, xstart = 0, xend = width):
	font = getfont(fontsize)
	x,z = font.getsize(text)
	d.text((xstart + (xend-xstart)//2-x//2,y), text, font = font, fill="BLACK")

def add_left_aligned_text (d, y, text, fontsize, x):
	font = getfont(fontsize)
	d.text((x,y), text, font=font, fill="BLACK")

def add_right_aligned_text (d, y, text, fontsize, xstart = 0, xend = width):
	font = getfont(fontsize)
	x,z = font.getsize(text)
	d.text((xend - x,y), text, font = font, fill="BLACK") 

def generate_card (firstname, lastname, auda, filename):
	img = Image.new('RGBA', (width, height),background)
	d = ImageDraw.Draw(img)

	img.paste(Image.open("background.png", 'r').resize((width,height)),(0,0))
	d.rectangle(xy=[(0,0), (width, height)], fill=None, outline="GREY", width=4)

	img.paste(Image.open("logo.png", 'r').resize((70,70)),(25,25))

	add_middle_aligned_text(d, 45, firstname, 65, 0, width)
	add_middle_aligned_text(d, 110, lastname, 65, 0, width)
	add_middle_aligned_text(d, 190, auda, 40, 0, width)

	out = Image.new("RGB", (width,height), background)
	out.paste(img, (0, 0), img)
	out.save(filename)

with open("data.tsv","r") as f:
	data = f.read().split("\n")

for line in data:
	firstname, lastname, auda = line.split("\t")
	generate_card(firstname, lastname, auda, f"singles/{firstname} {lastname}.png")
