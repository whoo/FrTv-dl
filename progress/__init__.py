import sys
class progressbar:
	current=0
	maxval=100
	def __init__(self,maxval):
		self.maxval=maxval;
		
	def display(self,current):
		sys.stdout.write("\r")
		sys.stdout.write("[")
		x = int(100*current/self.maxval)
		inner_bar = ['#' for i in range(int(x/2))] + ["." for i in range(49 - int(x/2))]
		sys.stdout.write("".join(inner_bar))
		sys.stdout.write("]")
		sys.stdout.write(" "+str(x))
		sys.stdout.write("%")
		sys.stdout.flush()
