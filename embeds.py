import discord


def embed_success(description):
    em = discord.Embed(title = "Success",
                       description = f"{description}",
                       color = discord.Color.brand_green())
    return em


def embed_error(description):
    em = discord.Embed(title = "Error",
                       description = f"{description}",
                       color = discord.Color.brand_red())
    return em
