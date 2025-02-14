import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class BoxenplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        # Create tabs for Plotting and Documents sections
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        # Plotting section
        with tab1:
            st.header("Boxenplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create two columns for the plot settings
            col1, col2 = st.columns(2,border=True)

            with col1:
                # Select columns for x and y axes
                x_axis = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                y_axis = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

                # Hue Parameters (optional)
                hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
                hue_norm = None
                hue_order = None
                if hue:
                    if hue in self.data.select_dtypes(include=["int", "float"]).columns.tolist():
                        hue_norm = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                        hue_norm = eval(hue_norm) if hue_norm else None
                    else:
                        hue_order = st.multiselect("Select the hue order", self.data[hue].unique().tolist())

                # Color and Palette selection
                color = st.color_picker("Pick a single color for the plot", "#000000")
                palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )

                # Saturation and fill settings
                saturation = st.slider("Saturation", min_value=0.0, max_value=1.0, value=0.75, step=0.05)
                fill = st.checkbox("Fill plot area?", value=True)

            with col2:
                # Dodge and Width settings
                dodge = st.selectbox("Dodge", ["auto", True, False])
                width = st.slider("Width", min_value=0.0, max_value=2.0, value=0.8, step=0.05)
                gap = st.slider("Gap", min_value=0.0, max_value=2.0, value=0.0, step=0.05)

                # Line and Width settings
                linewidth = st.slider("Line Width", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
                linecolor = st.color_picker("Line Color", "#000000")

                # Boxenplot width method and k_depth
                width_method = st.selectbox("Boxenplot Width Method", ["exponential", "linear", "area"])
                k_depth = st.selectbox("Number of Tails", ["tukey", "proportion", "trustworthy", "full"])

                # Outlier Parameters
                outlier_prop = st.slider("Outlier Proportion", min_value=0.0, max_value=1.0, value=0.007, step=0.001)
                trust_alpha = st.slider("Trust Alpha", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
                showfliers = st.checkbox("Show Outliers?", value=True)

                # Log Scale and Formatter
                log_scale = st.checkbox("Apply Log Scale?", value=False)
                native_scale = st.checkbox("Use Native Scale?", value=False)
                formatter = st.text_input("Enter Formatter Function (Optional)")
                orient = st.selectbox("Choose Plot Orientation", ["v", "h"])

                # Legend settings
                legend = st.selectbox("Legend", ["auto", "brief", "full", False])

            # Plot generation button
            if st.button("Generate Plot",use_container_width=True,type='primary'):
                self.generate_plot(x_axis, y_axis, hue, hue_order, hue_norm, color, palette, saturation, fill, dodge,
                                   width, gap, linewidth, linecolor, width_method, k_depth, outlier_prop, trust_alpha,
                                   showfliers, log_scale, native_scale, formatter, orient, legend)

        # Documents section for saved plots
        with tab2:
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

    def generate_plot(self, x_axis, y_axis, hue, hue_order, hue_norm, color, palette, saturation, fill, dodge, width,
                      gap, linewidth, linecolor, width_method, k_depth, outlier_prop, trust_alpha, showfliers,
                      log_scale, native_scale, formatter, orient, legend):
        fig, ax = plt.subplots(figsize=(10, 6))

        try:
            sns.boxenplot(
                data=self.data,
                x=x_axis,
                y=y_axis,
                hue=hue,
                order=hue_order,
                hue_norm=hue_norm,
                color=color,
                palette=palette,
                saturation=saturation,
                fill=fill,
                dodge=dodge,
                width=width,
                gap=gap,
                linewidth=linewidth,
                linecolor=linecolor,
                width_method=width_method,
                k_depth=k_depth,
                outlier_prop=outlier_prop,
                trust_alpha=trust_alpha,
                showfliers=showfliers,
                log_scale=log_scale,
                formatter=formatter if formatter else None,  # Ensure it's handled properly
                orient=orient,
                native_scale=native_scale,
                legend=legend,
                ax=ax
            )

            # Show and save the plot
            st.pyplot(fig)

            # Save the plot if needed
            plot_name = f"boxenplot_{x_axis}_{y_axis}.png"
            self.saved_plots.append(fig)
            st.write(f"Plot saved as {plot_name}")

        except Exception as e:
            st.error(f"Error generating plot: {e}")
