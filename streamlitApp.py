import chardet
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Importing all the entities from different python files
from ECDF import *
from HISTPLOT import *
from KDEPLOT import *
from RUGPLOT import *
from DISPLOT import *
from LINEPLOT import *
from RELPLOT import *
from SCATTERPLOT import *
from CATPLOT import *         
from STRIPPLOT import *       
from SWARMPLOT import *    
from BOXPLOT import *      
from VIOLINPLOT import *     
from BOXENPLOT import *      
from POINTPLOT import *       
from BARPLOT import *         
from COUNTPLOT import *      
from LMPLOT import *        
from REGPLOT import *         
from RESIDPLOT import *      
from HEATMAP import *         
from CLUSTERMAP import *      
from FACETGRID import *       
from PAIRPLOT import *        
from PAIRGRID import *        
from JOINTPLOT import *       
from JOINTGRID import *      
from fpdf import FPDF

def download_pdf(selected_graph_plots):
    if selected_graph_plots:
        # Create instance of FPDF class
        pdf = FPDF()

        # Loop through all images and add them to the PDF
        for img in selected_graph_plots:
            # Add a new page
            pdf.add_page()

            # Add image to the page, making it take the full page width (210mm)
            pdf.image(img, x=0, y=0, w=210)

        # Save the PDF to a file
        pdf_output = "plots_output.pdf"
        pdf.output(pdf_output)

        # Provide the PDF for download in Streamlit
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download PDF",
                data=file,
                file_name=pdf_output,
                mime="application/pdf"
            )
    else:
        st.error("No images to download.")

def readCSV(uploaded_file):
    raw_data = uploaded_file.getvalue()
    detected_encoding = chardet.detect(raw_data)
    encoding = detected_encoding['encoding']   
    try:
        df = pd.read_csv(uploaded_file, encoding=encoding)
        return df
    except UnicodeDecodeError:
        try:
            print(f"Encoding {encoding} failed. Trying with 'utf-8' encoding...")
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            return df
        except UnicodeDecodeError:
            try:
                print(f"Encoding 'utf-8' failed. Trying with 'ISO-8859-1' encoding...")
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')
                return df
            except Exception as e:
                print(f"Error reading the file: {e}")
                return "None"

# Listing all the lists available in session states
listVariables = ["rugplot","ecdf","kdeplot","histplot","displot","relplot","scatterplot","lineplot","catplot", "stripplot", "swarmplot",
                 "boxplot", "violinplot", "boxenplot", "pointplot", "barplot", "countplot",
                 "lmplot", "regplot", "residplot", "heatmap",
                 "clustermap", "FacetGrid", "pairplot", "PairGrid", "jointplot", "JointGrid"]

# Assigning session states
for i in listVariables:
    if i not in st.session_state:
        st.session_state[i] = []

# Assigning streamlit main components to streamlit's sidebar
file = st.sidebar.file_uploader("Upload the CSV file", type=["csv"])
st.sidebar.divider()
selectedPlot =st.sidebar.pills("Select the plot", listVariables)


if file is not None:
    df = readCSV(file)
    
    # Check if df is a DataFrame and not "None" string
    if isinstance(df, pd.DataFrame):
        # Main functionality
        if selectedPlot == "relplot":
            # Corrected variable name
            relplot = Distplot(df, st.session_state.get("relplot", []))  # Ensure session_state key exists
            relplot.display()
        elif selectedPlot == "scatterplot":
            scatterplot = ScatterPlot(df, st.session_state["scatterplot"])
            scatterplot.display()
        elif selectedPlot == "lineplot":
            lineplot = LinePlot(df, st.session_state["lineplot"])
            lineplot.display()
        elif selectedPlot == "displot":
            displot = DisPlot(df, st.session_state["displot"])
            displot.display()
        elif selectedPlot == "histplot":
            histplot = HistPlot(df, st.session_state["histplot"])
            histplot.display()
        elif selectedPlot == "kdeplot":
            kdeplot = KDEPlot(df, st.session_state["kdeplot"])
            kdeplot.display()
        elif selectedPlot == "ecdf":
            ecdf = ECDFPlot(df, st.session_state["ecdf"])
            ecdf.display()
        elif selectedPlot == "rugplot":
            rugplot = RugPlot(df, st.session_state["rugplot"])
            rugplot.display()
        elif selectedPlot == "catplot":
            catplot=Catplot(df,st.session_state["catplot"])
            catplot.display()
        elif selectedPlot == "stripplot":
            stripplot=Stripplot(df,st.session_state["stripplot"])
            stripplot.display()
        elif selectedPlot == "swarmplot":
            swarmplot=Swarmplot(df,st.session_state["swarmplot"])
            swarmplot.display()
        elif selectedPlot == "boxplot":
            boxplot=Boxplot(df,st.session_state["boxplot"])
            boxplot.display()
        elif selectedPlot == "violinplot":
            violinplot=ViolinPlotVisualizer(df,st.session_state["violinplot"])
            violinplot.display()
        elif selectedPlot == "boxenplot":
            boxenplot=BoxenplotVisualizer(df,st.session_state["boxenplot"])
            boxenplot.display()
        elif selectedPlot == "pointplot":
            pointplot=PointplotVisualizer(df,st.session_state["pointplot"])
            pointplot.display()
        elif selectedPlot == "barplot":
            barplot=BarplotVisualizer(df,st.session_state["barplot"])
            barplot.display()
        elif selectedPlot == "countplot":
            countplot=CountplotVisualizer(df,st.session_state["countplot"])
            countplot.display()
        elif selectedPlot == "lmplot":
            lmplot=LmplotVisualizer(df,st.session_state["lmplot"])
            lmplot.display()
        elif selectedPlot == "regplot":
            regplot=RegplotVisualizer(df,st.session_state["stripplot"])
            regplot.display()
        elif selectedPlot == "residplot":
            residplot=ResidplotVisualizer(df,st.session_state["stripplot"])
            residplot.display()
        elif selectedPlot == "heatmap":
            heatmap=HeatmapVisualizer(df,st.session_state["stripplot"])
            heatmap.display()
        elif selectedPlot == "clustermap":
            clustermap=ClustermapVisualizer(df,st.session_state["stripplot"])
            clustermap.display()
        elif selectedPlot == "FacetGrid":
            FacetGrid=FacetGridVisualizer(df,st.session_state["stripplot"])
            FacetGrid.display()
        elif selectedPlot == "pairplot":
            pairplot=PairPlotVisualizer(df,st.session_state["stripplot"])
            pairplot.display()
        elif selectedPlot == "PairGrid":
            PairGrid=PairGridVisualizer(df,st.session_state["stripplot"])
            PairGrid.display()
        elif selectedPlot == "jointplot":
            jointplot=JointPlotVisualizer(df,st.session_state["stripplot"])
            jointplot.display()
        elif selectedPlot == "JointGrid":
            JointGrid=JointGridVisualizer(df,st.session_state["stripplot"])
            JointGrid.display()
        else:
            st.error("Invalid plot selection.")
    else:
        st.error("Failed to load the CSV file. Please upload a valid file.")
