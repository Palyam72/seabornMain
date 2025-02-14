import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from itertools import cycle

class RegplotVisualizer:
    def __init__(self, data, saved_plots):
        self.data = data
        self.saved_plots = saved_plots
        self.columns = self.data.columns.tolist()

    def display(self):
        self.tab1, self.tab2 = st.tabs(["Plots", "Saved Plots"])

        with self.tab1:
            st.header("📊 Regression Plot Generator")
            st.info("✅ Dataset Loaded. Select Parameters to Generate a Regression Plot.")

            st.dataframe(self.data)

            col1, col2 = st.columns(2)
            with col1:
                # X and Y Axes Selection
                self.x = st.selectbox("📌 Select X-Axis", [None] + self.columns, index=0)
                self.y = st.selectbox("📌 Select Y-Axis", [None] + self.columns, index=0)

                # Regression Options
                self.fit_reg = st.checkbox("Fit Regression Line?", value=True)
                self.ci = st.slider("Confidence Interval (%)", min_value=50, max_value=100, value=95)
                self.order = st.slider("Polynomial Regression Order", min_value=1, max_value=5, value=1)
                self.logx = st.checkbox("Use Log Scale for X-Axis?", value=False)

            with col2:
                self.robust = st.checkbox("Use Robust Regression?", value=False)
                self.lowess = st.checkbox("Use Lowess Regression?", value=False)
                self.truncate = st.checkbox("Truncate Regression Line to Data Range?", value=True)
                self.logistic = st.checkbox("Logistic Regression?", value=False)

                # Scatter Plot Styling
                self.scatter = st.checkbox("Show Scatter Plot?", value=True)
                self.marker = st.text_input("Scatter Marker (e.g., 'o', 'x')", "o")
                self.color = st.color_picker("Pick a Plot Color", "#000000")

            # Advanced Parameters
            with st.expander("⚙️ Advanced Settings"):
                self.x_bins = st.slider("X-Axis Bins", min_value=1, max_value=50, value=10)
                self.n_boot = st.slider("Bootstrap Resamples", min_value=100, max_value=5000, value=1000)
                self.dropna = st.checkbox("Drop Missing Data?", value=True)
                self.x_jitter = st.slider("X Jitter", min_value=0.0, max_value=1.0, value=0.0)
                self.y_jitter = st.slider("Y Jitter", min_value=0.0, max_value=1.0, value=0.0)
                self.x_ci = st.selectbox("X Confidence Interval", ["ci", "sd", None], index=0)
                self.x_estimator = st.selectbox("X Estimator", [None, "mean", "median", "sum"])
                self.units = st.selectbox("Units (Grouping Factor)", [None] + self.columns, index=0)
                self.seed = st.number_input("Random Seed", value=None, step=1, format="%d")

            # Customization
            with st.expander("🎨 Customize Plot Style"):
                self.scatter_kws = st.text_area("Scatter Plot Style (Dict Format)", "{}")
                self.line_kws = st.text_area("Line Style (Dict Format)", "{}")
                self.label = st.text_input("Legend Label", "")

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
        if not self.x or not self.y:
            st.error("⚠️ Please select valid columns for both X and Y axes.")
            return

        # Convert text inputs to dictionary format
        try:
            scatter_kws = eval(self.scatter_kws) if self.scatter_kws.strip() else {}
            line_kws = eval(self.line_kws) if self.line_kws.strip() else {}
        except Exception:
            st.error("⚠️ Invalid format in scatter_kws or line_kws. Use dictionary format (e.g., {'alpha': 0.5})")
            return

        # Prepare Arguments for regplot
        plot_args = {
            'data': self.data,
            'x': self.x,
            'y': self.y,
            'x_estimator': self.get_estimator(),
            'x_bins': self.x_bins,
            'x_ci': self.x_ci,
            'scatter': self.scatter,
            'fit_reg': self.fit_reg,
            'ci': self.ci,
            'n_boot': self.n_boot,
            'units': self.units if self.units != "None" else None,
            'seed': self.seed if self.seed else None,
            'order': self.order,
            'logistic': self.logistic,
            'lowess': self.lowess,
            'robust': self.robust,
            'logx': self.logx,
            'x_partial': None,
            'y_partial': None,
            'truncate': self.truncate,
            'dropna': self.dropna,
            'x_jitter': self.x_jitter,
            'y_jitter': self.y_jitter,
            'label': self.label if self.label.strip() else None,
            'color': self.color,
            'marker': self.marker,
            'scatter_kws': scatter_kws,
            'line_kws': line_kws
        }

        # Create the plot
        fig, ax = plt.subplots(figsize=(8, 6))
        try:
            sns.regplot(ax=ax, **plot_args)
            st.pyplot(fig)
            self.saved_plots.append(fig)  # Save the plot
        except Exception as e:
            st.error(f"⚠️ An error occurred while generating the plot: {e}")

    def get_estimator(self):
        """Helper function to return the appropriate x_estimator function"""
        estimator_map = {"mean": lambda x: x.mean(), "median": lambda x: x.median(), "sum": lambda x: x.sum()}
        return estimator_map.get(self.x_estimator, None)
