from PIL import Image, ImageDraw, ImageFont, ImageFilter
from os import listdir
from os.path import isfile, join

width = 1275
height = 1650

perwidth = 507
perheight = 300

margin = 75

background = "WHITE"

onlyfiles = [f for f in listdir("singles") if isfile(join("singles", f))]
count = 1
while onlyfiles:
	init = (margin, margin)
	img = Image.new('RGBA', (width, height),background)
	d = ImageDraw.Draw(img)
	while init[1] < height - perheight - margin and onlyfiles:
		print("new line")
		while init[0] < width - perwidth - margin and onlyfiles:
			print(onlyfiles[0], init)
			img.paste(Image.open(f"singles/{onlyfiles.pop(0)}", 'r'), init)
			init = (init[0] + perwidth + margin, init[1])
		init = (margin, init[1] + perheight + margin)

	out = Image.new("RGB", (width,height), background)
	out.paste(img, (0, 0), img)
	out.save(f"out{count}.png")
	count += 1
