from disnake.ext import commands
from random import randint
import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
print("[SQLite ErrorHandler] database.db загружен!")

class ErrorHandler(commands.Cog):
    # Error handling
    @commands.Cog.listener()
    async def on_slash_command_error(ctx, message, error):
        if isinstance(error, commands.CheckFailure):
            await message.send(f"У вас нет прав для использования этой команды. | You don't have permission to use this command.", ephemeral=True)
        else:
            errorCode = randint(1, 2147483647)
            cursor.execute(f'INSERT INTO errorCodes (errorCode, error) VALUES ({errorCode}, "{error}")')
            connection.commit()

            print(f'[Ошибка] {error}')
            try:
                await message.send(f"Что-то пошло не так... Свяжитесь с владельцем бота, и сообщите ему этот код ошибки: {errorCode}\nSomething went wrong... Contact the owner of the bot, and tell him this error code: {errorCode}", ephemeral=True)
            except:
                pass

    @commands.Cog.listener()
    async def on_user_command_error(ctx, message, error):
        if isinstance(error, commands.CheckFailure):
            await message.send(f"У вас нет прав для использования этой команды. | You don't have permission to use this command.", ephemeral=True)
        else:
            errorCode = randint(1, 2147483647)
            cursor.execute(f'INSERT INTO errorCodes (errorCode, error) VALUES ({errorCode}, "{error}")')
            connection.commit()

            print(f'[Ошибка] {error}')
            try:
                await message.send(f"Что-то пошло не так... Свяжитесь с владельцем бота, и сообщите ему этот код ошибки: {errorCode}\nSomething went wrong... Contact the owner of the bot, and tell him this error code: {errorCode}", ephemeral=True)
            except:
                pass

    @commands.Cog.listener()
    async def on_message_command_error(ctx, message, error):
        if isinstance(error, commands.CheckFailure):
            await message.send(f"У вас нет прав для использования этой команды.\nYou don't have permission to use this command.", ephemeral=True)
        else:
            errorCode = randint(1, 2147483647)
            cursor.execute(f'INSERT INTO errorCodes (errorCode, error) VALUES ({errorCode}, "{error}")')
            connection.commit()

            print(f'[Ошибка] {error}')
            try:
                await message.send(f"Что-то пошло не так... Свяжитесь с владельцем бота, и сообщите ему этот код ошибки: {errorCode}\nSomething went wrong... Contact the owner of the bot, and tell him this error code: {errorCode}", ephemeral=True)
            except:
                pass

def setup(bot):
    bot.add_cog(ErrorHandler(bot))