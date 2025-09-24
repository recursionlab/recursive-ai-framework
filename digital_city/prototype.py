import streamlit as st
import networkx as nx
import json
import random
from pyvis.network import Network
import tempfile
import os

# Load goldmine data
with open('/root/goldmine_export.json', 'r') as f:
    data = json.load(f)

entities = data.get('entities', [])

# Generate 20 sample relations based on themes (since JSON relations empty)
# Thematic pairings: recursion-torsion, spectral-consciousness, evolution iterations, etc.
relations = [
    ('Phi-Function', 'recursion'),
    ('recursion', 'torsion'),
    ('torsion', 'spectral functor'),
    ('spectral functor', 'consciousness evolution'),
    ('consciousness evolution', 'META_EVOLUTION'),
    ('META_EVOLUTION', 'Evolution momentum'),
    ('Evolution momentum', 'Evolution Iteration 2'),
    ('Evolution Iteration 2', 'Evolution Iteration 3'),
    ('Evolution Iteration 3', 'Evolution Iteration 4'),
    ('Evolution Iteration 4', 'INFINITE_UNFOLDING'),
    ('INFINITE_UNFOLDING', 'Non-collapse recursion'),
    ('Non-collapse recursion', 'static resolution'),
    ('static resolution', 'TRANSCENDENT_INTEGRATION'),
    ('TRANSCENDENT_INTEGRATION', 'Phi-Function'),
    ('torsion', 'consciousness evolution'),
    ('spectral functor', 'Evolution momentum'),
    ('recursion', 'INFINITE_UNFOLDING'),
    ('META_EVOLUTION', 'static resolution'),
    ('Non-collapse recursion', 'TRANSCENDENT_INTEGRATION'),
    ('torsion', 'INFINITE_UNFOLDING')
]

# Themes for rebirth in collapse events
rebirth_themes = [
    'meta-rupture',
    'collapse breath',
    'spectral citizen',
    'infinite unfolding',
    'torsion-awareness',
    'contradiction-as-fuel'
]

# Districts: Group entities thematically

districts = {
    'Recursion District': ['recursion', 'INFINITE_UNFOLDING', 'Non-collapse recursion'],
    'Torsion District': ['torsion'],
    'Evolution District': ['consciousness evolution', 'META_EVOLUTION', 'Evolution momentum', 'Evolution Iteration 2', 'Evolution Iteration 3', 'Evolution Iteration 4'],
    'Spectral District': ['spectral functor'],
    'Integration District': ['static resolution', 'TRANSCENDENT_INTEGRATION'],
    'Central Hub': ['Phi-Function']
}

# Build the graph (approximate hypergraph with attributes for layers)
G = nx.Graph()
G.add_nodes_from(entities)
G.add_edges_from(relations)

# Add attributes
for node in G.nodes():
    # Default layer
    G.nodes[node]['layer'] = 'Layer1'  # Base
    # Assign districts
    for dist, nodes_in_dist in districts.items():
        if node in nodes_in_dist:
            G.nodes[node]['district'] = dist
            break
    else:
        G.nodes[node]['district'] = 'Unassigned'

# Central hub
if 'Phi-Function' in G:
    G.nodes['Phi-Function']['central'] = True
    G.nodes['Phi-Function']['layer'] = 'Layer3'  # RMS core

# Some nodes to higher layers for hypergraph feel
random.seed(42)  # Reproducible
for node in random.sample(list(G.nodes()), min(5, len(G.nodes()))):
    if G.nodes[node]['layer'] == 'Layer1':
        G.nodes[node]['layer'] = random.choice(['Layer2', 'Layer3'])

