import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class ResidplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Saved Plots"])

        with self.tab1:
            st.header("📊 Residual Plot Generator")
            st.info("✅ Dataset Loaded. Select Parameters to Generate a Residual Plot.")
            st.dataframe(self.data)

            col1, col2 = st.columns(2)
            with col1:
                # Select X and Y Axes
                self.x = st.selectbox("📌 Select X-Axis", [None] + self.columns, index=0)
                self.y = st.selectbox("📌 Select Y-Axis", [None] + self.columns, index=0)

                # Regression Options
                self.lowess = st.checkbox("Fit Lowess Smoother?", value=False)
                self.order = st.slider("Polynomial Order", min_value=1, max_value=5, value=1)
                self.robust = st.checkbox("Use Robust Regression?", value=False)
                self.dropna = st.checkbox("Drop Missing Data?", value=True)

            with col2:
                # Partial Residuals
                self.x_partial = st.selectbox("📌 X Partial Residuals", [None] + self.columns, index=0)
                self.y_partial = st.selectbox("📌 Y Partial Residuals", [None] + self.columns, index=0)

                # Appearance Settings
                self.color = st.color_picker("Pick a Color for the Plot", "#000000")
                self.label = st.text_input("Legend Label", "")

            # Advanced Plot Styling
            with st.expander("⚙️ Advanced Plot Styling"):
                self.scatter_kws = st.text_area("Scatter Plot Styling (Dict Format)", "{}")
                self.line_kws = st.text_area("Line Style (Dict Format)", "{}")

            # Generate Plot Button
            if st.button("🚀 Generate Plot", use_container_width=True):
                self.generate_plot()

        # Saved Plots
        with self.tab2:
            st.header("📂 Saved Plots")
            if self.saved_plots:
                col1, col2 = st.columns(2)
                cols = cycle([col1, col2])
                for fig in self.saved_plots:
                    with next(cols):
                        st.pyplot(fig)
            else:
                st.info("No saved plots yet. Click 'Generate Plot' to create one.")

    def generate_plot(self):

        # Convert text inputs to dictionary format
        try:
            scatter_kws = eval(self.scatter_kws) if self.scatter_kws.strip() else {}
            line_kws = eval(self.line_kws) if self.line_kws.strip() else {}
        except Exception:
            st.error("⚠️ Invalid format in scatter_kws or line_kws. Use dictionary format (e.g., {'alpha': 0.5})")
            return

        # Prepare Arguments for residplot
        plot_args = {
            'data': self.data,
            'x': self.x,
            'y': self.y,
            'x_partial': self.x_partial if self.x_partial != "None" else None,
            'y_partial': self.y_partial if self.y_partial != "None" else None,
            'lowess': self.lowess,
            'order': self.order,
            'robust': self.robust,
            'dropna': self.dropna,
            'label': self.label if self.label.strip() else None,
            'color': self.color,
            'scatter_kws': scatter_kws,
            'line_kws': line_kws
        }

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))
        try:
            sns.residplot(ax=ax, **plot_args)
            st.pyplot(fig)
            self.saved_plots.append(fig)  # Save the plot
        except Exception as e:
            st.error(f"⚠️ An error occurred while generating the plot: {e}")
