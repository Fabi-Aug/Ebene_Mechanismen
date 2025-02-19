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
tab = st.sidebar.radio("Select Section", ["Declaration", "Plot"])

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
        
        # Save Values button logic
        if "reload" not in st.session_state:
            st.session_state["reload"] = False
        
        if st.button("Save Values"):
            if not st.session_state["reload"]:
                st.session_state["reload"] = True
                st.session_state["points_data"] = edited_df.to_dict(orient="records")
                st.session_state["connections_data"] = connections
                st.rerun()
            else:
                st.session_state["reload"] = False
                Database.save_mechanism("test1.json")
        st.session_state["calc"] = Calculation()
        
    with prev:
        st.subheader("Preview")
        if st.button("Preview"):
            for point_id, point in st.session_state.points_objects.items():
                st.write(f"{point_id}: {point}")
            st.write("Connections:")
            for conn in connection_objects:
                st.write(conn)
    
    st.divider()
    st.subheader("Degree of Freedom Analysis")
    if st.button("Check DOF"):
        clear_all_inst()
        Database.load_mechanism("test1.json")
        st.session_state["calc"] = Calculation()
        st.write(st.session_state["calc"].__str__())
        if st.session_state["calc"].check_dof() == 0:
            st.success("Kinematically Determined System")
        else:
            st.error("Kinematically Undetermined System")
            st.write(f"Degree of Freedom: {st.session_state['calc'].check_dof()}")

elif tab == "Plot":
    st.subheader("Mechanism Visualization")
    data_source = st.selectbox(
        "Load Value",
        ["Use current Declaration data", "Load from database"]
    )
    if "point_ids" not in st.session_state or not st.session_state["point_ids"]:
        st.warning("No points available! Please define points in the Declaration tab.")
    else:
        p_c = st.selectbox("Select a point for plotting", st.session_state["point_ids"], key="plot_point")
    
    if st.button("plot"):
        if data_source == "Use current Declaration data":
            if st.session_state["points_data"]:
                st.session_state["calc"] = Calculation()
                st.session_state["calc"].trajectory()
                st.session_state["calc"].animate_plot(st.session_state.points_objects[st.session_state["point_ids"][2]])
                st.image("src/Animation.gif", caption="Mechanism Animation", use_container_width=True)
            else:
                st.warning("No saved values found!")
        elif data_source == "Load from database":
            st.info("Database loading functionality coming soon!")
