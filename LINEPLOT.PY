import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class LinePlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2, tab3 = st.tabs(["Plotting", "Plotted Plots Section", "Document Section"])

        with tab1:
            st.header("Line Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is inside"):
                st.dataframe(self.data)

            col1, col2 = st.columns(2)
            with col1:
                self.x = st.pills("Select data for x axis", [None] + self.columns, key='x_axis')
                self.y = st.pills("Select data for y axis", [None] + self.columns, key='y_axis')
                self.hue = st.pills("Select variable for color differentiation", [None] + self.columns, key='hue')
                self.size = st.pills("Select variable for size differentiation", [None] + self.columns, key='size')
                self.style = st.pills("Select variable for style differentiation", [None] + self.columns, key='style')
                self.units = st.pills("Select units", [None] + self.columns, key='units')
                self.weights = st.pills("Select weights", [None] + self.columns, key='weights')

            with col2:
                self.palette = st.pills("Select color palette", ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"], key='palette')
                self.hue_order_list = [None] + (self.data[self.hue].unique().tolist() if self.hue and self.hue in self.data else [])
                self.hue_order = st.multiselect("Specify hue order", self.hue_order_list, key='hue_order')

                hue_norm_input = st.text_input("Normalization for Hue (e.g., '10,20')", key='hue_norm')
                self.hue_norm = tuple(map(float, hue_norm_input.split(','))) if hue_norm_input else None

                #self.sizes = st.pills("Select variable for size", [None] + self.columns, key='sizes')
                size_norm_input = st.text_input("Normalization for Size (e.g., '10,20')", key='size_norm', value='10,20')
                self.size_norm = tuple(map(int, size_norm_input.split(','))) if size_norm_input else None

                self.size_order_list = [None] + (self.data[self.size].unique().tolist() if self.size and self.size in self.data else [])
                self.size_order = st.multiselect("Select size order", self.size_order_list, key='size_order')

                self.dashes = st.checkbox("Enable dashes", key='dashes')
                self.markers = st.checkbox("Enable markers", key='markers')

                self.style_order_list = [None] + (self.data[self.style].unique().tolist() if self.style and self.style in self.data else [])
                self.style_order = st.multiselect("Specify style order", self.style_order_list, key='style_order')

                self.estimator = st.pills("Select estimator", ['mean', 'sum', 'min', 'max', 'None'], key='estimator')
                self.errorbar = st.pills("Select error bar type", ['ci', 'pi', 'se', 'sd', 'None'], key='errorbar')
                self.n_boot = st.number_input("Number of bootstraps", min_value=100, max_value=5000, value=1000, key='n_boot')
                self.legend = st.pills("Select legend type", ['auto', 'brief', 'full'], key='legend')
                self.err_style = st.pills("Select error style", ['band', 'bars'], key='err_style')

            if st.button("Plot the Plots", key='plot_button'):
                if not self.x or not self.y:
                    st.error("Both X and Y axes must be selected!")
                else:
                    try:
                        fig, ax = plt.subplots()
                        sns.lineplot(
                            data=self.data, x=self.x, y=self.y, 
                            hue=self.hue if self.hue and self.hue in self.data else None, 
                            hue_order=self.hue_order if self.hue_order else None, 
                            hue_norm=self.hue_norm,
                            size=self.size if self.size and self.size in self.data else None, 
                            #sizes=self.sizes if self.sizes else None, 
                            size_order=self.size_order if self.size_order else None, 
                            size_norm=self.size_norm,
                            style=self.style if self.style and self.style in self.data else None, 
                            style_order=self.style_order if self.style_order else None, 
                            units=self.units if self.units and self.units in self.data else None,
                            weights=self.weights if self.weights and self.weights in self.data else None,
                            dashes=self.dashes,
                            markers=self.markers,
                            estimator=self.estimator if self.estimator != 'None' else None,
                            errorbar=self.errorbar if self.errorbar != 'None' else None,
                            n_boot=self.n_boot,
                            err_style=self.err_style,
                            palette=self.palette if self.palette else None,
                            legend=self.legend, ax=ax
                        )
                        st.pyplot(fig)
                        self.saved_plots.append(fig)
                    except Exception as e:
                        st.error(f"Error generating plot: {e}")

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
