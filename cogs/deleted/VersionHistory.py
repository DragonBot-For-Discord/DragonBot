import disnake as discord
from disnake.ext import commands

class VersionHistoryView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="0.0.5", style=discord.ButtonStyle.grey)
    async def ver005(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(name = "0.0.5 (dev)", value = "Добавлено: Спам фильтр, новые команды\nМногие команды перемещены в коги")
        await interaction.response.send_message(embed = embed, ephemeral=True)

    @discord.ui.button(label="0.0.6", style=discord.ButtonStyle.grey)
    async def ver006(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(inline = True, name = "0.0.6 (dev)", value = "Обновление базы данных плохих слов")
        await interaction.response.send_message(embed = embed, ephemeral=True)

    @discord.ui.button(label="0.0.7", style=discord.ButtonStyle.grey)
    async def ver007(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(inline = True, name = "0.0.7 (dev)", value = "Добавлено: Можно включать/выключать фильтры автомодераций\nДобавлено: Анти-Рейд")
        await interaction.response.send_message(embed = embed, ephemeral=True)

    @discord.ui.button(label="0.0.7.1", style=discord.ButtonStyle.gray)
    async def ver0071(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(inline = True, name = "0.0.7.1 (dev)", value = "Добавлено: Включение/Выключение фильтров теперь в когах\nДобавлено: Больше плохих слов в фильтре плохих слов\nПеремещено: Больше команд стало в когах\nУдалено и заменено: Ветка и версия бота из /about соеденились в [версиябота] ([ветка бота])\nДобавлено: Команда /generate_embed")
        await interaction.response.send_message(embed = embed, ephemeral=True)

    @discord.ui.button(label="0.0.8", style=discord.ButtonStyle.green)
    async def ver008(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(inline = True, name = "0.0.8 (beta)", value = "Новое: Бот переместился из ветки dev (На стадий ранней разработке), в ветку beta (Бета)\nНовое: Сделана копия GenAi\nДобавлено: В /stats добавлено сколько сообщений в GenAi")
        await interaction.response.send_message(embed = embed, ephemeral=True)

    @discord.ui.button(label="0.0.9", style=discord.ButtonStyle.red)
    async def ver009(self, button: discord.ui.Button, interaction: discord.MessageInteraction):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot")
        embed.add_field(inline = True, name = "0.0.9 (releasepreview)", value = "Новое: Бот переместился из ветки beta (Бета), в ветку releasepreview (Релиз превью (Почти релиз))\nНовое: Межсервер")
        await interaction.response.send_message(embed = embed, ephemeral=True)

class VersionHistory(commands.Cog):
    @commands.slash_command(description="История версий бота")
    async def ver_history(ctx):
        embed = discord.Embed(title="История версий бота", description="Ниже показана все обновления DragonBot\nНажимайте на кнопки чтобы посмотреть историю конкретной версии\nКрасная кнопка: Будущая версия\nЗелёная кнопка: Текущая версия\nСерая кнопка: Версия которая уже выпущена")
        await ctx.send(embed = embed, view = VersionHistoryView())

def setup(bot):
    bot.add_cog(VersionHistory(bot))