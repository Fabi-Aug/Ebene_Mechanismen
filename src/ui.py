import os, io, json
import zipfile
import streamlit as st
import pandas as pd
from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
from calculation_class import Calculation
from database_class import Database


# Clear all instances of the classes
def clear_all_inst():
    fixeddot.clear_instances()
    swivel.clear_instances()
    movabledot.clear_instances()
    connectionlinks.clear_instances()


st.title("Planar Mechanisms")

# Sidebar
st.sidebar.subheader("Navigation")
tab = st.sidebar.radio("", ["Build", "Plot", "Report"])

if "points_data" not in st.session_state:
    st.session_state["points_data"] = []
if "connections_data" not in st.session_state:
    st.session_state["connections_data"] = []

# Build tab to create a mechanism
if tab == "Build":
    clear_all_inst()
    init, prev = st.columns(2)
    with init:
        st.subheader("Define Points")
        num_fixed_points = st.number_input(
            "Number of fixed points",
            min_value=1,
            max_value=10,
            value=1,
            key="num_fixed",
        )
        num_movable_points = st.number_input(
            "Number of movable points",
            min_value=1,
            max_value=10,
            value=1,
            key="num_movable",
        )

        points_data = []
        # Create fixed points
        for i in range(num_fixed_points):
            points_data.append(
                {
                    "Point": f"F{i}",
                    "X": 0.0,
                    "Y": 0.0,
                    "Type": "Fixed Point",
                    "Radius": None,
                }
            )
        # Create a swivel point
        points_data.append(
            {"Point": "S", "X": 0.0, "Y": 0.0, "Type": "Swivel Point", "Radius": 0.0}
        )
        # Create movable points
        for i in range(num_movable_points):
            points_data.append(
                {
                    "Point": f"P{i}",
                    "X": 0.0,
                    "Y": 0.0,
                    "Type": "Movable Point",
                    "Radius": None,
                }
            )

        df = pd.DataFrame(points_data)

        # Edit the data in the data editor
        disabled_list = (
            [True] * num_fixed_points + [True] + [False] * num_movable_points
        )
        edited_df = st.data_editor(
            df,
            column_config={
                "Type": st.column_config.SelectboxColumn(
                    "Point Type",
                    options=["Fixed Point", "Swivel Point", "Movable Point"],
                    disabled=disabled_list,
                ),
                "Radius": st.column_config.NumberColumn(
                    "Radius", min_value=0.0, format="%.2f"
                ),
            },
            hide_index=True,
        )

        # Create new point instances based on the edited data:
        st.session_state.points_objects = {}
        for _, row in edited_df.iterrows():
            point_id = row["Point"]
            x, y, typ, radius = row["X"], row["Y"], row["Type"], row["Radius"]
            if typ == "Fixed Point":
                st.session_state.points_objects[point_id] = fixeddot(x, y, point_id)
            elif typ == "Swivel Point":
                st.session_state.points_objects[point_id] = swivel(
                    x, y, radius, 0, point_id
                )
            elif typ == "Movable Point":
                st.session_state.points_objects[point_id] = movabledot(x, y, point_id)

        # Define connections:
        st.subheader("Define Connections")
        st.session_state["point_ids"] = [
            row["Point"] for _, row in edited_df.iterrows()
        ]
        connections = []
        st.session_state["num_connections"] = st.number_input(
            "Number of connections", min_value=1, max_value=20, value=2
        )
        for i in range(st.session_state["num_connections"]):
            col1, col2 = st.columns(2)
            with col1:
                p1 = st.selectbox(
                    f"Connection {i+1} - Point 1",
                    st.session_state["point_ids"],
                    key=f"conn_{i}_p1",
                )
            with col2:
                p2 = st.selectbox(
                    f"Connection {i+1} - Point 2",
                    st.session_state["point_ids"],
                    key=f"conn_{i}_p2",
                )
            connections.append((p1, p2))

        # Create connection links
        connection_objects = [
            connectionlinks(
                st.session_state.points_objects[p1], st.session_state.points_objects[p2]
            )
            for p1, p2 in connections
        ]
        st.session_state["calc"] = Calculation()

    # Preview the mechanism
    with prev:
        st.subheader("Preview")
        st.session_state["calc"] = Calculation()
        st.session_state["calc"].static_plot()
        st.image(
            "src/StaticPlot.png", caption="Mechanism Preview", use_container_width=True
        )

        # Check DOF
        if st.button("Check DOF"):
            st.session_state["calc"] = Calculation()
            dof = st.session_state["calc"].check_dof()
            if dof == 0:
                st.success("Kinematically Determined System")
            else:
                st.error("Kinematically Undetermined System")
                st.write(f"Degree of Freedom: {dof}")

        # Save mechanism in built_mechanism.json file
        if st.button("Temporarily Save"):
            if st.session_state["calc"].check_dof() == 0:
                Database.save_mechanism("built_mechanism.json")
                st.success("Saved under built_mechanism.json")
            else:
                st.error("Cannot save, mechanism is kinematically undetermined")

    st.divider()
    st.subheader("Save Mechanism")
    # Save mechanism in a custom named file
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

