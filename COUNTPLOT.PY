import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class CountplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("Countplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create columns for layout organization
            col1, col2 = st.columns(2,border=True)
            with col1:
                # Select columns for x and y axes
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0, key="x_column")
                self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0, key="y_column")

                # Hue Parameters
                self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0, key="hue_column")
                self.hue_order = None
                if self.hue:
                    self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist(), key="hue_order")

                # Statistic Type
                self.stat = st.selectbox("Statistic to compute", ['count', 'percent', 'proportion', 'probability'], key="stat_compute")

                # Color and Palette selection
                self.color = st.color_picker("Pick a single color for the plot", "#000000", key="color_picker")
                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"],
                    key="color_palette"
                )

                # Log Scale
                self.log_scale = st.checkbox("Apply Log Scale?", value=False, key="log_scale")

                # Width and Dodge Settings
                self.width = st.slider("Width of bars", min_value=0.1, max_value=2.0, value=0.8, step=0.1, key="bar_width")
                self.dodge = st.selectbox("Dodge", [True, False, "auto"], key="dodge_select")

            with col2:
                # Additional parameters for the plot
                self.saturation = st.slider("Saturation", 0.0, 1.0, 0.75, 0.05, key="saturation_slider")
                self.fill = st.checkbox("Fill Bars", value=True, key="fill_bars_checkbox")
                self.hue_norm = st.slider("Hue Normalization", 0.0, 1.0, 1.0, 0.05, key="hue_norm_slider")
                self.gap = st.slider("Gap between bars", 0.0, 1.0, 0.0, step=0.1, key="gap_slider")
                self.native_scale = st.checkbox("Native Scale?", value=False, key="native_scale_checkbox")
                self.formatter = st.text_input("Formatter", "", key="formatter_input")  # Keep empty if not using a custom formatter

                # Plot options
                self.orientation = st.selectbox("Choose Plot Orientation", ["v", "h"], key="orientation_select")
                self.legend = st.selectbox("Legend", ["auto", "brief", "full", False], key="legend_select")

            # Generate Plot Button
            if st.button("Generate Plot", key="generate_plot_button", use_container_width=True, type='primary'):
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
        fig, ax = plt.subplots(figsize=(10, 6))

        # Ensure 'stat' is a valid option in seaborn.countplot
        valid_stats = ['count', 'percent', 'proportion', 'probability']
        if self.stat not in valid_stats:
            st.error(f"Invalid stat option. Please choose one of: {', '.join(valid_stats)}")
            return

        # Check if the formatter is a valid callable
        formatter_function = None
        if self.formatter:  # If a formatter is entered, try to make it callable
            try:
                formatter_function = eval(self.formatter)  # This turns the string into a callable function
                if not callable(formatter_function):
                    raise ValueError("The provided formatter is not callable.")
            except Exception as e:
                st.error(f"Invalid formatter function: {e}")
                return

        sns.countplot(
            data=self.data,
            x=self.x,
            y=self.y,
            hue=self.hue,
            hue_order=self.hue_order,
            stat=self.stat,
            color=self.color,
            palette=self.palette,
            saturation=self.saturation,
            fill=self.fill,
            hue_norm=self.hue_norm,
            width=self.width,
            dodge=self.dodge,
            gap=self.gap,
            log_scale=self.log_scale,
            native_scale=self.native_scale,
            formatter=formatter_function,  # Use the callable formatter if it's valid
            orient=self.orientation,
            legend=self.legend,
            ax=ax
        )
        st.pyplot(fig)
        self.saved_plots.append(fig)
