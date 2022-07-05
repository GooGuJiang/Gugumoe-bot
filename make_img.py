from PIL import Image, ImageDraw
import os

def make_eat_img(img_name,tgid):
    try:
        img_data = os.path.join('.', 'make_img', 'bg.png')
        tmp_data = os.path.join('.', 'tmp', f'eat_img_{tgid}.png')
        input_img_data = os.path.join('.', 'tmp', img_name)
        out_img_rl  = os.path.join('.', 'output', f'eat_img_{tgid}.png')

        bg_size = (600, 400)
        bg = Image.new('RGBA', bg_size)
        avatar_size = (130, 130)
        avatar = Image.open(input_img_data)
        avatar = avatar.resize(avatar_size)
        mask = Image.new('RGBA', avatar_size, color=(0,0,0,0))
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0,0, avatar_size[0], avatar_size[1]), fill=(0,0,0,255))
        x, y = 299, 289
        box = (x, y, (x + avatar_size[0]), (y + avatar_size[1]))
        bg.paste(avatar, box, mask)
        bg.save(tmp_data)

        bg_size = (600, 400)
        bg = Image.open(tmp_data)
        fruit_size = (600, 400)
        fruit = Image.open(img_data).convert('RGBA')
        x, y = int((bg_size[0]-fruit_size[0])/2), int((bg_size[1]-fruit_size[1])/2)
        fruit_box = (x, y, (x + fruit_size[0]), (y + fruit_size[1]))
        fruit = fruit.resize(fruit_size)
        bg.paste(fruit, fruit_box, fruit)
        bg.save(out_img_rl)
        os.remove(tmp_data)
        return out_img_rl
    except Exception as errr:
        print(errr)
        return False

