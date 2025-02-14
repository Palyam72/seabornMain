import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class ClustermapVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Clustermap Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for the clustermap
            self.columns_to_use = st.multiselect("Select columns for the clustermap", self.columns, default=self.columns)

            # Clustermap Parameters
            self.method = st.selectbox("Clustering Method", ['average', 'single', 'complete', 'ward', 'centroid', 'median'])
            self.metric = st.selectbox("Distance Metric", ['euclidean', 'cityblock', 'cosine', 'correlation'])
            self.z_score = st.selectbox("Z-Score Normalization", [None, 0, 1])
            self.standard_scale = st.selectbox("Standard Scale", [None, 0, 1])
            self.figsize = st.slider("Figure Size", min_value=5, max_value=20, value=10)
            self.cbar_kws = st.text_input("Colorbar Keyword Arguments (JSON format)", "{}")
            self.row_cluster = st.checkbox("Cluster Rows?", value=True)
            self.col_cluster = st.checkbox("Cluster Columns?", value=True)
            self.row_colors = st.text_input("Row Colors (List/Series)", "[]")
            self.col_colors = st.text_input("Column Colors (List/Series)", "[]")
            self.mask = st.checkbox("Mask Missing Values?", value=False)
            self.dendrogram_ratio = st.slider("Dendrogram Ratio", 0.1, 0.3, 0.2)
            self.colors_ratio = st.slider("Colors Ratio", 0.01, 0.1, 0.03)
            self.cbar_pos = st.text_input("Colorbar Position", "(0.02, 0.8, 0.05, 0.18)")
            self.tree_kws = st.text_input("Tree Keyword Arguments (JSON format)", "{}")

            # Generate Plot Button
            if st.button("Generate Clustermap"):
                self.generate_plot()

        with self.tab2:
            st.header("Documents Section")
            st.subheader("Saved Plots")

            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No plots saved yet.")

    def generate_plot(self):
        # Prepare the arguments for clustermap
        plot_args = {
            'data': self.data[self.columns_to_use],
            'method': self.method,
            'metric': self.metric,
            'z_score': self.z_score,
            'standard_scale': self.standard_scale,
            'figsize': (self.figsize, self.figsize),
            'cbar_kws': eval(self.cbar_kws),  # Convert string to dictionary
            'row_cluster': self.row_cluster,
            'col_cluster': self.col_cluster,
            'row_colors': eval(self.row_colors),  # Convert string to list/series
            'col_colors': eval(self.col_colors),  # Convert string to list/series
            'mask': self.mask,
            'dendrogram_ratio': self.dendrogram_ratio,
            'colors_ratio': self.colors_ratio,
            'cbar_pos': eval(self.cbar_pos),  # Convert string to tuple
            'tree_kws': eval(self.tree_kws)  # Convert string to dictionary
        }

        fig = sns.clustermap(**plot_args)

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
