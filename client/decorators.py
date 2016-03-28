from threading import Thread

def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
		thr.start()
	return wrapper

def run_thread(fn):
	def run(*args, **kwargs):
		try:
			thread = Thread(target=fn, args=args, kwargs=kwargs)
			thread.daemon = True
			thread.start()
			print ("Nova Thread %s",thread)
			return thread # <-- this is new!
		except Exception, e:
			print "Thread is die?"
	return run