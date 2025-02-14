import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class PairGridVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("PairGrid Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Select columns for the PairGrid
            self.vars = st.multiselect("Select Variables for PairGrid", self.columns)
            self.hue = st.selectbox("Select Hue Variable", [None] + self.columns)
            self.hue_order = st.text_input("Hue Order", "None")
            self.palette = st.text_input("Palette", "deep")
            self.hue_kws = st.text_input("Hue Keyword Arguments (JSON format)", "{}")
            self.corner = st.checkbox("Corner Plot", value=False)
            self.diag_sharey = st.checkbox("Share Y-axis on Diagonal", value=True)
            self.height = st.slider("Height of Each Plot", min_value=2, max_value=10, value=3)
            self.aspect = st.slider("Aspect Ratio", min_value=0.5, max_value=2.0, value=1.0)
            self.layout_pad = st.slider("Layout Padding", min_value=0.1, max_value=1.0, value=0.5)
            self.despine = st.checkbox("Remove Top and Right Spines?", value=True)
            self.dropna = st.checkbox("Drop Missing Values?", value=False)

            # Generate Plot Button
            if st.button("Generate PairGrid"):
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
        # Prepare the arguments for PairGrid
        plot_args = {
            'data': self.data,
            'hue': self.hue,
            'vars': self.vars if self.vars else None,
            'hue_order': eval(self.hue_order) if self.hue_order != "None" else None,
            'palette': self.palette,
            'hue_kws': eval(self.hue_kws) if self.hue_kws else {},
            'corner': self.corner,
            'diag_sharey': self.diag_sharey,
            'height': self.height,
            'aspect': self.aspect,
            'layout_pad': self.layout_pad,
            'despine': self.despine,
            'dropna': self.dropna
        }

        # Generate the PairGrid plot
        g = sns.PairGrid(**plot_args)
        g.map_lower(sns.kdeplot)  # Default plot for lower triangle
        g.map_diag(sns.histplot)  # Default plot for diagonal

        # Display the plot
        st.pyplot(g.fig)

        # Save the plot to the list of saved plots
        self.saved_plots.append(g.fig)
