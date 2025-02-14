import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from itertools import cycle

class HeatmapVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots

        # Keep only numeric columns for heatmap
        self.numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["📊 Heatmap Generator", "📂 Saved Plots"])

        with self.tab1:
            st.header("📊 Heatmap Generator")
            st.info("✅ Dataset Loaded. Select Parameters to Generate a Heatmap.")
            st.dataframe(self.data)

            col1, col2 = st.columns(2)

            with col1:
                # Select numeric columns
                self.selected_columns = st.multiselect(
                    "📌 Select Numeric Columns for Heatmap", self.numeric_columns, default=self.numeric_columns
                )

                if self.selected_columns:
                    min_val = self.data[self.selected_columns].min().min()
                    max_val = self.data[self.selected_columns].max().max()
                else:
                    min_val, max_val = 0, 1  # Defaults in case of no selection

                # Ensure proper numeric values
                self.vmin = st.number_input("Min Value for Heatmap", value=float(min_val))
                self.vmax = st.number_input("Max Value for Heatmap", value=float(max_val))
                
                # Handle optional center value safely
                center_val = st.text_input("Center Value (Optional)")
                self.center = float(center_val) if center_val.strip() else None

                self.cmap = st.selectbox("Select Colormap", ['coolwarm', 'viridis', 'plasma', 'inferno', 'magma'])
                self.robust = st.checkbox("Use Robust Color Mapping?", value=False)
                self.mask = st.checkbox("Mask Upper Triangle?", value=False)

            with col2:
                # Annotation & Appearance
                self.annot = st.checkbox("Show Annotations?", value=True)
                self.fmt = st.text_input("Annotation Format", ".2g")
                self.annot_kws = {"size": st.slider("Annotation Font Size", 8, 16, 12)}
                self.linewidths = st.slider("Cell Line Width", 0, 5, 1)
                self.linecolor = st.color_picker("Cell Line Color", "#FFFFFF")

                # Colorbar & Labels
                self.cbar = st.checkbox("Show Colorbar?", value=True)
                self.cbar_kws = {"shrink": st.slider("Colorbar Shrink Factor", 0.5, 1.5, 1.0)}
                self.xticklabels = st.selectbox("X-Axis Labels", ['auto', True, False])
                self.yticklabels = st.selectbox("Y-Axis Labels", ['auto', True, False])
                self.square = st.checkbox("Make Cells Square?", value=False)

            # Generate Plot Button
            if st.button("🚀 Generate Heatmap", use_container_width=True):
                self.generate_plot()

        # Saved Plots Section
        with self.tab2:
            st.header("📂 Saved Plots")
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])
                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No saved plots yet. Click 'Generate Heatmap' to create one.")

    def generate_plot(self):
        if not self.selected_columns:
            st.error("⚠️ Please select at least one numeric column for the heatmap.")
            return

        # Prepare Arguments for Heatmap
        plot_args = {
            'data': self.data[self.selected_columns],
            'vmin': self.vmin,
            'vmax': self.vmax,
            'center': self.center,
            'cmap': self.cmap,
            'robust': self.robust,
            'annot': self.annot,
            'fmt': self.fmt,
            'annot_kws': self.annot_kws,
            'linewidths': self.linewidths,
            'linecolor': self.linecolor,
            'cbar': self.cbar,
            'cbar_kws': self.cbar_kws if self.cbar else None,
            'square': self.square,
            'xticklabels': self.xticklabels,
            'yticklabels': self.yticklabels,
            'mask': None  # Default mask
        }

        # Apply mask for upper triangle (if selected)
        if self.mask:
            mask = np.triu(np.ones_like(self.data[self.selected_columns], dtype=bool))
            plot_args['mask'] = mask

        fig, ax = plt.subplots(figsize=(10, 8))

        try:
            sns.heatmap(**plot_args, ax=ax)

            # Display the figure in Streamlit
            st.pyplot(fig)

            # Save the figure and properly close it to avoid memory leaks
            self.saved_plots.append(fig)
        except Exception as e:
            st.error(f"⚠️ Error generating heatmap: {e}")
        finally:
            plt.close(fig)  # Always close the figure to avoid backend rendering issues
