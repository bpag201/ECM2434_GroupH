from PIL import Image


def assemble(avatar_name, background_name=None, moustache_name=None, glasses_name=None, hat_name=None):
    """Assembles the final avatar"""
    final_avatar = Image.new("RGBA", (1335, 1984))
    
    if background_name is not None:
        background = Image.open(background_name)
        final_avatar.paste(background, (0, 0), background)
    
    avatar = Image.open(avatar_name)
    final_avatar.paste(avatar, (0, 0), avatar)
    
    if moustache_name is not None:
        moustache = Image.open(moustache_name)
        final_avatar.paste(moustache, (0, 0), moustache)
    
    if glasses_name is not None:
        glasses = Image.open(glasses_name)
        final_avatar.paste(glasses, (0, 0), glasses)

    if hat_name is not None:
        hat = Image.open(hat_name)
        final_avatar.paste(hat, (0, 0), hat)
    
    final_avatar.save("final_avatar.png")
    return final_avatar
