import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class LmplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Documents"])

        with self.tab1:
            st.header("LMPlot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            st.dataframe(self.data)

            # Create columns for better layout
            col1, col2 = st.columns(2)
            with col1:
                # Select columns for x and y axes
                self.x = st.selectbox("Select the column for x-axis", [None] + self.columns, index=0)
                self.y = st.selectbox("Select the column for y-axis", [None] + self.columns, index=0)

                # Hue Parameters
                self.hue = st.selectbox("Select the column for hue", [None] + self.columns, index=0)
                self.hue_order = None
                if self.hue:
                    self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist())

                # Facet Parameters
                self.col = st.selectbox("Select column facet", [None] + self.columns, index=0)
                self.row = st.selectbox("Select row facet", [None] + self.columns, index=0)

                # Plot Appearance
                self.palette = st.selectbox(
                    "Select a color palette",
                    ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"]
                )
                self.markers = st.text_input("Enter markers (e.g., 'o', 'x')", "o")

            with col2:
                # Plot Size
                self.height = st.slider("Height of each facet", min_value=3, max_value=10, value=5)
                self.aspect = st.slider("Aspect ratio of each facet", min_value=1.0, max_value=3.0, value=1.0)

                # Regression Options
                self.fit_reg = st.checkbox("Fit Regression Line?", value=True)
                self.ci = st.slider("Confidence Interval (%)", min_value=50, max_value=100, value=95)
                self.order = st.slider("Order of Polynomial Regression", min_value=1, max_value=5, value=1)
                self.logx = st.checkbox("Use Log Scale for X-Axis?", value=False)
                self.robust = st.checkbox("Use Robust Regression?", value=False)
                self.lowess = st.checkbox("Use Lowess Regression?", value=False)
                self.truncate = st.checkbox("Truncate Regression Line to Data Range?", value=True)

                # Additional Parameters
                self.col_wrap = st.slider("Column Wrap (None for no wrapping)", min_value=0, max_value=5, value=0)
                self.legend_out = st.checkbox("Place Legend Outside?", value=False)
                self.scatter = st.checkbox("Display Scatter Plot?", value=True)
                self.x_jitter = st.slider("Jitter for X-Axis", min_value=0.0, max_value=1.0, value=0.0)
                self.y_jitter = st.slider("Jitter for Y-Axis", min_value=0.0, max_value=1.0, value=0.0)

            # Generate Plot Button
            if st.button("Generate Plot"):
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
        # Ensure that col_wrap is not set to zero
        if self.col_wrap == 0:
            st.warning("Column Wrap must be greater than 0 to avoid errors.")
            return

        # Prepare the arguments for lmplot
        plot_args = {
            'data': self.data,
            'x': self.x,
            'y': self.y,
            'hue': self.hue,
            'hue_order': self.hue_order,
            'col': self.col,
            'row': self.row,
            'palette': self.palette,
            'markers': self.markers,
            'height': self.height,
            'aspect': self.aspect,
            'fit_reg': self.fit_reg,
            'ci': self.ci,
            'order': self.order,
            'logx': self.logx,
            'robust': self.robust,
            'lowess': self.lowess,
            'truncate': self.truncate,
            'col_wrap': self.col_wrap if self.col_wrap > 0 else None,  # Avoid 0 value here
            'legend_out': self.legend_out,
            'scatter': self.scatter,
            'x_jitter': self.x_jitter,
            'y_jitter': self.y_jitter
        }

        try:
            fig = sns.lmplot(**plot_args)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            return

        if st.button("Plot the graph", use_container_width=True):
            st.pyplot(fig)
            self.saved_plots.append(fig)
