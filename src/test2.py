import graphlite as g

db = g.connect(':memory:', graphs=['knows'])
with db.transaction():
    for person in [2, 3]:
        db.store(g.V(1).knows(person))
db.find(g.V(1).knows).to(list)
