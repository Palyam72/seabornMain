import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class KDEPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("KDE Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is here"):
                st.dataframe(self.data)

            # Select columns for x and y axes
            col1, col2 = st.columns(2,border=True)
            with col1:
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                self.y = st.selectbox("Select the column for y-axis (optional)", [None] + self.columns, index=0)

                if not self.x:
                    st.warning("Please select an x-axis for the plot.")
                    return

                # If both x and y are selected, it will be bivariate
                self.is_bivariate = bool(self.y)

            with col1:
                self.hue = st.selectbox("Select the column for hue (optional)", [None] + self.columns, index=0)
                self.hue_norm = None
                self.hue_order = None
                if self.hue:
                    if self.hue in self.numeric_columns:
                        hue_norm_input = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                        try:
                            self.hue_norm = eval(hue_norm_input) if hue_norm_input else None
                        except:
                            st.error("Invalid range format. Please enter a tuple like (1, 2).")
                    else:
                        self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

            # Palette selection
            with col1:
                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )

            # Additional Parameters
            with col2:
                self.bw_method = st.selectbox("Select the bandwidth method", ["scott", "silverman"])
                self.bw_adjust = st.number_input("Bandwidth Adjustment", min_value=0.1, max_value=10.0, value=1.0)
                self.fill = st.checkbox("Fill under the curve")
                self.common_norm = st.checkbox("Common Normalization")
                self.cumulative = st.checkbox("Cumulative")
                self.log_scale = st.checkbox("Log Scale")
                self.gridsize = st.number_input("Grid Size", min_value=10, max_value=500, value=200)
                self.cut = st.number_input("Cut", min_value=0, max_value=10, value=3)
                self.levels = st.selectbox("Contour Levels", ["10", "20", "50", "100"])

            # Generate Plot
            if st.button("Generate KDE Plot",use_container_width=True,type='primary'):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"{self.x} vs {self.y if self.is_bivariate else ''}")
                    plt.xlabel(self.x)
                    if self.is_bivariate:
                        plt.ylabel(self.y)

                    # Generate KDE plot using seaborn.kdeplot
                    if self.is_bivariate:
                        fig = sns.kdeplot(
                            data=self.data, x=self.x, y=self.y, hue=self.hue,
                            bw_method=self.bw_method, bw_adjust=self.bw_adjust,
                            fill=self.fill, common_norm=self.common_norm,
                            cumulative=self.cumulative, log_scale=self.log_scale,
                            gridsize=self.gridsize, cut=self.cut, levels=int(self.levels),
                            palette=self.palette, hue_order=self.hue_order, hue_norm=self.hue_norm
                        )
                    else:
                        fig = sns.kdeplot(
                            data=self.data, x=self.x, hue=self.hue,
                            bw_method=self.bw_method, bw_adjust=self.bw_adjust,
                            fill=self.fill, common_norm=self.common_norm,
                            cumulative=self.cumulative, log_scale=self.log_scale,
                            gridsize=self.gridsize, cut=self.cut, levels=int(self.levels),
                            palette=self.palette, hue_order=self.hue_order, hue_norm=self.hue_norm
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
