import threading
import time


class ExampleWorkerClass:
	def __init__(self):
		# This variable is necessary because python doesn't offer a way to gracefully kill a thread
		self.running = False

	def stop(self):
		# This sets the running variable to false, which allows finnish the last iteration of the loop instead of simply
		# killing it. This to make sure you're not killing the thread while it was halfway in storing the result and
		# possibly corrupt some results
		self.running = False

	def run(self):
		# Do every thing in the loop until the variable becomes false (Which is changed when WorkerClas.stop() is called)
		self.running = True
		while self.running:
			print("--- Thread: But I'm still able to do my work in the background ---")
			time.sleep(1)


if __name__ == "__main__":
	worker = ExampleWorkerClass()

	# create a thread that calls the run() functions of the worker (mind that there are no parentheses around the
	# 'worker.run' as we're passing the function call, instead of actually executing the function and passing the result
	thread = threading.Thread(target=worker.run, args=[])

	# Nothing will be done until the thread is started
	thread.start()

	# Here is some pointless stuff happening to indicate that the thread keeps running regardless of this loop
	for x in range(20):
		print("I'm stuck in this loop, and won't anything else than this")
		time.sleep(0.5)

	print("That's enough for the thread")
	# Tell the thread to stop working (mind that I'm calling worker.stop() and not thread.stop() )
	worker.stop()

	# Some other pointless stuff to indicate that now the thread isn;t doing anything anymore
	for x in range(10):
		print("Stuck in this loop again, but now the thread should'nt be printing anythin anymore")
		time.sleep(0.5)
