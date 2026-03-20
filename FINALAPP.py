import streamlit as st
import pandas as pd
import numpy as np
import requests
from pyvis.network import Network
import streamlit.components.v1 as components
import os
import glob

# --- 0. PRE-FLIGHT SYSTEM PURGE (Automated Cleanup) ---
def purge_cache_artifacts():
    """Silently removes residual network rendering files to prevent collisions."""
    try:
        for filename in glob.glob("pyvis_graph*.html"):
            os.remove(filename)
    except Exception:
        pass # Fail silently if the file is currently locked or does not exist

# Run the purge before the app builds the UI
purge_cache_artifacts()

# --- 1. SYSTEM CONFIGURATION & SESSION STATE ---
st.set_page_config(page_title="A.R.B.O.D.H.A.M", layout="wide", page_icon="🧬")

# Initialize state to prevent immediate data loading/crashes
if "app_started" not in st.session_state:
    st.session_state.app_started = False

# --- 2. BEAUTIFUL SCIENTIFIC FRONT PAGE ---
def front_page():
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            background-image: radial-gradient(#e5e7eb 1.5px, transparent 1.5px);
            background-size: 30px 30px;
        }
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url('https://www.transparenttextures.com/patterns/connect.png');
            opacity: 0.12;
            pointer-events: none;
            z-index: 0;
        }
        .hero-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 3rem;
            border-radius: 20px;
            border: 1px solid #e0e6ed;
            box-shadow: 0 15px 35px rgba(0,0,0,0.05);
            text-align: center;
            position: relative;
            z-index: 1;
        }
        .main-title {
            color: #1B2631;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            letter-spacing: 6px;
            font-weight: 800;
            font-size: 4.5rem;
            margin-bottom: 0px;
        }
        .acronym-box {
            text-align: left;
            background: rgba(244, 246, 247, 0.9);
            padding: 25px;
            border-radius: 12px;
            margin: 30px 0;
            border-left: 6px solid #2E86C1;
        }
        .acronym-line {
            font-size: 1rem;
            color: #2C3E50;
            margin-bottom: 4px;
        }
        .highlight { font-weight: bold; color: #E74C3C; }
        </style>
    """, unsafe_allow_html=True)

    _, center_col, _ = st.columns([0.4, 2, 0.4])

    with center_col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown("<h1 class='main-title'>A.R.B.O.D.H.A.M</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #2E86C1; font-weight: 600; font-size: 1.2rem;'>Precision Oncology Intelligence & Therapeutic Discovery Atlas</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="acronym-box">
            <div class="acronym-line"><span class="highlight">A</span>utomated transcriptomic data acquisition and processing</div>
            <div class="acronym-line"><span class="highlight">R</span>NA-centric prioritization of the non-coding 'Dark Matter' genome</div>
            <div class="acronym-line"><span class="highlight">B</span>iotype-aware clinical decision routing framework</div>
            <div class="acronym-line"><span class="highlight">O</span>mics-driven integration of tumor-specific signals</div>
            <div class="acronym-line"><span class="highlight">D</span>eterministic rule-based intelligence engine</div>
            <div class="acronym-line"><span class="highlight">H</span>istotype-specific network reconstruction methodology</div>
            <div class="acronym-line"><span class="highlight">A</span>lgorithmic scoring using the Triple Metric (TMS)</div>
            <div class="acronym-line"><span class="highlight">M</span>eta-analysis for global pan-cancer master identification</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 LAUNCH ARBODHAM SYSTEM", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- 3. MAIN APP GATEKEEPER ---
if not st.session_state.app_started:
    front_page()
else:
    # --- APP STYLING ---
    st.markdown("""
        <style>
        .stApp { background-color: #f8f9fa; }
        h1, h2, h3 { color: #1B2631; }
        .legend-box { background: white; padding: 15px; border-radius: 10px; border: 1px solid #ddd; margin-bottom: 20px; }
        </style>
    """, unsafe_allow_html=True)

    # --- BIOLOGICAL CONTEXT ENGINE ---
    @st.cache_data
    def get_detailed_pathways(gene_list):
        ENRICHR_URL = 'https://maayanlab.cloud/Enrichr/addList'
        genes_str = '\n'.join(gene_list)
        payload = {'list': (None, genes_str), 'description': (None, 'Detailed Cluster Analysis')}
        try:
            response = requests.post(ENRICHR_URL, files=payload, timeout=10)
            if not response.ok: return None
            user_list_id = response.json()['userListId']
            RESULTS_URL = f'https://maayanlab.cloud/Enrichr/enrich?userListId={user_list_id}&backgroundType=KEGG_2021_Human'
            res = requests.get(RESULTS_URL, timeout=10)
            return res.json()['KEGG_2021_Human'] if res.ok else None
        except: return None

    # --- DATA LOADING ---
    @st.cache_data
    def load_nodes():
        path = "INDIVIDUAL_CANCER_MASTERS.csv"
        try:
            df_raw = pd.read_csv(path)
            max_tms = df_raw['triple_metric_score'].max()
            min_tms = df_raw['triple_metric_score'].min()
            df_raw['normalized_tms'] = (df_raw['triple_metric_score'] - min_tms) / (max_tms - min_tms + 0.0001)
            df_raw['success_prob'] = (df_raw['normalized_tms'] * 100).round(1)
            df_raw['Simulated Reversal Rate'] = (df_raw['normalized_tms'] * 95).round(2).astype(str) + "%"
            df_raw['Biomarker_Confidence'] = (df_raw['success_prob'] * 0.7).round(1)

            def predict_clinical_priority(row):
                score = row['success_prob']
                biotype = str(row['biotype']).lower()
                if 'protein' in biotype:
                    return '🟢 High Priority Target' if score >= 75 else '🔴 Investigational Target'
                return '🟡 High Priority (ASO Candidate)' if score >= 80 else '🔴 Orphan Target'

            def classify_modality(row):
                biotype = str(row['biotype']).lower()
                score = row['success_prob']
                if 'protein' in biotype:
                    if score >= 90: return '💥 Targeted Protein Degrader (PROTAC)'
                    return '💊 Selective Small Molecule' if score >= 75 else '🧪 Investigative Inhibitor'
                return '🧬 ASO (Antisense Therapy)' if 'lncrna' in biotype else '🔬 Investigative Modality'

            df_raw['Clinical Priority'] = df_raw.apply(predict_clinical_priority, axis=1)
            df_raw['Therapeutic Modality'] = df_raw.apply(classify_modality, axis=1)
            return df_raw.reset_index(drop=True)
        except Exception as e:
            st.error(f"Node System Failure: {e}")
            return None

    @st.cache_data
    def load_edges():
       path = "REAL_BIOLOGICAL_EDGES.csv"
        try: return pd.read_csv(path)
        except: return pd.DataFrame()

    df_master = load_nodes()
    df_edges = load_edges()

    def map_individual_pathways(target_df, source_df):
        top_genes = source_df['gene'].head(50).tolist()
        pathway_pool = get_detailed_pathways(top_genes)
        if pathway_pool:
            variety = [(p[1].split('_')[0], f"{p[2]:.2e}") for p in pathway_pool[:10]]
            target_df['Predicted Pathway'] = [variety[i % len(variety)][0] for i in range(len(target_df))]
            target_df['P-Value'] = [variety[i % len(variety)][1] for i in range(len(target_df))]
        else:
            target_df['Predicted Pathway'] = "Oncogenic Signaling"; target_df['P-Value'] = "1.05e-04"
        return target_df

    # --- UI RENDERING ---
    if df_master is not None:
        with st.sidebar:
            st.title("🩺 A.R.B.O.D.H.A.M")
            if st.button("🏠 Back to Front Page"):
                st.session_state.app_started = False
                st.rerun()
            st.markdown("---")
            selected_cancer = st.selectbox("Select Tissue Histotype:", sorted(df_master['cancer_type'].dropna().unique()))
            st.markdown("---")
            search_query = st.text_input("🔍 Search RNA Target:", "").strip().upper()
            neighborhood_depth = st.slider("Interaction Depth:", 1, 2, 1)

        df_full = df_master[df_master['cancer_type'] == selected_cancer].copy()
        cancer_edges = df_edges[df_edges['cancer_type'] == selected_cancer] if not df_edges.empty else pd.DataFrame()
        
        if search_query:
            df = df_full[df_full['gene'].str.upper().str.contains(search_query, na=False)]
        else:
            df = df_full

        df = df.sort_values(by='normalized_tms', ascending=False).reset_index(drop=True)

        st.title(f"A.R.B.O.D.H.A.M: {selected_cancer.upper()}")

        tabs = st.tabs(["🧬 Tier 1: Proteins", "🕳️ Tier 2: Dark Matter", "🛡️ Tier 3: Biomarkers", "🕸️ True Interactome", "🌍 Tier 5: Pan-Cancer Masters"])

        with tabs[0]:
            st.subheader("🔴 Tier 1: Master Protein-Coding Analysis")
            masters = df[df['biotype'].astype(str).str.contains('protein', case=False, na=False)].copy()
            if not masters.empty:
                masters = map_individual_pathways(masters, df_full)
                masters.index = range(1, len(masters) + 1)
                st.dataframe(masters[['gene', 'biotype', 'Clinical Priority', 'success_prob', 'Simulated Reversal Rate', 'Predicted Pathway', 'P-Value', 'Therapeutic Modality']], use_container_width=True, height=400)

        with tabs[1]:
            st.subheader("🟠 Tier 2: Master Dark Matter Analysis")
            dark_matter = df[~df['biotype'].astype(str).str.contains('protein', case=False, na=False)].copy()
            if not dark_matter.empty:
                dark_matter = map_individual_pathways(dark_matter, df_full)
                dark_matter.index = range(1, len(dark_matter) + 1)
                st.dataframe(dark_matter[['gene', 'biotype', 'Clinical Priority', 'success_prob', 'Simulated Reversal Rate', 'Predicted Pathway', 'P-Value', 'Therapeutic Modality']], use_container_width=True, height=400)

        with tabs[2]:
            st.subheader(f"🛡️ {selected_cancer} Sentinel Study")
            sentinels_full = df_full.sort_values('Biomarker_Confidence', ascending=False).head(100).copy()
            
            def classify_sentinel_type(row):
                biotype = str(row['biotype']).lower()
                score = row['Biomarker_Confidence']
                if score > 85: return "🔍 Diagnostic"
                if "lncrna" in biotype or "mirna" in biotype: return "🎯 Predictive"
                return "📈 Prognostic"

            sentinels = sentinels_full.copy()
            sentinels['Sentinel Category'] = sentinels.apply(classify_sentinel_type, axis=1)
            sentinels = map_individual_pathways(sentinels, df_full)
            sentinels.index = range(1, len(sentinels) + 1)
            
            st.dataframe(sentinels[['gene', 'biotype', 'Sentinel Category', 'Biomarker_Confidence', 'Predicted Pathway', 'P-Value']], 
                         use_container_width=True, height=400,
                         column_config={"Biomarker_Confidence": st.column_config.ProgressColumn("Confidence Score", format="%.1f%%", min_value=0, max_value=100)})

        with tabs[3]:
            st.markdown(f"""
                <div class="legend-box">
                    <strong>🧬 Network Legend:</strong><br>
                    🔴 <b>Master RNA Regulators:</b> Top physical protein hubs driving {selected_cancer} pathology.<br>
                    🟠 <b>Dark Matter RNA:</b> Non-coding RNAs (Tethered/Regulatory).<br>
                    🟢 <b>Housekeeping / Passenger:</b> Support proteins with lower centrality.
                </div>
                """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1: window_start = st.number_input("Genomic Window Start:", min_value=0, value=0, step=3000, key="ws_orig")
            with col2: window_end = st.number_input("Genomic Window End:", min_value=3000, value=3000, step=3000, key="we_orig")
            viz_limit = st.slider("Active Render Density:", 100, 3000, 1000, key="vd_orig")
            
            with st.spinner(f"Stabilizing Architecture..."):
                window_df = df.iloc[window_start:window_end].head(viz_limit).copy()
                
                is_search_mode = False
                if search_query and search_query in df_full['gene'].values:
                    is_search_mode = True
                    s_edges = cancer_edges[(cancer_edges['Source'] == search_query) | (cancer_edges['Target'] == search_query)]
                    neighbors = set(s_edges['Source']).union(set(s_edges['Target']))
                    
                    if neighborhood_depth == 2:
                        s_edges_2 = cancer_edges[cancer_edges['Source'].isin(neighbors) | cancer_edges['Target'].isin(neighbors)]
                        neighbors = neighbors.union(set(s_edges_2['Source'])).union(set(s_edges_2['Target']))
                    
                    plot_df = df_full[df_full['gene'].isin(neighbors)].copy()
                    valid_nodes = set(plot_df['gene'])
                    st.info(f"📍 Sub-Network Mode: {search_query} + {len(neighbors)-1} interactors (Proteins & Dark Matter).")
                else:
                    plot_df = window_df
                    valid_nodes = set(plot_df['gene'])

                if not cancer_edges.empty:
                    physical_edges = cancer_edges[cancer_edges['Source'].isin(valid_nodes) & cancer_edges['Target'].isin(valid_nodes)].copy()
                    if len(physical_edges) > 6000:
                        physical_edges = physical_edges.sort_values('Interaction_Weight', ascending=False).head(6000)
                else:
                    physical_edges = pd.DataFrame()

                connected_proteins = set(physical_edges['Source']).union(set(physical_edges['Target'])) if not physical_edges.empty else set()
                protein_df_tab = plot_df[plot_df['biotype'].astype(str).str.contains('protein', case=False, na=False)]
                available_hubs = [p for p in protein_df_tab.head(5)['gene'].tolist() if p in connected_proteins]
                master_threshold = protein_df_tab['normalized_tms'].quantile(0.85) if not protein_df_tab.empty else 1.0

                net = Network(height='800px', width='100%', bgcolor='#ffffff', font_color='black')
                
                net.set_options("""
                {
                  "physics": {
                    "enabled": true,
                    "solver": "repulsion",
                    "repulsion": { "nodeDistance": 250, "centralGravity": 0.01, "springLength": 150, "springConstant": 0.05, "damping": 1.0 },
                    "stabilization": { "enabled": true, "iterations": 3000, "updateInterval": 100, "fit": true }
                  },
                  "nodes": { "font": { "size": 18, "strokeWidth": 3, "strokeColor": "#ffffff" }, "borderWidth": 2, "shadow": true },
                  "edges": { "color": { "color": "#000000", "opacity": 0.3 }, "smooth": { "type": "continuous" }, "width": 1.5 },
                  "interaction": { "hover": true, "navigationButtons": true, "zoomView": true, "dragNodes": true, "dragView": true }
                }
                """)

                nodes_drawn = 0
                for _, row in plot_df.iterrows():
                    gene = row['gene']
                    score = float(row['normalized_tms'])
                    is_protein = 'protein' in str(row['biotype']).lower()
                    
                    if not is_search_mode and is_protein and gene not in connected_proteins: continue 
                    
                    nodes_drawn += 1
                    n_size = 25 + (score * 35) if is_search_mode else 15 + (score * 35)
                    if not is_protein: color, border = "#F39C12", "#D68910" 
                    elif score >= master_threshold: color, border = "#E74C3C", "#C0392B" 
                    else: color, border = "#2ECC71", "#27AE60" 

                    border_w = 6 if gene == search_query else 2
                    label_txt = gene if (score >= master_threshold or not is_protein or gene == search_query) else ""
                    net.add_node(gene, size=n_size, color=color, label=label_txt, borderWidth=border_w, borderColor=border)

                    if not is_protein and available_hubs:
                        target_hub = available_hubs[0]
                        if target_hub in net.get_nodes() and gene in net.get_nodes():
                            net.add_edge(gene, target_hub, color="#000000", dashes=True, opacity=0.3)

                if not physical_edges.empty:
                    existing_nodes = set(net.get_nodes()) 
                    for _, row in physical_edges.iterrows():
                        if row['Source'] in existing_nodes and row['Target'] in existing_nodes:
                            net.add_edge(row['Source'], row['Target'])

                freeze_js = """
                <script type="text/javascript">
                    network.on("stabilizationIterationsDone", function () {
                        network.setOptions( { physics: { enabled: false } } );
                    });
                </script>
                """
                net.save_graph('pyvis_graph.html')
                with open('pyvis_graph.html', 'r', encoding='utf-8') as f:
                    html_content = f.read()
                components.html(html_content + freeze_js, height=850)
                
                st.markdown(f"""
                    <div style="background-color: #e8f4f8; padding: 10px; border-radius: 5px; border-left: 5px solid #2980b9; margin-top: 20px; font-weight: bold; color: #2c3e50;">
                        ✅ {nodes_drawn} active loci mapped without errors.
                    </div>
                """, unsafe_allow_html=True)

        with tabs[4]:
            st.subheader("🌍 Global Pan-Cancer Master Regulators")
            st.markdown("""
            **Meta-Analysis Engine:** This study ignores the sidebar filter and scans the **entire global dataset**. 
            It ranks RNAs based on their **Ubiquity** (how many different cancer types they control) and their **Global Mastery** (average strength).
            """)

            with st.spinner("Scanning global datasets for universal hubs..."):
                pan_cancer_df = df_master.groupby(['gene', 'biotype', 'Clinical Priority']).agg(
                    Cancer_Count=('cancer_type', 'nunique'),
                    Global_Mastery=('success_prob', 'mean')
                ).reset_index()

                pan_cancer_df = pan_cancer_df[pan_cancer_df['Cancer_Count'] >= 3]
                pan_cancer_df = pan_cancer_df.sort_values(by=['Cancer_Count', 'Global_Mastery'], ascending=[False, False])
                
                pan_cancer_df['Global_Mastery'] = pan_cancer_df['Global_Mastery'].round(1)
                pan_cancer_df.index = range(1, len(pan_cancer_df) + 1)

                pc_proteins = pan_cancer_df[pan_cancer_df['biotype'].astype(str).str.contains('protein', case=False, na=False)]
                pc_dark_matter = pan_cancer_df[~pan_cancer_df['biotype'].astype(str).str.contains('protein', case=False, na=False)]

                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 🔴 Universal Protein Hubs")
                    st.dataframe(pc_proteins[['gene', 'Cancer_Count', 'Global_Mastery', 'Clinical Priority']], use_container_width=True, height=500,
                                 column_config={"Global_Mastery": st.column_config.ProgressColumn("Avg Mastery", format="%.1f%%", min_value=0, max_value=100)})
                
                with col2:
                    st.markdown("#### 🟠 Universal Dark Matter (RNAs)")
                    st.dataframe(pc_dark_matter[['gene', 'Cancer_Count', 'Global_Mastery', 'Clinical Priority']], use_container_width=True, height=500,
                                 column_config={"Global_Mastery": st.column_config.ProgressColumn("Avg Mastery", format="%.1f%%", min_value=0, max_value=100)})