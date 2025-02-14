import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import cycle

class ScatterPlot:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.numeric_columns = self.data.select_dtypes(include=["int", "float"]).columns.tolist()
        self.categorical_columns = self.data.select_dtypes(exclude=["int", "float"]).columns.tolist()
        self.columns = self.data.columns.tolist()

    def display(self):
        tab1, tab2, tab3 = st.tabs(["Plotting", "Plotted Plots Section", "Document Section"])

        with tab1:
            st.header("Scatter Plot Generator")
            st.subheader("Core Data and Axes Parameters")
            st.info("The data is already loaded.")
            with st.expander("Data Frame is inside"):
                st.dataframe(self.data)

            col1, col2 = st.columns(2,border=True)
            with col1:
                self.x = st.pills("Select data for x axis", [None] + self.columns, key='x_axis')
                self.y = st.pills("Select data for y axis", [None] + self.columns, key='y_axis')
                self.hue = st.pills("Select variable for color differentiation", [None] + self.columns, key='hue')
                self.size = st.pills("Select variable for size differentiation", [None] + self.columns, key='size')
                self.style = st.pills("Select variable for marker differentiation", [None] + self.columns, key='style',help='seaborn parameter : style')

            with col2:
                self.palette = st.pills("Select color palette", ["deep", "muted", "pastel", "dark", "colorblind", "viridis", "coolwarm"], key='palette')
                self.hue_order_list = [None] + (self.data[self.hue].unique().tolist() if self.hue and self.hue in self.data else [])
                self.hue_order = st.multiselect("Specify hue order", self.hue_order_list, key='hue_order')

                hue_norm_input = st.text_input("Normalization for Hue (e.g., '10,20')", key='hue_norm')
                self.hue_norm = tuple(map(float, hue_norm_input.split(','))) if hue_norm_input else None

                #self.sizes = st.text_input("Select variable for size", [None] + self.columns, key='sizes')

                size_norm_input = st.text_input("Normalization for Size (e.g., '10,20')", key='size_norm', value='10,20')
                self.size_norm = tuple(map(int, size_norm_input.split(','))) if size_norm_input else None

                self.size_order_list = [None] + (self.data[self.size].unique().tolist() if self.size and self.size in self.data else [])
                self.size_order = st.multiselect("Select size order", self.size_order_list, key='size_order')

                self.markers = st.checkbox("Enable markers", key='markers')

                self.style_order_list = [None] + (self.data[self.style].unique().tolist() if self.style and self.style in self.data else [])
                self.style_order = st.multiselect("Specify style order", self.style_order_list, key='style_order')

                self.legend = st.pills("Select legend type", ['auto', 'brief', 'full'], key='legend')
            
            if st.button("Plot the Plots", key='plot_button',use_container_width=True,type='primary'):
                if not self.x or not self.y:
                    st.error("Both X and Y axes must be selected!")
                else:
                    fig, ax = plt.subplots()
                    sns.scatterplot(
                        data=self.data,
                        x=self.x,
                        y=self.y, 
                        hue=self.hue if self.hue and self.hue in self.data else None, 
                        hue_order=self.hue_order if self.hue_order else None, 
                        hue_norm=self.hue_norm,
                        size=self.size if self.size and self.size in self.data else None, 
                        #sizes=self.sizes, 
                        size_order=self.size_order if self.size_order else None, 
                        size_norm=self.size_norm,
                        style=self.style if self.style and self.style in self.data else None, 
                        style_order=self.style_order if self.style_order else None, 
                        markers=self.markers, 
                        palette=self.palette if self.palette else None,
                        legend=self.legend, ax=ax
                    )
                    st.pyplot(fig)
                    self.saved_plots.append(fig)
                

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
