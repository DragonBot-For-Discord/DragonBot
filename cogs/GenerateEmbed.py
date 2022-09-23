import disnake as discord
from disnake.ext import commands
from disnake import Localized

class GenerateEmbed(commands.Cog):
    @commands.slash_command(description=Localized("Generate embed", key="GENERATE_EMBED_DESCRIPTION"))
    @commands.has_permissions(manage_channels = True)
    async def generate_embed(
        ctx,
        title: str,
        description: str,
        colorhex: int = 0,
        embedfooter: str = None,
        embedurl: str = None,
        thumbnailurl: str = None,
        imageurl: str = None
    ):
        if embedurl == None:
            embed = discord.Embed(
                title=title,
                description=description,
                color=colorhex
            )
        else:
            embed = discord.Embed(
                title=title,
                description=description,
                color=colorhex,
                url = embedurl
            )

        if imageurl == None: pass
        else: embed.set_image(imageurl)

        if thumbnailurl == None: pass
        else: embed.set_thumbnail(thumbnailurl)

        if embedfooter == None: pass
        else: embed.set_footer(text=embedfooter)

        await ctx.send(embed = embed)

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(GenerateEmbed(bot))