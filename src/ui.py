import streamlit as st
import pandas as pd
from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
from calculation_class import Calculation

st.title("Planar Mechanisms")

# Tabs for navigation
tab = st.sidebar.radio("Select Section", ["Declaration", "Plot"])

if "points_data" not in st.session_state:
    st.session_state["points_data"] = []
if "connections_data" not in st.session_state:
    st.session_state["connections_data"] = []

# Define everything under the Declaration tab
if tab == "Declaration":
    init, prev = st.columns(2)
    # Select number of movable points
    with init:
        st.subheader("Define Points")
        num_movable_points = st.number_input("Number of movable points", min_value=1, max_value=10, value=3)
        
        # Default data for fixed point, swivel point, and movable points
        points_data = [
            {"Point": "P0", "X": 0.0, "Y": 0.0, "Type": "Fixed Point", "Radius": None},
            {"Point": "P1", "X": 5.0, "Y": 5.0, "Type": "Swivel Point", "Radius": 1.0}
        ]

        for i in range(num_movable_points):
            points_data.append({"Point": f"P{i+2}", "X": 0.0, "Y": 0.0, "Type": "Movable Point", "Radius": None})

        # Create DataFrame
        df = pd.DataFrame(points_data)

        # Editable table
        edited_df = st.data_editor(
            df,
            column_config={
                "Type": st.column_config.SelectboxColumn(
                    "Point Type",
                    options=["Fixed Point", "Swivel Point", "Movable Point"],
                    disabled=[True, True] + [False] * num_movable_points  # Fix Fixed & Swivel points
                ),
                "Radius": st.column_config.NumberColumn(
                    "Radius",
                    min_value=0.0,
                    format="%.2f"
                )
            },
            hide_index=True
        )

        # Store points in classes based on type
        points_objects = {}

        for _, row in edited_df.iterrows():
            point_id = row["Point"]
            x, y, typ, radius = row["X"], row["Y"], row["Type"], row["Radius"]
            
            if typ == "Fixed Point":
                points_objects[point_id] = fixeddot(x, y)
            elif typ == "Swivel Point":
                points_objects[point_id] = swivel(x, y, radius, 0)
            elif typ == "Movable Point":
                points_objects[point_id] = movabledot(x, y)

        # Connection selection
        st.subheader("Define Connections")
        
        # List of all point IDs for dropdown
        point_ids = [row["Point"] for _, row in edited_df.iterrows()]

        # Initialize connection list
        connections = []
        
        num_connections = st.number_input("Number of connections", min_value=1, max_value=20, value=3)

        for i in range(num_connections):
            col1, col2 = st.columns(2)
            with col1:
                p1 = st.selectbox(f"Connection {i+1} - Point 1", point_ids, key=f"conn_{i}_p1")
            with col2:
                p2 = st.selectbox(f"Connection {i+1} - Point 2", point_ids, key=f"conn_{i}_p2")
            
            connections.append((p1, p2))

        # Save connections as connectionlinks objects
        connection_objects = [connectionlinks(points_objects[p1], points_objects[p2]) for p1, p2 in connections]
        
        # Reload button
        if "reload" in st.session_state:
            st.session_state["reload"] = False
        
        if st.button("Save Values"):
            st.session_state["points_data"] = edited_df.to_dict(orient="records")
            st.session_state["connections_data"] = connections
            st.rerun()
        st.session_state["calc"] = Calculation()
        
    with prev:
        st.subheader("Preview")
        if st.button("Preview"):
            for point_id, point in points_objects.items():
                st.write(f"{point_id}: {point}")
            st.write("Connections:")
            for conn in connection_objects:
                st.write(conn)
    
    st.divider()
    # Degree of Freedom (DOF) Analysis Button
    st.subheader("Degree of Freedom Analysis")
    if st.button("Check DOF"):
        if st.session_state["calc"].check_dof() == 0:
            st.success("Kinematically Determined System")
        else:
            st.error("Kinematically Undetermined System")

# Plot tab
elif tab == "Plot":
    st.subheader("Mechanism Visualization")

    data_source = st.selectbox(
        "Load Value",
        ["Use current Declaration data", "Load from database"]
    )

    if data_source == "Use current Declaration data":
        if st.session_state["points_data"]:
            st.write("🔹 Using stored points:", st.session_state["points_data"])
            st.write("🔗 Using stored connections:", st.session_state["connections_data"])
        else:
            st.warning("No saved values found!")

    elif data_source == "Load from database":
        st.info("Database loading functionality coming soon!")
