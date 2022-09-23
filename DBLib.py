class DBLib():
	def user_status(lang, status):
		if status == "idle":
			if lang == "ru":
				return "Неактивен"
			if lang == "en":
				return "Idle"
		elif status == "dnd":
			if lang == "ru":
				return "Не беспокоить"
			if lang == "en":
				return "Do Not Disturb"
		elif status == "online":
			if lang == "ru":
				return "Онлайн"
			if lang == "en":
				return "Online"
		elif status == "offline":
			if lang == "ru":
				return "Оффлайн"
			if lang == "en":
				return "Offline"
		elif status == None:
			if lang == "ru":
				return "Активность Отсутствует"
			if lang == "en":
				return "No Activity"
		else:
			return status

	def emoji(id):
		return f"<:dblib:{id}>"

	def timestamp(timestamp):
		return f"<t:{timestamp}:f>"