import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Swarmplot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        # Create tabs for Plot generation and Document section
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Swarmplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create two columns for parameters layout
            col1, col2 = st.columns(2)

            # Column 1: Basic Plot Parameters
            with col1:
                # Select columns for x and y axes
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

                # Hue Parameters
                st.subheader("Hue Parameters")
                self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
                self.hue_norm = None
                self.hue_order = None
                if self.hue:
                    if self.hue in self.numeric_columns:
                        self.hue_norm = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                        self.hue_norm = eval(self.hue_norm) if self.hue_norm else None
                    else:
                        self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

                # Palette selection
                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )

                # Size and Edge Color for points
                self.size = st.slider("Select the size of points", min_value=1, max_value=10, value=5)
                self.edgecolor = st.selectbox("Select edge color", [None, "black", "white"])

            # Column 2: Additional Plot Parameters
            with col2:
                # Order of categories
                self.order = st.multiselect("Order of categories", self.data[self.x].unique().tolist()) if self.x else None

                # Additional Parameters
                st.subheader("Additional Parameters")
                self.dodge = st.checkbox("Dodge hue levels")
                self.warn_thresh = st.number_input("Warn Threshold", min_value=0.0, max_value=1.0, value=0.05)

                # Log Scale and Native Scale options
                self.log_scale = st.checkbox("Log scale")
                self.native_scale = st.checkbox("Native scale")
                self.legend = st.selectbox("Select legend", ["auto", "brief", "full", False])

                # Extra Parameters for Swarmplot
                self.color = st.selectbox("Color", [None] + self.columns, index=0)
                self.linewidth = st.slider("Linewidth of points", min_value=0, max_value=5, value=0)
                self.formatter = st.text_input("Formatter (optional, e.g., '%.2f')", "")
                self.orient = st.selectbox("Select orientation", [None, "v", "h"], index=0)
                self.ax = st.selectbox("Select axes (optional)", [None, "ax1", "ax2"], index=0)  # for later customization

            # Button to generate plot
            if st.button("Generate Plot"):
                try:
                    # Create a figure for the plot
                    fig, ax = plt.subplots()

                    # Ensure hue is a string if provided
                    if self.hue is None:
                        self.hue = ""
                    if self.color is None:
                        self.color = ""

                    # Generate the swarmplot
                    sns.swarmplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_order=self.hue_order,
                        palette=self.palette, dodge=self.dodge, order=self.order, hue_norm=self.hue_norm,
                        log_scale=self.log_scale, native_scale=self.native_scale, color=self.color,
                        size=self.size, edgecolor=self.edgecolor, linewidth=self.linewidth,
                        legend=self.legend, warn_thresh=self.warn_thresh, ax=ax, formatter=self.formatter,
                        orient=self.orient
                    )

                    # Display the plot
                    st.pyplot(fig)
                    self.saved_plots.append(fig)  # Save the plot for later reference

                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
            st.header("Documents Section")
            st.subheader("Saved Plots")

            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                # Display saved plots in a two-column layout
                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)  # Display saved figures
            else:
                st.info("No plots saved yet.")
