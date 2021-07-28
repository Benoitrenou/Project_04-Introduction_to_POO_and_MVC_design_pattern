class InvalidRankErrorView:
	def print(self):
		print ("This is not a valid rank")

class InvalidRankError():
	def __init__(self):
	    super().__init__()
	    self.view = InvalidRankErrorView()

	def __call__(self):
		self.view.print()

