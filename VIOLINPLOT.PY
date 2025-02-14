import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import os

class ViolinPlotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        # Creating tabs for plots and documents sections
        tab1, tab2 = st.tabs(["Plots", "Documents"])

        with tab1:
            st.header("Violin Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create two columns for layout
            col1, col2 = st.columns(2,border=True)

            with col1:
                # Select columns for x and y axes
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

                # Hue Parameters
                self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
                self.hue_norm = None
                self.hue_order = None
                if self.hue:
                    if self.hue in self.data.select_dtypes(include=["int", "float"]).columns.tolist():
                        self.hue_norm = st.text_input("Enter a range to normalize values (e.g., (1, 2))")
                        self.hue_norm = eval(self.hue_norm) if self.hue_norm else None
                    else:
                        self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

                # Color and Palette selection
                self.color = st.color_picker("Pick a single color for the plot", "#000000")
                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )

            with col2:
                # Saturation and fill
                self.saturation = st.slider("Saturation", min_value=0.0, max_value=1.0, value=0.75, step=0.05)
                self.fill = st.checkbox("Fill plot area?", value=True)

                # Inner representation
                self.inner = st.selectbox("Select inner representation", ["box", "quart", "point", "stick", None])

                # Split parameter for hue
                self.split = st.checkbox("Split violins when hue is used?", value=False)

                # Violin plot width and dodge
                self.width = st.slider("Width", min_value=0.0, max_value=2.0, value=0.8, step=0.05)
                self.dodge = st.selectbox("Dodge", ["auto", True, False])

                # Gap, Line width, Line color
                self.gap = st.slider("Gap between violins", min_value=0.0, max_value=2.0, value=0.0, step=0.05)
                self.linewidth = st.slider("Line Width", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
                self.linecolor = st.color_picker("Line Color", "#000000")

                # KDE smoothing (Bandwidth)
                self.cut = st.slider("Bandwidth extension", min_value=0.0, max_value=5.0, value=2.0, step=0.1)
                self.gridsize = st.slider("Gridsize", min_value=10, max_value=200, value=100, step=10)
                self.bw_method = st.selectbox("Bandwidth method", ["scott", "silverman", "float"])
                self.bw_adjust = st.slider("Bandwidth adjust", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

                # Density normalization
                self.density_norm = st.selectbox("Density normalization", ["area", "count", "width"])
                self.common_norm = st.checkbox("Common normalization?", value=False)

                # Log scale
                self.log_scale = st.checkbox("Apply log scale?", value=False)

                # Plotting axis scaling options
                self.native_scale = st.checkbox("Use native scaling?", value=False)

                # Formatter for categorical data
                self.formatter = st.text_input("Enter formatter function (optional)")

                # Legend settings
                self.legend = st.selectbox("Legend", ["auto", "brief", "full", False])

                # Generate and plot button
            if st.button("Generate Plot",type='primary',use_container_width=True):
                self.generate_plot()

        with tab2:
            st.header("Documents Section")
            st.subheader("Saved Plots")

            if self.saved_plots:
                for plot in self.saved_plots:
                    st.pyplot(plot)
            else:
                st.info("No plots saved yet.")

    def generate_plot(self):



        fig, ax = plt.subplots(figsize=(10, 6))

        try:
            # Use sns.violinplot correctly
            sns.violinplot(
                data=self.data,
                x=self.x,
                y=self.y,
                hue=self.hue,
                order=self.hue_order,
                orient="v",  # Orientation can be controlled based on data type
                color=self.color,
                palette=self.palette,
                saturation=self.saturation,
                fill=self.fill,
                inner=self.inner,
                split=self.split,
                width=self.width,
                dodge=self.dodge,
                gap=self.gap,
                linewidth=self.linewidth,
                linecolor=self.linecolor,
                cut=self.cut,
                gridsize=self.gridsize,
                bw_method=self.bw_method,
                bw_adjust=self.bw_adjust,
                density_norm=self.density_norm,
                common_norm=self.common_norm,
                hue_norm=self.hue_norm,
                log_scale=self.log_scale,
                native_scale=self.native_scale,
                legend=self.legend,
                ax=ax
            )

            # Show the plot using Streamlit
            st.pyplot(fig)

            # Save the plot if needed
            plot_name = f"violin_plot_{self.x}_{self.y}.png"
            plot_path = os.path.join(".", plot_name)
            fig.savefig(plot_path)
            self.saved_plots.append(fig)
            st.write(f"Plot saved as {plot_name}")

        except Exception as e:
            st.error(f"Error generating plot: {e}")
