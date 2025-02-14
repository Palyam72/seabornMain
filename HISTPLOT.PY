import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class HistPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("HistPlot Generator")
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

            with col2:
                # Hue Parameters
                st.subheader("Hue Parameters")
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
                self.stat = st.selectbox("Select the statistic", ["count", "frequency", "density", "probability", "percent"])
                self.bins = st.selectbox("Select the bin parameter", ["auto", "doane", "fd", "scott", "stone", "sturges"])
                self.binwidth = st.number_input("Bin Width", min_value=1, max_value=100, value=10)
                self.discrete = st.checkbox("Discrete")
                self.cumulative = st.checkbox("Cumulative")
                self.common_bins = st.checkbox("Common bins for all plots")
                self.common_norm = st.checkbox("Common normalization")
                self.kde = st.checkbox("Add KDE line")
                self.fill = st.checkbox("Fill under bars")
                self.shrink = st.number_input("Bar shrink factor", min_value=0.1, max_value=1.0, value=1.0)

            # Color and Scaling Parameters
            with col1:
                self.colors = [
                    'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink', 'brown', 'gray', 'black', 'white',
                    'cyan', 'magenta', 'lime', 'indigo', 'violet', 'teal', 'navy', 'maroon', 'olive', 'beige'
                ]
                self.color = st.selectbox("Single color specification", self.colors)
                self.height = st.number_input("Height", min_value=1, max_value=20, value=6)

            with col2:
                self.aspect = st.number_input("Aspect", min_value=0.1, max_value=3.0, value=1.0)

            # Log scale
            with col1:
                self.log_scale = st.checkbox("Log Scale")
                
            # Thresholds
            with col2:
                self.thresh = st.number_input("Threshold", min_value=0.0, max_value=1.0, value=0.0)
                self.pthresh = st.number_input("P-threshold", min_value=0.0, max_value=1.0, value=0.0)
                self.pmax = st.number_input("P-max", min_value=0.0, max_value=1.0, value=1.0)

            # Generate Plot
            if st.button("Generate Histogram Plot",use_container_width=True,type='primary'):
                try:
                    st.header("Current Plot")
                    plt.figure(figsize=(10, 6))
                    plt.title(f"{self.x} vs {self.y if self.is_bivariate else ''}")
                    plt.xlabel(self.x)
                    if self.is_bivariate:
                        plt.ylabel(self.y)

                    # Generate histogram plot using seaborn.histplot
                    if self.is_bivariate:
                        fig = sns.histplot(
                            data=self.data, x=self.x, y=self.y, hue=self.hue,
                            stat=self.stat, bins=self.bins, binwidth=self.binwidth,
                            discrete=self.discrete, cumulative=self.cumulative,
                            common_bins=self.common_bins, common_norm=self.common_norm,
                            multiple='layer', element='bars', fill=self.fill,
                            shrink=self.shrink, kde=self.kde,
                            color=self.color, palette=self.palette, log_scale=self.log_scale,
                            legend=True, hue_order=self.hue_order, thresh=self.thresh, pthresh=self.pthresh, pmax=self.pmax
                        )
                    else:
                        fig = sns.histplot(
                            data=self.data, x=self.x, hue=self.hue,
                            stat=self.stat, bins=self.bins, binwidth=self.binwidth,
                            discrete=self.discrete, cumulative=self.cumulative,
                            common_bins=self.common_bins, common_norm=self.common_norm,
                            multiple='layer', element='bars', fill=self.fill,
                            shrink=self.shrink, kde=self.kde,
                            color=self.color, palette=self.palette, log_scale=self.log_scale,
                            legend=True, hue_order=self.hue_order, thresh=self.thresh, pthresh=self.pthresh, pmax=self.pmax
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
