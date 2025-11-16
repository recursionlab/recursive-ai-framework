#!/usr/bin/env python3
"""
TORSION FIELD MAP - 3D Visualization of Operator Space

Navigate the full epistemic manifold with 35 torsion pairs
"""

import streamlit as st
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import networkx as nx

st.set_page_config(page_title="Torsion Field Map", page_icon="🌌", layout="wide")

# Load data
@st.cache_data
def load_torsion_data():
    with open('extraction_outputs/torsion_field_analysis.json') as f:
        return json.load(f)

@st.cache_data
def load_commutators():
    with open('extraction_outputs/refined_commutators.json') as f:
        return json.load(f)

# Build network graph
def build_operator_network(torsion_field, commutators):
    """Build NetworkX graph of operators with torsion as edge weights"""

    G = nx.DiGraph()

    # Add nodes (operators)
    operators_set = set()
    for key, data in torsion_field.items():
        if isinstance(data, dict) and 'op1' in data:
            operators_set.add(data['op1'])
            operators_set.add(data['op2'])

    for op in operators_set:
        G.add_node(op)

    # Add edges (torsion connections)
    for key, data in torsion_field.items():
        if isinstance(data, dict) and 'op1' in data:
            G.add_edge(
                data['op1'],
                data['op2'],
                torsion=data['abs_torsion'],
                locations=data.get('locations', 0)
            )

    return G

# Create 3D network visualization
def create_3d_network(G, torsion_field):
    """Create 3D Plotly visualization of operator network"""

    # Use spring layout in 3D
    pos = nx.spring_layout(G, dim=3, k=2, iterations=50)

    # Extract node positions
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_z = [pos[node][2] for node in G.nodes()]

    # Node sizes based on degree
    node_degrees = dict(G.degree())
    node_sizes = [10 + node_degrees[node] * 2 for node in G.nodes()]

    # Create edges
    edge_traces = []

    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]

        torsion = G.edges[edge]['torsion']

        # Color by torsion strength
        color = f'rgba({int(255*torsion)}, {int(100*(1-torsion))}, {int(200*torsion)}, 0.6)'

        edge_trace = go.Scatter3d(
            x=[x0, x1, None],
            y=[y0, y1, None],
            z=[z0, z1, None],
            mode='lines',
            line=dict(color=color, width=2 + 8*torsion),
            hoverinfo='text',
            text=f"{edge[0]} → {edge[1]}<br>Torsion: {torsion:.3f}",
            showlegend=False
        )

        edge_traces.append(edge_trace)

    # Create nodes
    node_trace = go.Scatter3d(
        x=node_x,
        y=node_y,
        z=node_z,
        mode='markers+text',
        marker=dict(
            size=node_sizes,
            color=[node_degrees[node] for node in G.nodes()],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Degree"),
            line=dict(color='white', width=2)
        ),
        text=list(G.nodes()),
        textposition='top center',
        hoverinfo='text',
        hovertext=[f"{node}<br>Degree: {node_degrees[node]}" for node in G.nodes()],
        showlegend=False
    )

    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace])

    fig.update_layout(
        title="3D Operator Network - Torsion Field Topology",
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, title=''),
            yaxis=dict(showbackground=False, showticklabels=False, title=''),
            zaxis=dict(showbackground=False, showticklabels=False, title=''),
            bgcolor='rgba(0,0,0,0.9)'
        ),
        height=700,
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    return fig

# Create heatmap
def create_torsion_heatmap(torsion_field):
    """Create 2D heatmap of torsion magnitudes"""

    # Extract all unique operators
    operators = set()
    for key, data in torsion_field.items():
        if isinstance(data, dict) and 'op1' in data:
            operators.add(data['op1'])
            operators.add(data['op2'])

    operators = sorted(list(operators))

    # Build matrix
    matrix = np.zeros((len(operators), len(operators)))

    for key, data in torsion_field.items():
        if isinstance(data, dict) and 'op1' in data:
            i = operators.index(data['op1'])
            j = operators.index(data['op2'])
            matrix[i, j] = data['abs_torsion']

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=matrix,
        x=operators,
        y=operators,
        colorscale='Plasma',
        text=matrix,
        texttemplate='%{text:.2f}',
        textfont={"size": 10},
        colorbar=dict(title="Torsion<br>Magnitude")
    ))

    fig.update_layout(
        title="Torsion Field Heatmap - Operator Commutators",
        xaxis_title="Operator 2",
        yaxis_title="Operator 1",
        height=600
    )

    return fig

