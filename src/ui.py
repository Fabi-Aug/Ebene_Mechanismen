import os
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
tab = st.sidebar.radio("Select Section", ["Declaration", "Save", "Plot"])

if "points_data" not in st.session_state:
    st.session_state["points_data"] = []
if "connections_data" not in st.session_state:
    st.session_state["connections_data"] = []

if tab == "Declaration":
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
        
        if st.button("Temporarily Save"):
            Database.save_mechanism("temp_data.json")
        
    with prev:
        st.subheader("Preview")
        if st.button("Preview"):
            #clear_all_inst()                                       #load dunktioniert nicht ganz richtig      
            #Database.load_mechanism("test1.json")
            st.session_state["calc"] = Calculation()
            st.session_state["calc"].static_plot()
            st.image("src/StaticPlot.png", caption="Mechanism Preview", use_container_width=True)
            for point_id, point in st.session_state.points_objects.items():
                st.write(f"{point_id}: {point}")
            st.write("Connections:")
            for conn in connection_objects:
                st.write(conn)
            st.session_state["points_data"] = edited_df.to_dict(orient="records")       #test zeilen
            st.session_state["connections_data"] = connections
            
    
    st.divider()
    st.subheader("Degree of Freedom Analysis")
    if st.button("Check DOF"):
        #clear_all_inst()                           #load funktioniert nicht ganz richtig
        #Database.load_mechanism("test1.json")
        st.session_state["calc"] = Calculation()
        if st.session_state["calc"].check_dof() == 0:
            st.success("Kinematically Determined System")
        else:
            st.error("Kinematically Undetermined System")
            st.write(f"Degree of Freedom: {st.session_state['calc'].check_dof()}")

elif tab == "Save":
    st.subheader("Save Mechanism")
    file_name = st.text_input("Enter file name (without extension):")  
    if st.button("Save Mechanism"):
        Database.save_mechanism(f"{file_name}.json")
        st.success(f"Mechanism saved as {file_name}.json")

elif tab == "Plot":
    st.subheader("Mechanism Visualization")
    
    # Dropdown for selecting data source
    data_source_options =[f for f in os.listdir("src") if f.endswith(".json")]
    data_source = st.selectbox("Select data source:", data_source_options)

    json_file_path = f"{data_source}"
    clear_all_inst()
    Database.load_mechanism(json_file_path)
    st.success(f"Mechanism loaded from {json_file_path}")
    st.session_state["calc"] = Calculation()
    # Check if points are available
    # Check if points are available

    point_ids_list = st.session_state["calc"].get_dot_ids()  # IDs abrufen
    if point_ids_list:
        p_c = st.selectbox("Select a point for plotting", point_ids_list, key="plot_point")
    else:
        st.warning("No valid point IDs found in calculation data.")

    if "calculation" not in st.session_state:
        st.session_state["calculation"] = False 
    
    if st.session_state["calculation"] == False:                #preview funktioniert nicht ganz richtig!!!!!!!!!!
            st.session_state["calc"].static_plot()
            st.image("src/StaticPlot.png", caption="Mechanism Preview", use_container_width=True)

    if st.button("Calculate"):
            st.session_state["calc"] = Calculation()
            st.session_state["calc"].create_bom()
            st.session_state["calc"].generate_openscad()
            st.session_state["calc"].trajectory()
            st.session_state["calc"].animate_plot(p_c)
            st.session_state["calc"].save_csv("test.csv", p_c)
            st.image("src/Animation.gif", caption="Mechanism Animation", use_container_width=True)
            st.session_state["calculation"] = True

            #if st.session_state["points_data"]:
            #    st.session_state["calc"] = Calculation()
            #    st.session_state["calc"].trajectory()
            #    st.session_state["calc"].animate_plot(st.session_state.points_objects[st.session_state["point_ids"][2]])
            #    st.image("src/Animation.gif", caption="Mechanism Animation", use_container_width=True)
            #else:
            #      st.warning("No saved values found!")
    if st.session_state.get("calculation"):  # Ensure calculation exists
        st.subheader("Download all Data")

        zip_filename = "mechanism_data.zip"
        zip_path = os.path.join("src", zip_filename)  # Save in the same directory

        # Create a ZIP file with all required files
        with zipfile.ZipFile(zip_path, "w") as zipf:
            files_to_include = ["Animation.gif", "bom.pdf", "test.csv", "mechanism.scad"]
            
            for file in files_to_include:
                file_path = os.path.join("src", file)
                if os.path.exists(file_path):
                    zipf.write(file_path, arcname=file)  # Store without full path

        # Provide download button for the ZIP file
        with open(zip_path, "rb") as f:
            st.download_button(
                label="Download All Data",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )