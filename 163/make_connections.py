
 
def main():
	fout = open('connections_output.txt', 'w')

	sources = {}
	connections = []
	
	
	people = []

	for filename in os.listdir('articles'):
		make_connections

def make_connections(article, names, connections, people):
	f = open('articles/'+path)
