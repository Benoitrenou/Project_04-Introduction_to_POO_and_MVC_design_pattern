class ExceptionsView:
	def invalid_rank_error(self):
		print ("This is not a valid rank")

class InvalidRankError(Exception):
	def __init__(self):
	    # super().__init__()
	    self.view = ExceptionsView()

	def __call__(self):
		self.view.invalid_rank_error()

class TournamentFinished:
	pass

