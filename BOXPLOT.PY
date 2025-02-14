import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class Boxplot:
    def __init__(self, data, saved_plots):
        # Initialize with data and a list of saved plots
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Boxplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create two columns for parameter layout
            col1, col2 = st.columns(2,border=True)

            # Column 1: Core Data, Axes Parameters, and Hue Parameters
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

            # Column 2: Boxplot Settings, Log scale and Native scale
            with col2:
                st.subheader("Boxplot Settings")
                # Boxplot Settings
                self.orient = st.selectbox("Orientation", ["v", "h"])
                self.width = st.number_input("Set width of box elements", min_value=0.1, max_value=1.0, value=0.8)
                self.saturation = st.slider("Saturation", min_value=0.0, max_value=1.0, value=0.75)
                self.fill = st.checkbox("Fill box", value=True)
                self.dodge = st.selectbox("Dodge hue levels", ["auto", True, False])
                self.whis = st.number_input("Whisker length", min_value=0.1, value=1.5)
                self.gap = st.number_input("Gap between elements", min_value=0.0, value=0.0)
                self.linecolor = st.color_picker("Line color", "#000000")
                self.linewidth = st.number_input("Line width", min_value=0.0, value=1.0)
                self.fliersize = st.number_input("Outlier marker size", min_value=0.0, value=5.0)

                # Log scale and native scale
                self.log_scale = st.checkbox("Use log scale", value=False)
                self.native_scale = st.checkbox("Use native scale", value=False)

                # Legend and other settings
                self.legend = st.selectbox("Select legend", ["auto", "brief", "full", False])

            # Button to generate the plot
            if st.button("Generate Plot",use_container_width=True,type='primary'):
                try:
                    # Create the plot using seaborn (sns.boxplot)
                    fig, ax = plt.subplots(figsize=(10, 6))  # Create a figure and axis

                    sns.boxplot(
                        data=self.data, x=self.x, y=self.y, hue=self.hue, hue_order=self.hue_order,
                        palette=self.palette, saturation=self.saturation, fill=self.fill,
                        dodge=self.dodge, width=self.width, gap=self.gap, whis=self.whis,
                        linecolor=self.linecolor, linewidth=self.linewidth, fliersize=self.fliersize,
                        hue_norm=self.hue_norm, native_scale=self.native_scale, log_scale=self.log_scale,
                        orient=self.orient, legend=self.legend, ax=ax
                    )

                    # Display the plot using Streamlit
                    st.pyplot(fig)

                    # Save the plot to the list of saved plots
                    self.saved_plots.append(fig)
                except Exception as e:
                    st.error(f"Error generating plot: {e}")

        with tab2:
            st.header("Documents Section")
            st.subheader("Saved Plots")

            # Display saved plots in a two-column layout
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])

                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No plots saved yet.")
