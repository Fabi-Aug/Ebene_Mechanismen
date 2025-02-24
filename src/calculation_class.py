from dot_class import dot
from connectinglinks_class import connectionlinks
from fixeddot_class import fixeddot
from swivel_class import swivel
from movabledot_class import movabledot
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
import numpy as np
import pandas as pd
import scipy.optimize as opt
import math
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import datetime
from database_class import Database


class Calculation:
    """
    A class that houses the calculation and the feature including methods.
    """

    def __init__(self):
        """
        Initializes the Calculation class by retrieving instances of dots, movable dots, connections, fixed dots, and swivels.
        Also calculates the number of dots and connections.
        """
        self._dots = dot.get_all_instances()
        self.movabledots = movabledot.get_instances()
        self._connections = connectionlinks.get_instances()
        self._fixeddots = fixeddot.get_instances()
        self._swivels = swivel.get_instances()
        self._n = len(self._dots)
        self._m = len(self._connections)

    def check_dof(self) -> int:
        """
        Calculate degrees of freedom using Grübler's equation.
        Returns the degrees of freedom as an integer.
        """
        N = len(self._dots)
        J = len(self._fixeddots) + len(self._swivels)
        M = len(self._connections)
        F = 2 * N - 2 * J - M
        return F

    def calculate(self, phi, phi2, params, l_c) -> np.ndarray:
        """
        Perform calculations for the mechanism based on given angles (phi, phi2) and parameters.
        Returns the error vector as a numpy array.
        """
        for instance in self._swivels:
            instance.set_phi(phi)
        if self.check_dof() != 0:
            raise ValueError(
                "The calculation is not possible, because the system is not statically determined."
            )
        for i, movable in enumerate(self.movabledots):
            x, y = params[2 * i : 2 * i + 2]
            movable.set_coordinates(x, y)
        for instance in self._swivels:
            instance.set_phi(phi2)
        l_n = np.zeros((0, 1))
        for connection in self._connections:
            l_n = np.vstack((l_n, [[connection.calc_length()]]))
        e = (l_n - l_c).flatten()
        return e

    def optimizer(self, phi, phi2, l_c) -> opt.OptimizeResult:
        """
        Optimize the mechanism configuration using least squares optimization.
        Returns the optimization result.
        """

        def objective(params):
            return self.calculate(phi, phi2, params, l_c)

        md = []
        for movable in self.movabledots:
            md.extend(movable.get_coordinates())
        result = opt.least_squares(objective, md)
        return result

    def trajectory(self):
        """
        Calculate the trajectory of the mechanism by optimizing the configuration for a range of angles.
        Raises a ValueError if the system is not statically determined.
        """
        angles = np.linspace(0, 2 * math.pi, 360)
        if self.check_dof() != 0:
            raise ValueError(
                "The calculation is not possible, because the system is not statically determined."
            )
        l_c = np.zeros((0, 1))
        for connection in self._connections:
            l_c = np.vstack((l_c, [[connection.calc_length()]]))
        self.residual_error = []
        for i in range(len(angles) - 1):
            result = self.optimizer(angles[i], angles[i + 1], l_c)
            self.residual_error.append(result.optimality)
            for instance in self.movabledots:
                instance.x_values.append(instance.get_coordinates()[0])
                instance.y_values.append(instance.get_coordinates()[1])
            for instance in self._swivels:
                instance.x_values.append(instance.get_coordinates()[0])
                instance.y_values.append(instance.get_coordinates()[1])
            for instance in self._fixeddots:
                instance.x_values.append(instance.get_coordinates()[0])
                instance.y_values.append(instance.get_coordinates()[1])
        print("Trajectory calculated")
        self.error_plot()

    def save_csv(self, path, id: str):
        """
        Save the trajectory of a specific dot to a CSV file at the given path.
        """
        dot = next((d for d in self._dots if d.id == id), None)
        if dot is None:
            print(f"No dot found with id {id}")
            return
        full_path = os.path.join("src", path)
        df = pd.DataFrame({"x": dot.x_values, "y": dot.y_values})
        df.to_csv(full_path, index=False)
        print(f"CSV saved as {full_path}")

    def static_plot(self):
        """
        Generate and save a static plot of the mechanism, showing fixed dots, swivels, connections, and movable dots.
        """
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.subplots_adjust(
            left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.2
        )
        for fixed in self._fixeddots:
            x_fixed, y_fixed = fixed.get_coordinates()
            ax.plot(x_fixed, y_fixed, "ro")
            ax.text(
                x_fixed + 0.1, y_fixed + 0.1, f"{fixed.id}", fontsize=12, color="black"
            )
        for swivel in self._swivels:
            ax.plot(swivel.x_m, swivel.y_m, "ro")
            x, y = swivel.get_coordinates()
            ax.plot(x, y, "bo")
            ax.text(x + 0.1, y + 0.1, f"{swivel.id}", fontsize=12, color="black")
            circle = patches.Circle(
                (swivel.x_m, swivel.y_m), swivel._r, edgecolor="black", facecolor="none"
            )
            ax.add_patch(circle)
        for connection in self._connections:
            dot1_x, dot1_y = connection.dot1.get_coordinates()
            dot2_x, dot2_y = connection.dot2.get_coordinates()
            ax.plot([dot1_x, dot2_x], [dot1_y, dot2_y], linestyle="-", color="gray")
        for movingdot in self.movabledots:
            x, y = movingdot.get_coordinates()
            ax.plot(x, y, "bo")
            ax.text(x + 0.1, y + 0.1, f"{movingdot.id}", fontsize=12, color="black")
        plt.autoscale()
        plt.savefig("src/StaticPlot.png")
        print("Static plot saved as 'src/StaticPlot.png'")

    def animate_plot(self, id: str):
        """
        Generate and save an animation of the mechanism, showing the trajectory of a specific dot.
        """
        dot_trajectory = next((d for d in self._dots if d.id == id), None)
        if dot_trajectory is None:
            print(f"No dot found with id {id}")
            return
        x_all = []
        y_all = []
        for dot in self._dots:
            x_all.append(dot.x_values)
            y_all.append(dot.y_values)

        def find_max(lst):
            return max(max(inner_list) for inner_list in lst)

        def find_min(lst):
            return min(min(inner_list) for inner_list in lst)

        fig, ax = plt.subplots(figsize=(5, 5))
        fig.subplots_adjust(
            left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.2
        )
        x_min, x_max = find_min(x_all), find_max(x_all)
        y_min, y_max = find_min(y_all), find_max(y_all)
        x_range = x_max - x_min
        y_range = y_max - y_min
        max_range = max(x_range, y_range)
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2
        ax.set_xlim(x_center - max_range / 2 - 10, x_center + max_range / 2 + 10)
        ax.set_ylim(y_center - max_range / 2 - 10, y_center + max_range / 2 + 10)
        (traj_line,) = ax.plot([], [], linestyle="-", color="blue", linewidth=2.5)
        for fixed in self._fixeddots:
            x_fixed, y_fixed = fixed.get_coordinates()
            ax.plot(x_fixed, y_fixed, "ro")
        circle_lines = []
        for swivel in self._swivels:
            ax.plot(swivel.x_m, swivel.y_m, "ro")
            (cline,) = ax.plot([], [], linestyle="-", color="black")
            circle_lines.append(cline)
        conn_lines = []
        for _ in self._connections:
            (cline,) = ax.plot([], [], linestyle="-", color="gray")
            conn_lines.append(cline)
        movingdot_lines = []
        swivel_lines = []
        n_frames = len(dot_trajectory.x_values) if dot_trajectory.x_values else 0

        def init():
            traj_line.set_data([], [])
            for cl in circle_lines:
                cl.set_data([], [])
            for cl in conn_lines:
                cl.set_data([], [])
            for movingdot_line in movingdot_lines:
                movingdot_line.set_data([], [])
            for swivel_line in swivel_lines:
                swivel_line.set_data([], [])
            return (
                [traj_line] + circle_lines + conn_lines + movingdot_lines + swivel_lines
            )

        def update(frame):
            traj_line.set_data(
                dot_trajectory.x_values[: frame + 1],
                dot_trajectory.y_values[: frame + 1],
            )
            for i, swivel in enumerate(self._swivels):
                if frame < len(swivel.x_values):
                    circle_lines[i].set_data(
                        swivel.x_values[: frame + 1], swivel.y_values[: frame + 1]
                    )
            for i, connection in enumerate(self._connections):
                if frame < len(connection.dot1.x_values) and frame < len(
                    connection.dot2.x_values
                ):
                    coord1_x = connection.dot1.x_values[frame]
                    coord1_y = connection.dot1.y_values[frame]
                    coord2_x = connection.dot2.x_values[frame]
                    coord2_y = connection.dot2.y_values[frame]
                conn_lines[i].set_data([coord1_x, coord2_x], [coord1_y, coord2_y])
            for i, movingdot in enumerate(self.movabledots):
                x = movingdot.x_values[frame]
                y = movingdot.y_values[frame]
                if i >= len(movingdot_lines):
                    (movingdot_line,) = ax.plot([], [], "bo")
                    movingdot_lines.append(movingdot_line)
                movingdot_lines[i].set_data([x], [y])
            for i, swivel in enumerate(self._swivels):
                x = swivel.x_values[frame]
                y = swivel.y_values[frame]
                if i >= len(swivel_lines):
                    (swivel_line,) = ax.plot([], [], "bo")
                    swivel_lines.append(swivel_line)
                swivel_lines[i].set_data([x], [y])
            return (
                [traj_line] + circle_lines + conn_lines + movingdot_lines + swivel_lines
            )

        ani = animation.FuncAnimation(
            fig,
            update,
            frames=n_frames,
            init_func=init,
            blit=False,
            repeat=False,
            interval=25,
        )
        ani.save("src/Animation.gif", writer="pillow", fps=30)
        plt.savefig("src/Animation_last_frame.png", dpi=600)
        print("Animation saved as 'src/Animation.gif'")

    def create_bom(self):
        """
        Generate and save a Bill of Materials (BOM) as a PDF, listing all components of the mechanism.
        """
        data = {"Checked": [], "Object": [], "Quantity": [], "Description": []}
        for i, fixed in enumerate(self._fixeddots):
            data["Object"].append(fixed.id)
            data["Quantity"].append(1)
            data["Description"].append("Two-point fixed support")
            data["Checked"].append("☐")
        for i, movable in enumerate(self.movabledots):
            data["Object"].append(movable.id)
            data["Quantity"].append(1)
            data["Description"].append("Joint")
            data["Checked"].append("☐")
        for i, swivel in enumerate(self._swivels):
            data["Object"].append(swivel.id)
            data["Quantity"].append(1)
            data["Description"].append(f"Crank mechanism with radius {swivel._r:.2f}")
            data["Checked"].append("☐")
        connection_lengths = {}
        for connection in self._connections:
            length = connection.calc_length()
            if length in connection_lengths:
                connection_lengths[length]["Quantity"] += 1
                connection_lengths[length][
                    "Object"
                ] += f", {connection.dot1.id}-{connection.dot2.id}"
            else:
                connection_lengths[length] = {
                    "Object": f"{connection.dot1.id}-{connection.dot2.id}",
                    "Quantity": 1,
                    "Description": f"Connection with length {connection.calc_length():.2f}",
                    "Checked": "☐",
                }
        for conn in connection_lengths.values():
            data["Object"].append(conn["Object"])
            data["Quantity"].append(conn["Quantity"])
            data["Description"].append(conn["Description"])
            data["Checked"].append("☐")
        df = pd.DataFrame(data)
        pdf_filename = "src/bom.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter
        margin = 50
        y_position = height - margin
        c.setFont("Helvetica-Bold", 20)
        c.drawString(width / 2 - 60, y_position, "Bill of Materials")
        y_position -= 30
        col_widths = {"Checked": 60, "Object": 120, "Quantity": 60, "Description": 275}
        c.setFont("Helvetica-Bold", 10)
        table_headers = df.columns.tolist()
        x_position = margin
        for header in table_headers:
            c.setFillColor(HexColor("#7bb0e0"))
            c.rect(x_position, y_position, col_widths[header], 15, fill=1)
            c.setFillColor(HexColor("#000000"))
            c.drawString(x_position + 5, y_position + 3, header)
            x_position += col_widths[header]
        y_position -= 15
        c.setFont("Helvetica", 10)
        for index, row in df.iterrows():
            x_position = margin
            if index % 2 == 0:
                row_color = HexColor("#a8a7a2")
            else:
                row_color = HexColor("#ffffff")
            c.setFillColor(row_color)
            c.rect(x_position, y_position, sum(col_widths.values()), 15, fill=1)
            for i, value in enumerate(row):
                c.setFillColor(HexColor("#000000"))
                c.drawString(x_position + 5, y_position + 3, str(value))
                x_position += col_widths[table_headers[i]]
            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(0.5)
            c.line(margin, y_position, margin + sum(col_widths.values()), y_position)
            y_position -= 15
            if y_position < margin:
                c.showPage()
                c.setFont("Helvetica-Bold", 10)
                y_position = height - margin
        c.setStrokeColor(HexColor("#000000"))
        c.setLineWidth(0.5)
        c.line(margin, y_position, margin + sum(col_widths.values()), y_position)
        c.drawString(
            margin,
            y_position - 20,
            f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )
        c.save()
        print(f"BOM saved as {pdf_filename}")

    def generate_openscad(self, filename="mechanism.scad"):
        """
        Generate and save OpenSCAD code for visualizing the mechanism.
        """
        scad_code = []
        scad_code.append("// OpenSCAD code for mechanism visualization")
        scad_code.append("$fn=50; // Smooth rendering")
        for fixed in self._fixeddots:
            x, y = fixed.get_coordinates()
            scad_code.append(f'color("red" )')
            scad_code.append(f"translate([{x}, {y},-1]) cylinder(h=2,r=2);")
        for movable in self.movabledots:
            x, y = movable.get_coordinates()
            scad_code.append(f'color("blue")')
            scad_code.append(f"translate([{x}, {y},-1]) cylinder(h=2,r=2);")
        for swivel in self._swivels:
            x_m, y_m = swivel.x_m, swivel.y_m
            scad_code.append(f'color("red")')
            scad_code.append(
                f"translate([{x_m}, {y_m},-3]) cylinder(h=2,r={swivel._r});"
            )
            x, y = swivel.get_coordinates()
            scad_code.append(f'color("blue")')
            scad_code.append(f"translate([{x}, {y},-1]) cylinder(h=2,r=2);")

        scad_code.append(
            "module connection(p1, p2) {{dx = p2[0] - p1[0]; dy = p2[1] - p1[1]; length = sqrt(dx*dx + dy*dy); translate(p1) {{rotate([0, 0, atan2(dy, dx)]) {{translate([length/2, 0, 0]) cube([length, 2, 2], center=true); }}}}}}"
        )

        for connection in self._connections:
            x1, y1 = connection.dot1.get_coordinates()
            x2, y2 = connection.dot2.get_coordinates()
            scad_code.append(f'color("gray")')
            scad_code.append(f"connection([{x1}, {y1},0], [{x2}, {y2},0]);")
        path = os.path.join("src", filename)
        with open(path, "w") as file:
            file.write("\n".join(scad_code))
        print(f"OpenSCAD code saved as {filename}")

    def get_dot_ids(self):
        """
        Get IDs of all movable dots.
        Returns a list of IDs.
        """
        ids = []
        for instance in self.movabledots:
            ids.append(instance.id)
        return ids

    def error_plot(self):
        """
        Generate and save a plot of the residual error over a range of angles.
        """
        plt.figure(figsize=(10, 5))
        x_values = np.linspace(1, 360, num=359)
        plt.plot(x_values, self.residual_error, label="Residual Error", color="b")
        plt.xlabel("phi")
        plt.ylabel("Residual Error")
        plt.grid(True)
        plt.savefig("src/ErrorPlot.png")
        print("Error plot saved as 'src/ErrorPlot.png'")

    def __str__(self):
        """
        Returns a string representation of the Calculation object, including details of dots, connections, fixed dots, and swivels.
        """
        return f"Calculation: dots:{self._dots}\nconnections:{self._connections}\nfixeddots:{self._fixeddots}\nswivels:{self._swivels}\n"


if __name__ == "__main__":

    Database.load_mechanism("strandbeest.json")
    # Database.load_mechanism("mechanism.json")
    # Database.load_mechanism("two_legged_strandbeest.json")

    calc = Calculation()

    calc.create_bom()
    calc.static_plot()
    calc.generate_openscad()
    calc.trajectory()
    # select an existing dot id to save its trajectory
    calc.save_csv("test.csv", "e")
    calc.animate_plot("e")
    calc.error_plot()
