from gremlin_python.structure.graph import Graph
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.process.traversal import Order, P

# Conect to gremlin server
graph = Graph()
remote_connection = DriverRemoteConnection('ws://localhost:8182/gremlin', 'g')
g = graph.traversal().withRemote(remote_connection)

# Add users
user1 = g.addV('user').property('userId', '1').next()
user2 = g.addV('user').property('userId', '2').next()
user3 = g.addV('user').property('userId', '3').next()

# Add itens
item1 = g.addV('item').property('itemId', 'A').next()
item2 = g.addV('item').property('itemId', 'B').next()
item3 = g.addV('item').property('itemId', 'C').next()

# Add rating
rating1 = g.addE('rated').from_(user1).to(item1).property('rating', 5).next()
rating2 = g.addE('rated').from_(user1).to(item2).property('rating', 3).next()
rating3 = g.addE('rated').from_(user2).to(item1).property('rating', 4).next()
rating4 = g.addE('rated').from_(user2).to(item3).property('rating', 5).next()
rating5 = g.addE('rated').from_(user3).to(item2).property('rating', 4).next()
rating6 = g.addE('rated').from_(user3).to(item3).property('rating', 3).next()

# Verify the edges
edges = g.E().toList()
print("Arestas:", edges)

# Found a best rated content for an user
user1_ratings = g.V().has('user', 'userId', '1').outE('rated').order().by('rating', Order.desc).inV().values('itemId').toList()
print("Itens mais bem avaliados pelo usuário 1:", user1_ratings)

# Recommendation by similarity
# Adjust to ignore the user himself in the recommendation
recommended_items_for_user1 = g.V().has('user', 'userId', '1').as_('a').out('rated').in_('rated').has('user', 'userId', P.neq('1')).out('rated').dedup().values('itemId').toList()
print("Itens recomendados para o usuário 1:", recommended_items_for_user1)

remote_connection.close()
