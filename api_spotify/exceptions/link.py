class Invalid_Link(Exception):
	def __init__(
		self,
		link: str,
		message: str = 'Invalid link \'{link}\''
	):
		self.link = link
		self.message = message

		super().__init__(
			self.message.format(
				link = link
			)
		)
