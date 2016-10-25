from lxml import etree
import pygraphviz as pgv
import sys

def nodeAndEdge(db):
	node_list=[]
	edge_list=[]
	for db_entry in db:
		node_name=str((db_entry.find('.//lsp-id')).text).split('.')[0]
		node_list.append(node_name)
		neighbors=db_entry.findall('.//isis-neighbor')
		for neighbor in neighbors: 
			edge=[node_name, str(neighbor.find('.//is-neighbor-id').text).split('.')[0]]
			edge_list.append(edge)
	return node_list, edge_list

def removeDuplicates(data):
	clean_list=[]
	for x in data:
		if x not in clean_list:
			x.reverse()
			if x not in clean_list:
				if x[0] != x[1]:
					clean_list.append(x)
	return clean_list

def plotGraph(database,level):
	if len(database) != 0:
		graph=pgv.AGraph()
		nodes, edges = nodeAndEdge(database)
		graph.add_nodes_from(nodes)
		graph.add_edges_from(removeDuplicates(edges))
		graph.write("graph_level_"+str(level)+".dot")
	else:
		print "ISIS database does not have any node in ISIS Level "+str(level)

try:
	etree.parse(sys.argv[1])
except etree.ParseError:
	print "The syntax XML document is not in proper format"
except IOError:
	print "The document provided is not XML"
else:
	raw_data=etree.parse(sys.argv[1])

# Cleaning up the namespace against each XML TAG
	for elem in raw_data.getiterator():
		if not hasattr(elem.tag, 'find'):
			continue
		i=elem.tag.find('}')
		if i>=0:
			elem.tag=elem.tag[i+1:]

# Split the Database into L1 and L2 databases
	isis_l1_db, isis_l2_db =raw_data.findall('//isis-database')[0], raw_data.findall('//isis-database')[1]
	isis_l1_entries=isis_l1_db.xpath('.//isis-database-entry')
	isis_l2_entries=isis_l2_db.xpath('.//isis-database-entry')
	plotGraph(isis_l2_entries, 2)
	plotGraph(isis_l1_entries, 1)