# Plot tab to calculate and visualize the Trajectory
elif tab == "Plot":
    st.subheader("Mechanism Visualization")
    load, prev = st.columns(2)
    # Load mechanism from a JSON file
    with load:
        data_source_options = (
            ["Choose Mechanism"]
            + [f for f in os.listdir("src") if f.endswith(".json")]
            + ["Upload file"]
        )
        data_source = st.selectbox("Select data source:", data_source_options)
        if data_source == "Upload file":
            uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
            if uploaded_file is not None:
                file_path = os.path.join("src", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"Uploaded file saved as {uploaded_file.name}")
                data_source = uploaded_file.name
            else:
                st.info("Awaiting file upload.")
                st.stop()
        if data_source == "Choose Mechanism":
            st.info("Please select a mechanism to visualize.")
            st.stop()

        if (
            "current_file" not in st.session_state
            or st.session_state["current_file"] != data_source
        ):
            st.session_state["current_file"] = data_source
            st.session_state["calculation"] = False
            st.session_state["calc_done"] = False

        json_file_path = data_source
        clear_all_inst()
        Database.load_mechanism(json_file_path)
        st.success(f"Mechanism loaded from {json_file_path}")
        st.session_state["calc"] = Calculation()

        point_ids_list = st.session_state["calc"].get_dot_ids()
        if point_ids_list:
            st.session_state["p_c"] = st.selectbox(
                "Select a point for trajectory", point_ids_list, key="plot_point"
            )
        else:
            st.warning("No valid point IDs found in calculation data.")

        if "calculation" not in st.session_state:
            st.session_state["calculation"] = False

        if st.button("Calculate"):
            st.session_state["calculation"] = True

    # Show preview of the Loaded mechanism
    with prev:
        st.session_state["calc"].static_plot()
        st.image(
            "src/StaticPlot.png",
            caption=f"{data_source} Preview",
            use_container_width=True,
        )

    if "file_name" not in st.session_state:
        st.session_state["file_name"] = None

    if st.session_state["calculation"]:
        file_name = os.path.splitext(data_source)[0]
        st.session_state["file_name"] = file_name
        st.subheader(file_name)

        if not st.session_state.get("calc_done", False):
            st.session_state["calc"] = Calculation()
            st.session_state["calc"].create_bom()
            st.session_state["calc"].generate_openscad()
            st.session_state["calc"].trajectory()
            st.session_state["calc"].animate_plot(st.session_state["p_c"])
            st.session_state["calc"].save_csv("mechanism.csv", st.session_state["p_c"])
            st.session_state["calc_done"] = True

        st.image(
            "src/Animation.gif", caption="Mechanism Animation", use_container_width=True
        )

        # Download of Bill of Materials, Trajectory CSV, CAD Model, Animation, Trajectory Plot, Database and a Zip of all files
        st.subheader("Download from Mechanism " + file_name)
        options = [
            "Select file to download",
            [
                "Bill of Materials",
                "Trajectory CSV",
                "CAD Modell",
                "Animation",
                "Trajectory Plot",
                f"{file_name} Database",
                "All Data as Zip",
            ],
        ]
        selected_option = st.selectbox("Select file to download", options[1])
        if selected_option == "Bill of Materials":
            with open("src/bom.pdf", "rb") as pdf_file:
                st.download_button(
                    label="Download",
                    data=pdf_file,
                    file_name=f"{file_name}_bom.pdf",
                    mime="application/pdf",
                )
        elif selected_option == "Trajectory CSV":
            with open(f"src/mechanism.csv", "rb") as csv_file:
                st.download_button(
                    label="Download",
                    data=csv_file,
                    file_name=f"{file_name}.csv",
                    mime="text/csv",
                )
        elif selected_option == "CAD Modell":
            with open("src/mechanism.scad", "rb") as scad_file:
                st.download_button(
                    label="Download",
                    data=scad_file,
                    file_name=f"{file_name}.scad",
                    mime="text/plain",
                )
        elif selected_option == "Animation":
            with open("src/Animation.gif", "rb") as gif_file:
                st.download_button(
                    label="Download",
                    data=gif_file,
                    file_name=f"{file_name}_animation.gif",
                    mime="image/gif",
                )
        elif selected_option == "Trajectory Plot":
            with open("src/Animation_last_frame.png", "rb") as plot_file:
                st.download_button(
                    label="Download",
                    data=plot_file,
                    file_name=f"{file_name}_trajectory_plot.png",
                    mime="image/png",
                )
        elif selected_option == f"{file_name} Database":
            with open(f"src/{file_name}.json", "rb") as json_file:
                st.download_button(
                    label=f"Download",
                    data=json_file,
                    file_name=f"{file_name}.json",
                    mime="application/json",
                )
        elif selected_option == "All Data as Zip":
            zip_filename = f"{file_name}_data.zip"
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zipf:
                files_mapping = {
                    "Animation": ("Animation.gif", f"{file_name}_animation.gif"),
                    "Trajectory Plot": (
                        "Animation_last_frame.png",
                        f"{file_name}_trajectory_plot.png",
                    ),
                    "BOM": ("bom.pdf", f"{file_name}_bom.pdf"),
                    "CSV": (f"mechanism.csv", f"{file_name}.csv"),
                    "Database": (f"{file_name}.json", f"{file_name}.json"),
                    "CAD": ("mechanism.scad", f"{file_name}.scad"),
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
                mime="application/zip",
            )

