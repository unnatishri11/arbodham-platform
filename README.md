ARBODHAM: Standard Operating Protocols (SOP)
Protocol 1: Environment & Dependency InitializationThis protocol ensures the computational workspace is configured for high-dimensional transcriptomic processing.
System Requirements: Python 3.9+ environment with at least 8GB RAM to handle large-scale interaction networks.
Library Installation: Execute pip install streamlit pandas numpy requests pyvis.
Visual Engine: Install the Graphviz system binary (v12.0+) and verify dot is accessible via the system PATH to enable ortho-edge rendering.
Protocol 2: Multi-Omic Data Ingestion & NormalizationThis protocol transforms raw genomic signals into a standardized format for cross-cancer comparison.
Input Architecture: Load the Master Node Dataset (expression metrics) and the Tissue-Specific Edge List (interactome weights).
Normalization Logic: Apply Min-Max Scaling to raw scores to bounded ranges [0, 1], incorporating a numerical constant ($\epsilon$) to prevent division-by-zero errors during batch processing.Biotype Categorization: Assign unique identifiers to each molecular entity (mRNA vs. lncRNA/miRNA) to facilitate downstream rule-based routing.
Protocol 3: The Triple Metric Scoring (TMS) PipelineThe core algorithmic protocol for identifying master regulatory drivers.
Step 1 (Magnitude): Calculate the normalized expression intensity for the specific cancer histotype.
Step 2 (Reliability): Integrate statistical confidence intervals to filter out stochastic transcriptomic noise.
Step 3 (Topology): Perform network centrality analysis to measure the node's functional influence over its biological neighbors.
Integration: Fuse these three vectors into the composite Triple Metric Score (TMS).
Protocol 4: Deterministic Clinical TranslationThis protocol maps computational outputs to real-world therapeutic strategies without relying on "black-box" probabilistic models.
Threshold Selection ($\theta$): Apply predefined quantitative hurdles; targets exceeding $\theta$ are fast-tracked for prioritization.
Therapeutic Routing:Protein-Coding: Automatically route to PROTACs or Small-Molecule inhibitors.
Non-Coding (Dark Matter): Route to Antisense Oligonucleotides (ASOs) or RNAi, bypassing traditional "druggability" constraints.
Sentinel Classification: Assign targets to Diagnostic, Prognostic, or Predictive categories based on biomarker confidence scores.
Protocol 5: Pan-Cancer Meta-Analysis & System StabilityEnsuring the framework scales across diverse oncology datasets.
Stability Check: Execute a pre-render validation on all network nodes to prevent memory overflow during high-density visualization.
Universal Driver Identification: Scan the global database to identify "Master Regulators" that satisfy priority criteria across a plurality of cancer types.
