import os,io, json
import zipfile
import streamlit as st
import pandas as pd
from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
from calculation_class import Calculation
from database_class import Database  # Import for load/save

def clear_all_inst():
    fixeddot.clear_instances()
    swivel.clear_instances()
    movabledot.clear_instances()
    connectionlinks.clear_instances()

st.title("Planar Mechanisms")

# Tabs for navigation
tab = st.sidebar.radio("Select Section", ["Build", "Plot"])

if "points_data" not in st.session_state:
    st.session_state["points_data"] = []
if "connections_data" not in st.session_state:
    st.session_state["connections_data"] = []

if tab == "Build":
    # 1) Clear all old instances:
    clear_all_inst()
    # 2) Read user input and create new points
    init, prev = st.columns(2)
    with init:
        st.subheader("Define Points")
        num_movable_points = st.number_input("Number of movable points", min_value=1, max_value=10, value=1)
        
        # Default data for fixed point, swivel point, and movable points
        points_data = [
            {"Point": "F", "X": 0.0, "Y": 0.0, "Type": "Fixed Point", "Radius": None},
            {"Point": "S", "X": -30.0, "Y": 0.0, "Type": "Swivel Point", "Radius": 11.0}
        ]
        for i in range(num_movable_points):
            points_data.append({"Point": f"P{i}", "X": 0.0, "Y": 0.0, "Type": "Movable Point", "Radius": None})

        # Create DataFrame
        df = pd.DataFrame(points_data)

        # Editable table
        edited_df = st.data_editor(
            df,
            column_config={
                "Type": st.column_config.SelectboxColumn(
                    "Point Type",
                    options=["Fixed Point", "Swivel Point", "Movable Point"],
                    disabled=[True, True] + [False] * num_movable_points
                ),
                "Radius": st.column_config.NumberColumn(
                    "Radius",
                    min_value=0.0,
                    format="%.2f"
                )
            },
            hide_index=True
        )

        # Create new point instances based on edited_df
        st.session_state.points_objects = {}
        for _, row in edited_df.iterrows():
            point_id = row["Point"]
            x, y, typ, radius = row["X"], row["Y"], row["Type"], row["Radius"]
            if typ == "Fixed Point":
                st.session_state.points_objects[point_id] = fixeddot(x, y, point_id)
            elif typ == "Swivel Point":
                st.session_state.points_objects[point_id] = swivel(x, y, radius, 0, point_id)
            elif typ == "Movable Point":
                st.session_state.points_objects[point_id] = movabledot(x, y, point_id)

        # 3) Create connections
        st.subheader("Define Connections")
        st.session_state["point_ids"] = [row["Point"] for _, row in edited_df.iterrows()]
        connections = []
        st.session_state["num_connections"] = st.number_input("Number of connections", min_value=1, max_value=20, value=2)
        for i in range(st.session_state["num_connections"]):
            col1, col2 = st.columns(2)
            with col1:
                p1 = st.selectbox(f"Connection {i+1} - Point 1", st.session_state["point_ids"], key=f"conn_{i}_p1")
            with col2:
                p2 = st.selectbox(f"Connection {i+1} - Point 2", st.session_state["point_ids"], key=f"conn_{i}_p2")
            connections.append((p1, p2))
        
        # Create connectionlinks instances
        connection_objects = [
            connectionlinks(st.session_state.points_objects[p1], st.session_state.points_objects[p2])
            for p1, p2 in connections
        ]
        st.session_state["calc"] = Calculation()
        
    with prev:
        st.subheader("Preview")
        
        st.session_state["calc"] = Calculation()
        st.session_state["calc"].static_plot()
        st.image("src/StaticPlot.png", caption="Mechanism Preview", use_container_width=True)
        #for point_id, point in st.session_state.points_objects.items():
        #    st.write(f"{point_id}: {point}")
        #st.write("Connections:")
        #for conn in connection_objects:
        #    st.write(conn)
        #st.session_state["points_data"] = edited_df.to_dict(orient="records")       #test zeilen
        #st.session_state["connections_data"] = connections
        if st.button("Check DOF"):
            st.session_state["calc"] = Calculation()
            if st.session_state["calc"].check_dof() == 0:
                st.success("Kinematically Determined System")
            else:
                st.error("Kinematically Undetermined System")
                st.write(f"Degree of Freedom: {st.session_state['calc'].check_dof()}")

        if st.button("Temporarily Save"):
            if st.session_state["calc"].check_dof() == 0:
                Database.save_mechanism("builded_mechanism.json")
                st.success("Saved under builded_mechanism.json")
            else:
                st.error("Cannot save, mechanism is kinematically undetermined")
    
    st.divider()
    st.subheader("Save Mechanism")
    file_name = st.text_input("Enter file name (without extension):")  
    if st.button("Save Mechanism"):
        if st.session_state["calc"].check_dof() == 0:
            if not file_name:
                st.error("Please enter a valid file name")
            else:
                Database.save_mechanism(f"{file_name}.json")    
                st.success(f"Mechanism saved as {file_name}.json")
        else:
            st.error("Cannot save, mechanism is kinematically undetermined")
    
