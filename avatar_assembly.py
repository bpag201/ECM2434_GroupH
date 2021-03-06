from PIL import Image


def assemble(background_name, avatar_name, moustache_name, glasses_name, hat_name):
    """Assembles the final avatar"""

    background = Image.open(background_name)
    avatar = Image.open(avatar_name)
    moustache = Image.open(moustache_name)
    glasses = Image.open(glasses_name)
    hat = Image.open(hat_name)
    final_avatar = Image.new("RGBA", (1335, 1984))
    final_avatar.paste(background, (0, 0), background)
    final_avatar.paste(avatar, (0, 0), avatar)
    final_avatar.paste(moustache, (0, 0), moustache)
    final_avatar.paste(glasses, (0, 0), glasses)
    final_avatar.paste(hat, (0, 0), hat)
    final_avatar.save("final_avatar.png")
    final_avatar.show()
    return final_avatar


assemble('D:\GIMP 2.10.22\Accessories\Backgrounds png\Red background.png',
         'D:\GIMP 2.10.22\Plain silhouette.png',
         'D:\GIMP 2.10.22\Accessories\Moustache png\Brown moustache.png',
         'D:\GIMP 2.10.22\Accessories\Round glasses png\Red round glasses.png',
         'D:\GIMP 2.10.22\Accessories\Top Hat png\Green strip top hat.png')
