import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from itertools import cycle

class ECDFPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("ECDF Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is here"):
                st.dataframe(self.data)

            # Create two columns for parameters
            col1, col2 = st.columns(2,border=True)

            # Column 1: x, y, hue, palette, weights
            with col1:
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                self.y = st.selectbox("Select the column for y-axis (optional)", [None] + self.columns, index=0)

                self.hue = st.selectbox("Select the column for hue (optional)", [None] + self.columns, index=0)
                self.weights = st.selectbox("Select the column for weights (optional)", [None] + self.columns, index=0)

                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )

            # Column 2: stat, complementary, log_scale, hue_order, hue_norm, legend
            with col2:
                self.stat = st.selectbox("Select the statistic", ["proportion", "percent", "count"])
                self.complementary = st.checkbox("Complementary ECDF")
                self.log_scale = st.checkbox("Log Scale")
                self.hue_order = st.multiselect("Select the hue order (if applicable)", self.data[self.hue].unique().tolist()) if self.hue else None
                self.hue_norm = st.text_input("Enter hue normalization range (e.g., (1, 2))")
                self.legend = st.checkbox("Show legend", value=True)

            # Generate Plot Button
            if st.button("Generate ECDF Plot",use_container_width=True,type='primary'):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"ECDF of {self.x} vs {self.y if self.y else ''}")
                    plt.xlabel(self.x)
                    if self.y:
                        plt.ylabel(self.y)

                    # Normalize hue if necessary
                    if self.hue_norm:
                        try:
                            self.hue_norm = eval(self.hue_norm)
                        except:
                            st.error("Invalid range format for hue normalization. Please enter a tuple like (1, 2).")
                            return

                    # Generate ECDF plot using seaborn.ecdfplot
                    fig = sns.ecdfplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, weights=self.weights,
                        stat=self.stat, complementary=self.complementary, palette=self.palette,
                        hue_order=self.hue_order, hue_norm=self.hue_norm, log_scale=self.log_scale,
                        legend=self.legend
                    )

                    # Display the plot
                    st.pyplot(plt.gcf())

                    # Save the figure (save the actual matplotlib figure)
                    self.saved_plots.append(plt.gcf())

                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
            st.header("Saved Plots")
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for saved_plot in self.saved_plots:
                    with next(cols):
                        st.pyplot(saved_plot)
            else:
                st.info("No plots saved yet.")