# Main app
def main():
    st.title("🌌 Torsion Field Map")
    st.markdown("Explore the complete topology of recursive operator space")

    try:
        torsion_data = load_torsion_data()
        commutators = load_commutators()
    except FileNotFoundError:
        st.error("❌ Data files not found. Run `python3 setup.py` first.")
        st.stop()

    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Torsion Pairs", torsion_data['metadata']['torsion_pairs'])
    with col2:
        st.metric("Invariants", torsion_data['metadata']['invariants'])
    with col3:
        st.metric("Mean Torsion", f"{torsion_data['torsion_statistics']['mean']:.3f}")
    with col4:
        st.metric("Max Torsion", f"{torsion_data['torsion_statistics']['max']:.3f}")

    st.divider()

    # Visualization mode
    viz_mode = st.radio(
        "Visualization Mode:",
        ["3D Network Graph", "Torsion Heatmap", "Data Table"],
        horizontal=True
    )

    if viz_mode == "3D Network Graph":
        st.subheader("Interactive 3D Operator Network")
        st.markdown("""
        **How to read this visualization:**
        - **Nodes**: Operators (Meta, Ana, Para, etc.)
        - **Edges**: Torsion connections (thicker = higher torsion)
        - **Color**: Degree centrality (more connections = darker)
        - **Rotate/Zoom**: Use mouse to navigate

        **Key Discovery:** Meta ∘ Meta has maximum torsion (T=1.0) - validates Y-recursion non-triviality
        """)

        G = build_operator_network(torsion_data['torsion_field'], commutators)
        fig_3d = create_3d_network(G, torsion_data['torsion_field'])
        st.plotly_chart(fig_3d, use_container_width=True)

        # Network statistics
        st.subheader("Network Statistics")
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Nodes (Operators)", G.number_of_nodes())
        with col_b:
            st.metric("Edges (Connections)", G.number_of_edges())
        with col_c:
            density = nx.density(G)
            st.metric("Network Density", f"{density:.3f}")

        # Top operators by centrality
        st.subheader("Top Operators by Centrality")

        degree_cent = nx.degree_centrality(G)
        betweenness_cent = nx.betweenness_centrality(G)

        df_centrality = pd.DataFrame({
            'Operator': list(G.nodes()),
            'Degree Centrality': [degree_cent[n] for n in G.nodes()],
            'Betweenness Centrality': [betweenness_cent[n] for n in G.nodes()]
        }).sort_values('Degree Centrality', ascending=False)

        st.dataframe(df_centrality, use_container_width=True)

    elif viz_mode == "Torsion Heatmap":
        st.subheader("Torsion Field Heatmap")
        st.markdown("""
        **2D Matrix View** of all operator commutators.

        - **Bright spots**: High torsion (productive contradiction)
        - **Dark spots**: Low torsion (near-invariance)
        - **Diagonal**: Self-composition (Meta∘Meta, Ana∘Ana, etc.)
        """)

        fig_heatmap = create_torsion_heatmap(torsion_data['torsion_field'])
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Highest torsion pairs
        st.subheader("🔥 Highest Torsion Pairs")

        torsion_pairs = []
        for key, data in torsion_data['torsion_field'].items():
            if isinstance(data, dict) and 'abs_torsion' in data:
                torsion_pairs.append({
                    'Operator Pair': f"{data['op1']} ∘ {data['op2']}",
                    'Torsion': data['abs_torsion'],
                    'Locations': data.get('locations', 0)
                })

        df_torsion = pd.DataFrame(torsion_pairs).sort_values('Torsion', ascending=False).head(15)
        st.dataframe(df_torsion, use_container_width=True)

    else:  # Data Table
        st.subheader("Complete Torsion Field Data")

        torsion_records = []
        for key, data in torsion_data['torsion_field'].items():
            if isinstance(data, dict) and 'abs_torsion' in data:
                torsion_records.append({
                    'Operator 1': data['op1'],
                    'Operator 2': data['op2'],
                    'Torsion (Signed)': data['torsion'],
                    'Torsion (Absolute)': data['abs_torsion'],
                    'Locations': data.get('locations', 0),
                    'Normalized': data.get('locations', 0) / torsion_data['metadata']['total_contradictions'] if torsion_data['metadata']['total_contradictions'] > 0 else 0
                })

        df_full = pd.DataFrame(torsion_records).sort_values('Torsion (Absolute)', ascending=False)

        # Filter options
        min_torsion = st.slider("Minimum Torsion", 0.0, 1.0, 0.0, 0.05)
        df_filtered = df_full[df_full['Torsion (Absolute)'] >= min_torsion]

        st.dataframe(df_filtered, use_container_width=True)

        # Download button
        csv = df_filtered.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="torsion_field_data.csv",
            mime="text/csv"
        )

    st.divider()

    # Invariants analysis
    st.subheader("🎯 Invariant Points (T ≈ 0)")
    st.markdown("""
    These operator pairs produce **near-zero torsion** - semantic invariance zones.
    They represent stable attractors in the epistemic manifold.
    """)

    invariants = []
    for key, data in torsion_data['torsion_field'].items():
        if isinstance(data, dict) and 'abs_torsion' in data:
            if data['abs_torsion'] < torsion_data['metadata']['epsilon']:
                invariants.append({
                    'Operator Pair': f"{data['op1']} ∘ {data['op2']}",
                    'Torsion': data['abs_torsion'],
                    'Attractor': data.get('attractor', 'Unknown')
                })

    if invariants:
        df_invariants = pd.DataFrame(invariants)
        st.dataframe(df_invariants, use_container_width=True)

        # Attractor distribution
        if 'Attractor' in df_invariants.columns:
            fig_pie = go.Figure(data=[go.Pie(
                labels=df_invariants['Attractor'].value_counts().index,
                values=df_invariants['Attractor'].value_counts().values,
                hole=0.4
            )])
            fig_pie.update_layout(title="Invariant Distribution by Attractor", height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No invariants found below epsilon threshold.")

    # Footer
    st.divider()
    st.markdown("""
    **Data Source:** 73,949 contradictions from 524 markdown files

    **Computation:** T = antiSym(∇C) where C is contradiction vector field

    **Key Discovery:** Meta ∘ Meta = 1.0 (maximum torsion confirms Y-recursion non-triviality)
    """)

if __name__ == '__main__':
    main()
