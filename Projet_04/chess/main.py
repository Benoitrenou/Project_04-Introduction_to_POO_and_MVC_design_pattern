from controllers.controllers import ApplicationController

DEFAULT_NUMBER_OF_ROUNDS = 4


def main():
	app = ApplicationController()
	app.start()


if __name__ == "__main__":
    main()