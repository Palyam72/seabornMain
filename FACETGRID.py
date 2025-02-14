import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class FacetGridVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("FacetGrid Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for the FacetGrid
            self.row = st.selectbox("Select Row Variable", self.columns)
            self.col = st.selectbox("Select Column Variable", self.columns)
            self.hue = st.selectbox("Select Hue Variable", [None] + self.columns)

            # FacetGrid Parameters
            self.col_wrap = st.number_input("Number of Columns to Wrap", min_value=1, value=3)
            self.sharex = st.radio("Share X-axis", ["True", "False", "col", "row"], index=1)
            self.sharey = st.radio("Share Y-axis", ["True", "False", "col", "row"], index=1)
            self.height = st.slider("Height of Each Facet", min_value=2, max_value=10, value=3)
            self.aspect = st.slider("Aspect Ratio", min_value=0.5, max_value=2.0, value=1.0)
            self.palette = st.text_input("Palette", "deep")
            self.row_order = st.text_input("Row Order", "None")
            self.col_order = st.text_input("Column Order", "None")
            self.hue_order = st.text_input("Hue Order", "None")
            self.hue_kws = st.text_input("Hue Keyword Arguments (JSON format)", "{}")
            self.dropna = st.checkbox("Drop Missing Values?", value=False)
            self.legend_out = st.checkbox("Place Legend Outside?", value=True)
            self.despine = st.checkbox("Remove Spines?", value=True)
            self.margin_titles = st.checkbox("Show Margin Titles?", value=False)
            self.xlim = st.text_input("X-axis Limits (e.g. (0, 10))", "None")
            self.ylim = st.text_input("Y-axis Limits (e.g. (0, 100))", "None")
            self.subplot_kws = st.text_input("Subplot Keyword Arguments (JSON format)", "{}")
            self.gridspec_kws = st.text_input("GridSpec Keyword Arguments (JSON format)", "{}")

            # Generate Plot Button
            if st.button("Generate FacetGrid"):
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
        # Prepare the arguments for FacetGrid
        plot_args = {
            'data': self.data,
            'row': self.row,
            'col': self.col,
            'hue': self.hue,
            'col_wrap': self.col_wrap,
            'sharex': self.sharex,
            'sharey': self.sharey,
            'height': self.height,
            'aspect': self.aspect,
            'palette': self.palette,
            'row_order': eval(self.row_order) if self.row_order != "None" else None,
            'col_order': eval(self.col_order) if self.col_order != "None" else None,
            'hue_order': eval(self.hue_order) if self.hue_order != "None" else None,
            'hue_kws': eval(self.hue_kws) if self.hue_kws else {},
            'dropna': self.dropna,
            'legend_out': self.legend_out,
            'despine': self.despine,
            'margin_titles': self.margin_titles,
            'xlim': eval(self.xlim) if self.xlim != "None" else None,
            'ylim': eval(self.ylim) if self.ylim != "None" else None,
            'subplot_kws': eval(self.subplot_kws) if self.subplot_kws else {},
            'gridspec_kws': eval(self.gridspec_kws) if self.gridspec_kws else {}
        }

        # Generate the FacetGrid plot
        g = sns.FacetGrid(**plot_args)
        g.map(sns.scatterplot, self.row, self.col)

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(g)
            self.saved_plots.append(g.fig)
