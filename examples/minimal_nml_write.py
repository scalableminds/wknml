import wknml

groups = [wknml.Group(id=1, name='Synapses', children=[])]

trees = [
  wknml.Tree(
    id=1, 
    color=(255,255,0,1),
    name="Synapse 1", 
    nodes=[wknml.Node(id=1, position=(12,34,56), radius=12)],
    edges=[],
    groupId=1
  ),
  wknml.Tree(
    id=2, 
    color=(255,0,255,1),
    name="Synapse 2", 
    nodes=[wknml.Node(id=3, position=(56,34,12), radius=12)],
    edges=[],
    groupId=1
  )
]

nml = wknml.NML(
  parameters=wknml.NMLParameters(
    name="Test",
    scale=(11.24, 11.24, 25),
  ),
  trees=trees,
  branchpoints=[],
  comments=[],
  groups=groups,
)

with open('out.nml', 'wb') as f:
  wknml.write_nml(f, nml)
