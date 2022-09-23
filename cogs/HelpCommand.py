import disnake as discord
from disnake.ext import commands
from disnake import Localized
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite HelpCommand] database.db загружен!")

embedColor = 0x520500

class HelpDropdown(discord.ui.Select):
    def __init__(self, langCode):
        langCodeReal = langCode
        if langCodeReal == 'ru':
            # Set the options that will be presented inside the dropdown
            options = [
                discord.SelectOption(
                    label="Модерация сервера", description="Команды для модераций сервера", emoji="🔧", value="moderation"
                ),
                discord.SelectOption(
                    label="Команды генераций", description="Команды для генераций разных штук", emoji="🚦", value="command_generations"
                ),
                discord.SelectOption(
                    label="АвтоМодерация", description="Команды для генераций разных штук", emoji="🔨", value="automod"
                ),
                discord.SelectOption(
                    label="Всякие весёлые штуки", description="Команды для генераций разных штук", emoji="🎮", value="fun"
                ),
                discord.SelectOption(
                    label="Команды на правую кнопку мыши", description="Команды на правую кнопку мыши", emoji="🖱", value="right-click-commands"
                ),
            ]

            # The placeholder is what will be shown when no option is chosen
            # The min and max values indicate we can only pick one of the three options
            # The options parameter defines the dropdown options. We defined this above
            super().__init__(
                placeholder="Выберите категорию",
                min_values=1,
                max_values=1,
                options=options,
            )
        if langCodeReal == 'en':
            # Set the options that will be presented inside the dropdown
            options = [
                discord.SelectOption(
                    label="Moderation", description="Commands for moderation", emoji="🔧", value="moderation"
                ),
                discord.SelectOption(
                    label="Generations", description="Commands for generations", emoji="🚦", value="command_generations"
                ),
                discord.SelectOption(
                    label="AutoMod", description="Commands for automod", emoji="🔨", value="automod"
                ),
                discord.SelectOption(
                    label="Fun", description="Commands for fun", emoji="🎮", value="fun"
                ),
                discord.SelectOption(
                    label="Right-click commands", description="Commands for right-click", emoji="🖱", value="right-click-commands"
                ),
            ]

            # The placeholder is what will be shown when no option is chosen
            # The min and max values indicate we can only pick one of the three options
            # The options parameter defines the dropdown options. We defined this above
            super().__init__(
                placeholder="Select category",
                min_values=1,
                max_values=1,
                options=options,
            )


    async def callback(self, interaction: discord.MessageInteraction):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {interaction.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
        
        # select menu
        if langCodeReal == "ru":
            if self.values[0] == "moderation":
                embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
                embed.add_field(name="Модерация сервера", value=f"""
                Команды для модерации сервера:
                \n - kick <пользователь> <причина> - Кикает пользователя
                \n - ban <пользователь> <причина> - Банит пользователя
                \n - unban <пользователь> - Разбанит пользователя
                \n - mute <пользователь> <время в секундах> <причина> - Мутит пользователя
                \n - clear <количество> - Очищает чат
                \n - del_spam_channels <название> - Удаляет каналы с одинаковыми названиями
                \n - del_spam_roles <название> - Удаляет роли с одинаковыми названиями
                \n - backup <действие> - Сделать бэкап сервера
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "command_generations":
                embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
                embed.add_field(name="Команды генераций", value=f"""
                Команды для генераций разных штук:
                \n - rand_number <минимальное число> <максимальное число> - Генерирует случайное число
                \n - rand_string <количество символов> - Генерирует случайные символы
                \n - rand_uuid - Генерирует случайны UUID
                \n - generate_embed - Сделать эмбед""", inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "automod":
                embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
                embed.add_field(name="АвтоМодерация", value=f"""
                Автомодерация **выключена** по умолчанию, но её можно включить
                \n - automod_spam <off/on> - Включить/выключить автомодерацию по спаму
                \n - automod_badwords <off/on> - Включить/выключить автомодерацию по матам
                \n - automod_raid <off/on> - Включить/выключить автомодерацию по рейдам-крашам
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "fun":
                embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
                embed.add_field(name="Всякие весёлые штуки", value=f"""
                GenAi **выключен** по умолчанию, но его можно включить
                \n - animals - Посмотреть разных животных
                \n - genai_toggle <канал> <вкл/выкл> - Включить/выключить GenAi
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "right-click-commands":
                embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
                embed.add_field(name="Команды на правую кнопку мыши", value=f"""
                Или же на зажать на сообщений или нажать на пользователя
                \n Команды на пользователя:
                \n - Аватар - Посмотреть аватарку пользователя
                \n - Информация о пользователе - Посмотреть информацию о пользователе
                \n Команды на сообщение:
                \n - Репортнуть плохое слово - Отправить команде разработчиков сообщение с плохим словом
                """, inline=False)
                await interaction.response.edit_message(embed = embed)
        elif langCodeReal == "en":
            if self.values[0] == "moderation":
                embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
                embed.add_field(name="Commands for moderation of the server", value=f"""
                \n - kick <user> <reason> - Kicks the user
                \n - ban <user> <reason> - Bans the user
                \n - unban <user> - Unbans the user
                \n - mute <user> <time in seconds> <reason> - Mutes the user
                \n - clear <amount> - Clears the chat
                \n - del_spam_channels <name> - Deletes channels with the same name
                \n - del_spam_roles <name> - Deletes roles with the same name
                \n - backup <action> - Make a server backup
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "command_generations":
                embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
                embed.add_field(name="Commands for command generations", value=f"""
                Commands for command generations:
                \n - rand_number <min> <max> - Generates a random number
                \n - rand_string <amount> - Generates random characters
                \n - rand_uuid - Generates a random UUID
                \n - generate_embed - Make an embed""" , inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "automod":
                embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
                embed.add_field(name="Automod commands", value=f"""
                \n - automod_spam <off/on> - Enable/disable automod for spam
                \n - automod_badwords <off/on> - Enables/disables automod for badwords
                \n - automod_raid <off/on> - Enables/disables automod for raids
                """ , inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "fun":
                embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
                embed.add_field(name="Commands for fun", value=f"""
                \n - animals - Shows different animals
                \n - genai_toggle <channel> <on/off> - Enables/disables GenAi
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
            elif self.values[0] == "right-click-commands":
                embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
                embed.add_field(name="Commands for right-click", value=f"""
                \n - avatar - Shows the avatar of the user
                \n - info - Shows information about the user
                \n - report <word> - Sends a message to the developers with the bad word
                """, inline=False)
                await interaction.response.edit_message(embed=embed)
                





class DropdownView(discord.ui.View):
    def __init__(self, langCode):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(HelpDropdown(langCode))

class HelpCommand(commands.Cog):
    @commands.slash_command(description=Localized("Shows help on commands", key="HELP_DESCRIPTION"))
    async def help(ctx):
        cursor.execute(f"SELECT lang_code FROM guilds_lang WHERE guild_id = {ctx.guild.id}")
        langCode = cursor.fetchone()
        langCodeStr = str(langCode)
        langCodeReal = langCodeStr.replace('(', '').replace(')', '').replace(',', '').replace("'", '')
        
        # select menu
        if langCodeReal == "ru":
            embed = discord.Embed(title="Помощь по командам", description=f"Ниже показаны все команды бота\nЧтобы выбрать категорию, нажмите ниже", color=embedColor)
            await ctx.response.send_message(embed = embed, view=DropdownView(langCodeReal), ephemeral=True)
        elif langCodeReal == "en":
            embed = discord.Embed(title="Help for commands", description=f"Below are all commands of the bot\nTo select a category, click below", color=embedColor)
            await ctx.response.send_message(embed = embed, view=DropdownView(langCodeReal), ephemeral=True)



def setup(bot):
    bot.i18n.load("locale/")
    bot.add_cog(HelpCommand(bot))