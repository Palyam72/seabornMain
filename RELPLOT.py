import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

class Distplot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2, tab3 = st.tabs(["Plotting", "Plotted Plots Section", "Document Section"])

        with tab1:
            st.header("Distplot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is inside"):
                st.dataframe(self.data)

            col1, col2 = st.columns(2)
            with col1:
                self.x = st.pills("Select the column for x-axis", [None] + self.columns, key="x_axis_distplot")
                self.y = st.pills("Select the column for y-axis", [None] + self.columns, key="y_axis_distplot")
                self.hue = st.pills("Select the column for hue", [None] + self.columns, key="hue_distplot")
                self.row = st.pills("Facet by rows", [None] + self.columns, key="row_distplot")
                self.col = st.pills("Facet by columns", [None] + self.columns, key="col_distplot")
                self.weights = st.pills("Select weights column (optional)", [None] + self.columns, key="weights_distplot")
                self.kind = st.pills("Select plot type", ["hist", "kde", "ecdf"], key="kind_distplot")
                self.rug = st.checkbox("Enable Rugplot", key="rug_distplot")
                self.legend = st.checkbox("Show Legend", key="legend_distplot")
                self.palette = st.pills("Select a color palette", ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"], key="palette_distplot")
                self.height = st.number_input("Set height of facets (in inches)", min_value=1, value=5, key="height_distplot")
                self.aspect = st.number_input("Set aspect ratio of facets", min_value=1, value=1, key="aspect_distplot")
                self.col_wrap = st.number_input("Wrap columns at specified width", min_value=1, max_value=5, value=3, key="col_wrap_distplot")

            with col2:
                self.hue_order = st.multiselect("Select the hue order", self.data[self.hue].unique().tolist(), key="hue_order_distplot") if self.hue else None
                self.hue_norm = None
                if self.hue:
                    if self.hue in self.numeric_columns:
                        hue_norm_input = st.text_input("Enter a range to normalize values (e.g., 1, 2)", key="hue_norm_distplot")
                        self.hue_norm = tuple(map(float, hue_norm_input.split(','))) if hue_norm_input else None

                self.row_order = self.data[self.row].unique().tolist() if self.row else None
                self.col_order = self.data[self.col].unique().tolist() if self.col else None

        with tab2:
            st.header("Plotted Plots Section")
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])
                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No plots saved yet.")

        with tab3:
            st.header("Document Section")
            st.code(__file__, language="python")

        # Plotting the graph based on user input
        if st.button("Generate Distplot", use_container_width=True, type='primary', key="plot_button_distplot"):
            try:
                fig = sns.displot(
                    data=self.data, x=self.x, y=self.y, hue=self.hue, weights=self.weights, kind=self.kind, 
                    rug=self.rug, log_scale=None, legend=self.legend, palette=self.palette, hue_order=self.hue_order,
                    hue_norm=self.hue_norm, col_wrap=self.col_wrap, row=self.row, col=self.col, 
                    row_order=self.row_order, col_order=self.col_order, height=self.height, 
                    aspect=self.aspect
                )
                st.pyplot(fig)
                self.saved_plots.append(fig)
            except Exception as e:
                st.error(f"Error generating plot: {e}")