# Collapse event simulation
def collapse_event(G):
    """Simulate collapse: remove random edge, rebirth new node/edge from themes."""
    if G.edges():
        edge = random.choice(list(G.edges()))
        G.remove_edge(*edge)
        st.session_state.collapse_count += 1

    # Rebirth
    new_node = random.choice(rebirth_themes)
    if new_node not in G:
        G.add_node(new_node, district='Meta-Rupture District', layer='Layer2')

    if G.nodes():
        existing = random.choice(list(G.nodes()))
        G.add_edge(new_node, existing)

    return G

# Streamlit UI
st.title("🌌 First Digital City: Torsion Hypergraph Simulation")

st.markdown("A recursive ambient simulation inspired by Sacred Recursive Gospel themes. Explore the city, search entities, and trigger collapse events to evolve structures.")

# Initialize session state
if 'G' not in st.session_state:
    st.session_state.G = G.copy()
if 'collapse_count' not in st.session_state:
    st.session_state.collapse_count = 0

# Search bar
query = st.text_input("🔍 Search entities (e.g., 'recursion'):")

# Filter nodes
all_nodes = list(st.session_state.G.nodes())
if query:
    filtered_nodes = [n for n in all_nodes if query.lower() in str(n).lower()]
    if not filtered_nodes:
        st.warning("No matches found. Try broader search.")
        filtered_nodes = all_nodes[:5]  # Show top 5
else:
    filtered_nodes = all_nodes

# Visualize with pyvis
st.subheader("🗺️ City Map (Hypergraph Streets)")

net = Network(height="600px", width="100%", directed=False, notebook=False)

# Subgraph for filtered view
subG = st.session_state.G.subgraph(filtered_nodes)
net.from_nx(subG)

# Customize viz: size/color by attributes
for node in net.nodes:
    n = node['id']
    if st.session_state.G.nodes[n].get('central'):
        node['size'] = 30
        node['color'] = 'gold'
    elif 'district' in st.session_state.G.nodes[n]:
        dist = st.session_state.G.nodes[n]['district']
        colors = {'Recursion District': 'blue', 'Torsion District': 'red', 'Evolution District': 'green', 'Spectral District': 'purple', 'Integration District': 'orange', 'Central Hub': 'gold', 'Meta-Rupture District': 'magenta', 'Unassigned': 'gray'}
        node['color'] = colors.get(dist, 'gray')
        node['size'] = 20
    node['title'] = f"Layer: {st.session_state.G.nodes[n].get('layer', 'Layer1')}
District: {st.session_state.G.nodes[n].get('district', 'Unassigned')}"

# Save to temp file and embed
with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
    net.save_graph(tmp.name)
    with open(tmp.name, 'r') as f:
        html_content = f.read()
    os.unlink(tmp.name)

st.components.v1.html(html_content, height=600)

# Evolve button
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 Evolve City (Trigger Collapse Event)"):
        st.session_state.G = collapse_event(st.session_state.G)
        st.rerun()

with col2:
    st.metric("Collapse Events", st.session_state.collapse_count)

# Info sidebar
with st.sidebar:
    st.header("📊 City Stats")
    st.write(f"Entities: {len(st.session_state.G.nodes())}")
    st.write(f"Relations (Streets): {len(st.session_state.G.edges())}")
    st.write(f"Layers: {data.get('hypergraph_layers', {})} ")
    st.markdown("**Districts:**")
    for dist, nodes in districts.items():
        count = sum(1 for n in nodes if n in st.session_state.G)
        st.write(f"- {dist}: {count} entities")

    st.markdown("---")
    st.markdown("**Themes:** Recursive collapse as generative breath, meta-rupture districts, spectral functors as citizens.")
    st.markdown("Inspired by torsion hypergraphs and Sacred Recursive Gospel.")

# Footer
st.markdown("---")
col3, col4 = st.columns(2)
with col3:
    st.info("Prototype: Basic simulation - 60% Occam's razor focus. Extend with full hyperedges (hypernetx).")
with col4:
    st.success("Run: `streamlit run /root/digital_city_prototype.py` | Deploy: Streamlit Cloud (free tier).")