elif tab == "Plot":
    st.subheader("Mechanism Visualization")
    load, prev = st.columns(2)    
    with load:
        if "delete_file" not in st.session_state:
            st.session_state["delete_file"] = "None"
        data_source_options = [f for f in os.listdir("src") if f.endswith(".json") and not f == st.session_state["delete_file"]]
        data_source = st.selectbox("Select data source:", data_source_options)
        
        # Reset calculation flags only if a new file is selected
        if "current_file" not in st.session_state or st.session_state["current_file"] != data_source:
            st.session_state["current_file"] = data_source
            st.session_state["calculation"] = False
            st.session_state["calc_done"] = False
        
        json_file_path = f"{data_source}"
        clear_all_inst()
        Database.load_mechanism(json_file_path)
        st.success(f"Mechanism loaded from {json_file_path}")
        st.session_state["calc"] = Calculation()
        
        point_ids_list = st.session_state["calc"].get_dot_ids()  # IDs abrufen
        if point_ids_list:
            p_c = st.selectbox("Select a point for plotting", point_ids_list, key="plot_point")
        else:
            st.warning("No valid point IDs found in calculation data.")
        
        if "calculation" not in st.session_state:
            st.session_state["calculation"] = False
        
        calculate, delete = st.columns(2)
        with calculate:
            if st.button("Calculate"):
                st.session_state["calculation"] = True
        #with delete:
        #    if data_source not in ["strandbeest.json", "builded_mechanism.json"]:
        #        delete_button = st.button("Delete")
        #       
        #        if delete_button:
        #            file_path = os.path.join("src", data_source)
        #
        #            try:
        #                # Unload any loaded mechanism to prevent file locks
        #                clear_all_inst()
        #
        #                # Store the file path in session state before deletion
        #                st.session_state["delete_file"] = file_path
        #
        #                # Ensure the file exists before deleting
        #                if os.path.exists(st.session_state["delete_file"]):
        #                    os.remove(st.session_state["delete_file"])
        #                    st.success(f"Deleted {os.path.basename(st.session_state['delete_file'])}")
#
        #                    # Reset state and refresh UI
        #                    st.session_state["delete_file"] = None
        #                    st.rerun()
        #                else:
        #                    st.error("File not found. It might have been deleted already.")
#
        #            except PermissionError:
        #                st.error(f"File '{os.path.basename(st.session_state['delete_file'])}' is currently in use. Close any applications using it and try again.")
        #            except FileNotFoundError:
        #                st.error("File not found. It might have been deleted already.")

    with prev:
        st.session_state["calc"].static_plot()
        st.image("src/StaticPlot.png", caption="Mechanism Preview", use_container_width=True)
        
    if st.session_state["calculation"]:
        file_name = os.path.splitext(data_source)[0]
        st.subheader(file_name)
        
        # Only perform expensive calculations if they haven't been done already.
        if not st.session_state.get("calc_done", False):
            st.session_state["calc"] = Calculation()
            st.session_state["calc"].create_bom()
            st.session_state["calc"].generate_openscad()
            st.session_state["calc"].trajectory()
            st.session_state["calc"].animate_plot(p_c)
            st.session_state["calc"].save_csv("mechanism.csv", p_c)
            st.session_state["calc_done"] = True
        
        st.image("src/Animation.gif", caption="Mechanism Animation", use_container_width=True)
       
        st.subheader("Download from Mechanism " + file_name)
        options = ["Select file to download", ["Bill of Materials", "CSV", "CAD Modell", "Animation", f"{file_name} Database", "All Data as Zip"]]
        selected_option = st.selectbox("Select file to download", options[1])
        if selected_option == "Bill of Materials":
            with open("src/bom.pdf", "rb") as pdf_file:
                st.download_button(
                    label="Download",
                    data=pdf_file,
                    file_name=f"{file_name}_bom.pdf", 
                    mime="application/pdf"
                )
        elif selected_option == "CSV":
            with open(f"src/mechanism.csv", "rb") as csv_file:
                st.download_button(
                    label="Download",
                    data=csv_file,
                    file_name=f"{file_name}.csv",
                    mime="text/csv"
                )
        elif selected_option == "CAD Modell":
            with open("src/mechanism.scad", "rb") as scad_file:
                st.download_button(
                    label="Download",
                    data=scad_file,
                    file_name=f"{file_name}.scad",
                    mime="text/plain"
                )
        elif selected_option == "Animation":
            with open("src/Animation.gif", "rb") as gif_file:
                st.download_button(
                    label="Download",
                    data=gif_file,
                    file_name=f"{file_name}_animation.gif",
                    mime="image/gif"
                )
        elif selected_option == f"{file_name} Database":
            with open(f"src/{file_name}.json", "rb") as json_file:
                st.download_button(
                    label=f"Download",
                    data=json_file,
                    file_name=f"{file_name}.json",
                    mime="application/json"
                )
        elif selected_option == "All Data as Zip":
            zip_filename = f"{file_name}_data.zip"
            # Create an in-memory ZIP file
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                # Mapping: disk file → downloaded (connected) file name
                files_mapping = {
                    "Animation": ("Animation.gif", f"{file_name}_animation.gif"),
                    "BOM": ("bom.pdf", f"{file_name}_bom.pdf"),
                    "CSV": (f"mechanism.csv", f"{file_name}.csv"),
                    "Database": (f"{file_name}.json", f"{file_name}.json"),
                    "CAD": ("mechanism.scad", f"{file_name}.scad")
                }
                for key, (src_filename, new_filename) in files_mapping.items():
                    file_path = os.path.join("src", src_filename)
                    if os.path.exists(file_path):
                        zipf.write(file_path, arcname=new_filename)
            zip_buffer.seek(0)
            st.download_button(
                label="Download",
                data=zip_buffer,
                file_name=zip_filename,
                mime="application/zip"
            )
                        