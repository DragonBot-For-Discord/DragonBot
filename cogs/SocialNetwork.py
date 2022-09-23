import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite SocialNetwork] database.db загружен!")

class SocialNetwork(commands.Cog):
    @commands.slash_command(description=Localized("Social network profile", key="SN_PROFILE_DESCRIPTION"))
    async def sn_profile(ctx):
        cursor.execute(f'SELECT * FROM sn_posts WHERE user_id = {ctx.author.id}')
        posts = cursor.fetchall()

        embed = discord.Embed(title = f"Профиль {ctx.author.name}", description = f"Постов: {len(posts)}")
        await ctx.send(embed = embed)

    @commands.slash_command(description=Localized("Create post", key="SN_POST_CREATE_DESCRIPTION"))
    async def sn_post_create(ctx, title: str, text: str):
        cursor.execute(f'INSERT INTO sn_posts(user_id, postTitle, postText) VALUES({ctx.author.id}, "{title}", "{text}")')
        connection.commit()

        await ctx.send('Пост создан!')

    @commands.slash_command(description=Localized("View post", key="SN_POST_VIEW_DESCRIPTION"))
    async def sn_post_view(ctx, author: discord.Member, title: str):
        try:
            cursor.execute(f'SELECT * FROM sn_posts WHERE user_id = {author.id} AND postTitle = "{title}"')
            result = cursor.fetchone()

            embed = discord.Embed(title = f"{result[1]} от {author.name}", description = f"{result[2]}")
            await ctx.send(embed = embed)
        except:
            await ctx.send('Пост не найден')

    @commands.slash_command(description=Localized("View post", key="SN_POST_VIEW_DESCRIPTION"))
    async def sn_post_delete(ctx, title: str):
        try:
            cursor.execute(f'DELETE FROM sn_posts WHERE user_id = {ctx.author.id} AND postTitle = "{title}"')
            connection.commit()

            await ctx.send('Пост удалён')
        except:
            await ctx.send('Пост не найден')

def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(SocialNetwork(bot))