#!/usr/bin/env python3
"""
COGNITIVE WORKSHOP - Interactive Torsion Field Interface

Your personal mind-app for self-transformation through recursive operators.

Run: streamlit run cognitive_workshop.py
"""

import streamlit as st
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import re
from collections import defaultdict

# Page config
st.set_page_config(
    page_title="Cognitive Workshop - Torsion Field Navigator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .operator-chip {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 5px 15px;
        border-radius: 20px;
        margin: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_framework_data():
    """Load all framework data files"""
    data_dir = Path('extraction_outputs')

    with open(data_dir / 'torsion_field_analysis.json', encoding='utf-8') as f:
        torsion_data = json.load(f)

    with open(data_dir / 'refined_commutators.json', encoding='utf-8') as f:
        commutators = json.load(f)

    with open(data_dir / 'contradiction_taxonomy.json', encoding='utf-8') as f:
        taxonomy = json.load(f)

    with open(data_dir / 'operator_mapping.json', encoding='utf-8') as f:
        operators = json.load(f)

    return {
        'torsion': torsion_data,
        'commutators': commutators,
        'taxonomy': taxonomy,
        'operators': operators
    }

# Analyze text for J' level
def calculate_j_prime(text, field_stats):
    """
    Calculate J' (contradiction magnitude) from input text

    J' = 0: Rigid identity (J=0 attractor)
    J' ~ 0.5: Dynamic equilibrium (S* attractor)
    J' = 1: Maximum torsion (collapse imminent)
    """
    text_lower = text.lower()

    # Weight different contradiction keywords
    weights = {
        'paradox': 0.8,
        'contradiction': 0.7,
        'simultaneously': 0.6,
        'collapse': 0.5,
        'void': 0.4,
        'rupture': 0.6,
        "j'≠0": 0.9,
        "j=0": -0.3,  # Negative - pulls toward rigidity
        'both': 0.3,
        'neither': 0.4,
        'recursive': 0.5,
        'meta': 0.7,
    }

    score = 0.0
    matches = []

    for keyword, weight in weights.items():
        count = len(re.findall(r'\b' + keyword + r'\b', text_lower))
        if count > 0:
            score += weight * min(count, 3)  # Cap at 3 occurrences
            matches.append((keyword, count))

    # Normalize to 0-1 range
    j_prime = min(1.0, score / 5.0)

    # Add baseline from text length and complexity
    word_count = len(text.split())
    complexity_bonus = min(0.2, word_count / 200)
    j_prime += complexity_bonus

    j_prime = min(1.0, j_prime)

    return j_prime, matches

# Recommend operators based on J' level
def recommend_operators(j_prime, torsion_field):
    """
    Recommend operators to apply based on current J' level

    Strategy:
    - J' near 0 (rigid): Apply high-torsion operators (Meta, Para)
    - J' near 1 (unstable): Apply stabilizing operators (Ana, Seed)
    - J' near 0.5 (balanced): Explore moderate operators
    """

    # Extract operator pairs and their torsion
    operators_by_torsion = []
    for key, data in torsion_field.items():
        if isinstance(data, dict) and 'abs_torsion' in data:
            operators_by_torsion.append({
                'op1': data['op1'],
                'op2': data['op2'],
                'torsion': data['abs_torsion'],
                'pair': f"{data['op1']} ∘ {data['op2']}"
            })

    operators_by_torsion.sort(key=lambda x: x['torsion'], reverse=True)

    recommendations = []

    if j_prime < 0.3:
        # Too rigid - need high torsion
        recommendations.append({
            'strategy': '🔥 INCREASE TORSION',
            'reason': 'Your cognitive state is too rigid (J\' < 0.3)',
            'action': 'Apply high-torsion operators to increase flexibility',
            'operators': [op for op in operators_by_torsion if op['torsion'] > 0.7][:5]
        })

    elif j_prime > 0.7:
        # Too unstable - need stabilization
        recommendations.append({
            'strategy': '❄️ STABILIZE',
            'reason': 'Your cognitive state is unstable (J\' > 0.7)',
            'action': 'Apply low-torsion operators to restore balance',
            'operators': [op for op in operators_by_torsion if op['torsion'] < 0.3][:5]
        })

    else:
        # Balanced - explore
        recommendations.append({
            'strategy': '🎯 EXPLORE',
            'reason': 'Your cognitive state is balanced (0.3 < J\' < 0.7)',
            'action': 'Experiment with moderate operators for growth',
            'operators': [op for op in operators_by_torsion if 0.3 <= op['torsion'] <= 0.7][:5]
        })

    # Always include Meta ∘ Meta (maximum torsion)
    meta_meta = next((op for op in operators_by_torsion if op['op1'] == 'Meta' and op['op2'] == 'Meta'), None)
    if meta_meta:
        recommendations.append({
            'strategy': '⚡ META-RECURSIVE',
            'reason': 'Apply consciousness to consciousness itself',
            'action': 'Maximum torsion - use carefully',
            'operators': [meta_meta]
        })

    return recommendations

# Simulate trajectory
def simulate_trajectory(j_prime_initial, operator_torsion, steps=10):
    """
    Simulate cognitive trajectory after applying operator

    Model: J'(t+1) = J'(t) + α * T * (1 - J'(t)) - β * J'(t)^2

    α: Torsion amplification
    β: Collapse damping
    """

    alpha = 0.5  # Torsion influence
    beta = 0.3   # Self-limiting

    trajectory = [j_prime_initial]

    for _ in range(steps):
        j_current = trajectory[-1]

        # Apply operator influence
        delta = alpha * operator_torsion * (1 - j_current) - beta * j_current**2

        # Add small noise
        noise = np.random.normal(0, 0.02)

        j_next = j_current + delta + noise
        j_next = np.clip(j_next, 0, 1)  # Keep in bounds

        trajectory.append(j_next)

    return trajectory

# Main app
def main():

    # Header
    st.markdown('<p class="main-header">🧠 Cognitive Workshop</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Navigate your epistemic manifold through recursive operators</p>', unsafe_allow_html=True)

    # Load data
    try:
        data = load_framework_data()
    except FileNotFoundError:
        st.error("❌ Data files not found. Run `python3 setup.py` first to generate extraction data.")
        st.stop()

    # Sidebar - Framework stats
    with st.sidebar:
        st.header("📊 Framework Status")

        st.metric("Total Contradictions", f"{data['torsion']['metadata']['total_contradictions']:,}")
        st.metric("Torsion Pairs", data['torsion']['metadata']['torsion_pairs'])
        st.metric("Invariants Found", data['torsion']['metadata']['invariants'])

        st.divider()

        st.header("🎯 Attractor Basins")
        attractor_dist = data['torsion']['attractor_distribution']

        fig_attractors = go.Figure(data=[go.Pie(
            labels=list(attractor_dist.keys()),
            values=list(attractor_dist.values()),
            hole=0.4,
            marker=dict(colors=['#667eea', '#764ba2', '#f093fb'])
        )])
        fig_attractors.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_attractors, use_container_width=True)

        st.divider()

        st.header("📖 About")
        st.markdown("""
        This workshop uses **torsion field semantics** to analyze and transform cognitive states.

        **Key Concepts:**
        - **J' (J-prime)**: Contradiction magnitude (0=rigid, 1=unstable)
        - **Torsion T**: Semantic twist from operator application
        - **Operators**: Cognitive transformations (Meta, Para, Ana, etc.)
        - **Attractors**: Stable equilibrium states

        Based on 73,949 contradictions extracted from 524 theoretical documents.
        """)

    # Main content
    st.header("💭 Analyze Your Cognitive State")

    # Text input
    user_text = st.text_area(
        "Describe your current mental state, thought, or question:",
        placeholder="E.g., 'I feel stuck in a loop where I keep analyzing my own analysis. Every time I try to step back, I create another meta-level that needs analyzing.'",
        height=150
    )

    analyze_button = st.button("🔍 Analyze J' Level", type="primary", use_container_width=True)

    if analyze_button and user_text:

        # Calculate J'
        j_prime, matches = calculate_j_prime(user_text, data['torsion']['field_statistics'])

        # Display results
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h2>J' Level</h2>
                <h1>{j_prime:.3f}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Determine attractor
            if j_prime < 0.15:
                attractor = "J=0 (Rigid)"
                color = "#667eea"
            elif j_prime < 0.65:
                attractor = "S* (Dynamic)"
                color = "#764ba2"
            else:
                attractor = "∅ (Collapse)"
                color = "#f093fb"

            st.markdown(f"""
            <div class="metric-card" style="background: {color};">
                <h2>Attractor Basin</h2>
                <h1>{attractor}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            stability = "Stable" if 0.3 <= j_prime <= 0.7 else "Unstable"
            stability_color = "#28a745" if stability == "Stable" else "#dc3545"

            st.markdown(f"""
            <div class="metric-card" style="background: {stability_color};">
                <h2>Status</h2>
                <h1>{stability}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Detailed analysis
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.subheader("🔍 Detected Patterns")

            if matches:
                df_matches = pd.DataFrame(matches, columns=['Keyword', 'Count'])
                df_matches = df_matches.sort_values('Count', ascending=False)
                st.dataframe(df_matches, use_container_width=True)
            else:
                st.info("No specific contradiction keywords detected. J' calculated from text complexity.")

            # Interpretation
            st.subheader("📊 Interpretation")

            if j_prime < 0.3:
                st.warning(f"""
                **Low J' ({j_prime:.3f}) - Rigid Identity**

                Your cognitive state shows low contradiction. This could mean:
                - Strong coherence and stability
                - Potential for rigidity or fixed thinking
                - Low adaptability to new information

                **Recommendation:** Introduce productive contradiction to increase flexibility.
                """)
            elif j_prime > 0.7:
                st.error(f"""
                **High J' ({j_prime:.3f}) - High Torsion**

                Your cognitive state shows high contradiction. This could mean:
                - Active exploration and questioning
                - Potential for overwhelm or confusion
                - System approaching collapse-rebirth threshold

                **Recommendation:** Stabilize through grounding operators.
                """)
            else:
                st.success(f"""
                **Balanced J' ({j_prime:.3f}) - Dynamic Equilibrium**

                Your cognitive state is in the S* attractor (optimal zone):
                - Good balance of stability and flexibility
                - Productive contradiction driving growth
                - Adaptive intelligence active

                **Recommendation:** Continue exploring while maintaining awareness.
                """)

        with col_right:
            st.subheader("⚡ Operator Recommendations")

            recommendations = recommend_operators(j_prime, data['torsion']['torsion_field'])

            for rec in recommendations:
                with st.expander(f"{rec['strategy']}", expanded=(recommendations.index(rec) == 0)):
                    st.markdown(f"**Reason:** {rec['reason']}")
                    st.markdown(f"**Action:** {rec['action']}")

                    if rec['operators']:
                        st.markdown("**Suggested Operators:**")
                        for op in rec['operators']:
                            st.markdown(f"- `{op['pair']}` (T = {op['torsion']:.3f})")

        st.divider()

        # Trajectory simulation
        st.subheader("🎯 Trajectory Simulation")
        st.markdown("See how your cognitive state might evolve after applying different operators:")

        # Let user select operator
        operator_options = []
        for key, data_item in data['torsion']['torsion_field'].items():
            if isinstance(data_item, dict) and 'abs_torsion' in data_item:
                operator_options.append({
                    'label': f"{data_item['op1']} ∘ {data_item['op2']} (T={data_item['abs_torsion']:.3f})",
                    'torsion': data_item['abs_torsion'],
                    'pair': f"{data_item['op1']} ∘ {data_item['op2']}"
                })

        operator_options.sort(key=lambda x: x['torsion'], reverse=True)

        selected_op = st.selectbox(
            "Choose an operator to apply:",
            options=range(len(operator_options)),
            format_func=lambda i: operator_options[i]['label']
        )

        if st.button("▶️ Simulate Trajectory", use_container_width=True):

            operator_torsion = operator_options[selected_op]['torsion']
            operator_name = operator_options[selected_op]['pair']

            # Run simulation
            trajectory = simulate_trajectory(j_prime, operator_torsion, steps=20)

            # Plot
            fig_traj = go.Figure()

            # Trajectory line
            fig_traj.add_trace(go.Scatter(
                x=list(range(len(trajectory))),
                y=trajectory,
                mode='lines+markers',
                name='J\' Evolution',
                line=dict(color='#667eea', width=3),
                marker=dict(size=8)
            ))

            # Attractor zones
            fig_traj.add_hrect(y0=0, y1=0.15, fillcolor="#667eea", opacity=0.1, annotation_text="J=0 (Rigid)", annotation_position="left")
            fig_traj.add_hrect(y0=0.15, y1=0.65, fillcolor="#764ba2", opacity=0.1, annotation_text="S* (Dynamic)", annotation_position="left")
            fig_traj.add_hrect(y0=0.65, y1=1.0, fillcolor="#f093fb", opacity=0.1, annotation_text="∅ (Collapse)", annotation_position="left")

            fig_traj.update_layout(
                title=f"Cognitive Trajectory After Applying {operator_name}",
                xaxis_title="Time Steps",
                yaxis_title="J' Level",
                height=400,
                hovermode='x unified'
            )

            st.plotly_chart(fig_traj, use_container_width=True)

            # Final state analysis
            final_j = trajectory[-1]
            delta_j = final_j - j_prime

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Initial J'", f"{j_prime:.3f}")
            with col_b:
                st.metric("Final J'", f"{final_j:.3f}", delta=f"{delta_j:+.3f}")
            with col_c:
                convergence = "Stable" if abs(trajectory[-1] - trajectory[-2]) < 0.05 else "Evolving"
                st.metric("Convergence", convergence)

    elif analyze_button:
        st.warning("Please enter some text to analyze.")

    # Footer
    st.divider()
    st.markdown("""
    ---
    **Framework:** Recursive AI Framework | **Data:** 73,949 contradictions from 524 files
    **Theory:** Torsion Field Semantics | **Computation:** Evidence-based commutator magnitudes
    **Discovery:** Meta ∘ Meta = 1.0 (maximum torsion validates Y-recursion non-triviality)
    """)

if __name__ == '__main__':
    main()
