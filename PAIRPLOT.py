import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class PairPlotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("PairPlot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for the PairPlot
            self.vars = st.multiselect("Select Variables for PairPlot", self.columns)
            self.hue = st.selectbox("Select Hue Variable", [None] + self.columns)
            self.hue_order = st.text_input("Hue Order", "None")
            self.palette = st.text_input("Palette", "deep")
            self.kind = st.selectbox("Kind of Plot", ['scatter', 'kde', 'hist', 'reg'], index=0)
            self.diag_kind = st.selectbox("Kind of Diagonal Plot", ['auto', 'hist', 'kde', None], index=0)
            self.markers = st.text_input("Markers", "o")
            self.height = st.slider("Height of Each Plot", min_value=2, max_value=10, value=3)
            self.aspect = st.slider("Aspect Ratio", min_value=0.5, max_value=2.0, value=1.0)
            self.corner = st.checkbox("Corner Plot", value=False)
            self.dropna = st.checkbox("Drop Missing Values?", value=False)
            self.plot_kws = st.text_input("Plot Keyword Arguments (JSON format)", "{}")
            self.diag_kws = st.text_input("Diagonal Plot Keyword Arguments (JSON format)", "{}")
            self.grid_kws = st.text_input("Grid Keyword Arguments (JSON format)", "{}")

            # Generate Plot Button
            if st.button("Generate PairPlot"):
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
        # Prepare the arguments for PairPlot
        plot_args = {
            'data': self.data,
            'hue': self.hue,
            'hue_order': eval(self.hue_order) if self.hue_order != "None" else None,
            'palette': self.palette,
            'vars': self.vars if self.vars else None,
            'kind': self.kind,
            'diag_kind': self.diag_kind,
            'markers': self.markers,
            'height': self.height,
            'aspect': self.aspect,
            'corner': self.corner,
            'dropna': self.dropna,
            'plot_kws': eval(self.plot_kws) if self.plot_kws else {},
            'diag_kws': eval(self.diag_kws) if self.diag_kws else {},
            'grid_kws': eval(self.grid_kws) if self.grid_kws else {}
        }

        # Generate the PairPlot
        g = sns.pairplot(**plot_args)
        st.pyplot(g)
        self.saved_plots.append(g.fig)