# Report tab to show the Points, Connections, Dof, Residual Error and Trajectory
elif tab == "Report":
    if "calculation" not in st.session_state:
        st.session_state["calculation"] = False

    if st.session_state["calculation"]:

        st.subheader("Points")
        st.write("The following table shows the points of the mechanism.")

        points = (
            fixeddot.get_instances()
            + swivel.get_instances()
            + movabledot.get_instances()
        )
        points_df = pd.DataFrame(points)
        points_df.columns = ["Points"]
        st.dataframe(points_df)

        st.subheader("Connections")
        st.write("The following table shows the connections between the points.")
        connections = connectionlinks.get_instances()
        connections_df = pd.DataFrame(connections)
        connections_df.columns = ["Connections"]
        st.dataframe(connections_df)

        st.subheader("Degree of Freedom")
        dof = st.session_state["calc"].check_dof()
        st.write(f"The mechanism has {dof} degree of freedom.")
        st.write(
            "that means the mechanism is kinematically determined."
            if dof == 0
            else "that means the mechanism is kinematically undetermined."
        )

        st.subheader("Residual Error")
        st.image(
            "src/ErrorPlot.png", caption="Residual Error Plot", use_container_width=True
        )
        st.write(
            "The residual error plot shows the error between the calculated and the desired lengths of the connections for 360 degree."
        )
        st.subheader("Trajectory")
        st.image(
            "src/Animation_last_frame.png",
            caption="Trajectory Plot",
            use_container_width=True,
        )
        st.write(
            f"The trajectory plot shows the mechanism({st.session_state["file_name"]})of the selected point {st.session_state["p_c"]}."
        )

    else:
        st.warning("Please calculate the mechanism first.")
        st.stop()
