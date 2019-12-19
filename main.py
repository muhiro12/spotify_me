import api

def update():
	print('[LOG] update() was called.')
	api.updateMyBest()
	api.updateTop20()
	api.updateRecent()

update()
