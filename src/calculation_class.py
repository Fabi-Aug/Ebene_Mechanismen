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
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
import datetime


class Calculation:
    """
    A class that represents a calculation, plotting and saving of a 2D plane."""

    def __init__(self):
        self._dots = dot.get_all_instances()
        self.movabledots = movabledot.get_instances()
        self._connections = connectionlinks.get_instances()
        self._fixeddots = fixeddot.get_instances()
        self._swivels = swivel.get_instances()
        self._n = len(self._dots)
        self._m = len(self._connections)

    def check_dof(self):
        f = 2 * self._n - 2 - 2 - self._m
        # print(f"Degrees of freedom: {f}")
        return f

    def calculate(self, phi, phi2, params):
        for instance in self._swivels:
            instance.set_phi(phi)
        if self.check_dof() != 0:
            raise ValueError(
                "The calculation is not possible, because the system is not statically determined."
            )

        l_c = np.zeros((0, 1))
        for connection in self._connections:
            l_c = np.vstack((l_c, [[connection.calc_length()]]))

        for i, movable in enumerate(self.movabledots):
            x, y = params[2 * i : 2 * i + 2]
            movable.set_coordinates(x, y)

        for instance in self._swivels:
            instance.set_phi(phi2)
        l_n = np.zeros((0, 1))
        for connection in self._connections:
            l_n = np.vstack((l_n, [[connection.calc_length()]]))

        e = (l_n - l_c).flatten()
        # print(f"Error: {e}")
        return e

    def optimizer(self, phi, phi2):
        def objective(params):
            return self.calculate(phi, phi2, params)

        md = []
        for movable in self.movabledots:
            md.extend(movable.get_coordinates())

        result = opt.least_squares(objective, md)
        # print(result)
        return result.x

    def trajectory(self):
        angles = np.linspace(0, 2 * math.pi, 360)  # 1000 Werte zwischen 0 und 2π
        for i in range(len(angles) - 1):
            self.optimizer(angles[i], angles[i + 1])  # Optimierung ausführen

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

    def save_csv(self, path, dot: movabledot):
        full_path = os.path.join("src", path)
        df = pd.DataFrame({"x": dot.x_values, "y": dot.y_values})
        df.to_csv(full_path, index=False)
        print(f"CSV saved as {full_path}")

    def static_plot(self):
        fig, ax = plt.subplots(figsize=(5, 5))
        fig.subplots_adjust(
            left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.2, hspace=0.2
        )

        # Fixed dots (rote Punkte)
        for fixed in self._fixeddots:
            x_fixed, y_fixed = fixed.get_coordinates()
            ax.plot(x_fixed, y_fixed, "ro")
            # Text neben dem Punkt
            ax.text(
                x_fixed + 0.1, y_fixed + 0.1, f"{fixed.id}", fontsize=12, color="black"
            )

        # Swivel dots (rote und blaue Punkte mit Kreisen)
        for swivel in self._swivels:
            ax.plot(swivel.x_m, swivel.y_m, "ro")
            x, y = swivel.get_coordinates()
            ax.plot(x, y, "bo")
            # Text neben dem Punkt
            ax.text(x + 0.1, y + 0.1, f"{swivel.id}", fontsize=12, color="black")

            # Kreis für den Swivel-Punkt
            circle = patches.Circle(
                (swivel.x_m, swivel.y_m), swivel._r, edgecolor="black", facecolor="none"
            )
            ax.add_patch(circle)

        # Verbindungen (Linien zwischen den Punkten)
        for connection in self._connections:
            dot1_x, dot1_y = connection.dot1.get_coordinates()
            dot2_x, dot2_y = connection.dot2.get_coordinates()
            ax.plot([dot1_x, dot2_x], [dot1_y, dot2_y], linestyle="-", color="gray")

        # Bewegliche Punkte (blaue Punkte)
        for movingdot in self.movabledots:
            x, y = movingdot.get_coordinates()
            ax.plot(x, y, "bo")
            # Text neben dem Punkt
            ax.text(x + 0.1, y + 0.1, f"{movingdot.id}", fontsize=12, color="black")

        # Skalierung und Speichern
        plt.autoscale()
        plt.savefig("src/StaticPlot.png")
        print("Static plot saved as 'src/StaticPlot.png'")

    def animate_plot(self, dot_trajectory: movabledot):
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

        # Min/Max-Werte für X- und Y-Achse berechnen
        x_min, x_max = find_min(x_all), find_max(x_all)
        y_min, y_max = find_min(y_all), find_max(y_all)

        # Spannweite berechnen
        x_range = x_max - x_min
        y_range = y_max - y_min

        # Größere Range wählen
        max_range = max(x_range, y_range)

        # X- und Y-Achsen anpassen, damit sie gleich groß sind
        x_center = (x_max + x_min) / 2
        y_center = (y_max + y_min) / 2

        ax.set_xlim(x_center - max_range / 2 - 10, x_center + max_range / 2 + 10)
        ax.set_ylim(y_center - max_range / 2 - 10, y_center + max_range / 2 + 10)

        # 1. Erzeuge eine Linie für den übergebenen movabledot (Trajektorie, blau)
        (traj_line,) = ax.plot([], [], linestyle="-", color="blue", linewidth=2.5)

        # 2. Zeichne fixeddots (rote Punkte)
        for fixed in self._fixeddots:
            x_fixed, y_fixed = fixed.get_coordinates()
            ax.plot(x_fixed, y_fixed, "ro")

        # 3. Zeichne Swivels (rote Punkte) und deren Trajektorie (circle_line, schwarz)
        circle_lines = []
        for swivel in self._swivels:
            ax.plot(swivel.x_m, swivel.y_m, "ro")
            (cline,) = ax.plot([], [], linestyle="-", color="black")
            circle_lines.append(cline)

        # 4. Erzeuge Verbindungslinien (graue Linien)
        conn_lines = []
        for _ in self._connections:
            (cline,) = ax.plot([], [], linestyle="-", color="gray")
            conn_lines.append(cline)

        # 5. Erstelle eine leere Liste für die `movingdots`-Punkte
        movingdot_lines = []

        # 6. Erstelle eine leere Liste für die "swivel"-Punkte
        swivel_lines = []

        # Anzahl der Frames = Maximale Anzahl der Werte im übergebenen movabledot
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
            # 1. Aktualisiere die Trajektorie des übergebenen movabledot
            traj_line.set_data(
                dot_trajectory.x_values[: frame + 1],
                dot_trajectory.y_values[: frame + 1],
            )

            # 2. Aktualisiere die Trajektorien der Swivels
            for i, swivel in enumerate(self._swivels):
                if frame < len(swivel.x_values):
                    circle_lines[i].set_data(
                        swivel.x_values[: frame + 1], swivel.y_values[: frame + 1]
                    )

            # 3. Aktualisiere die Verbindungslinien
            for i, connection in enumerate(self._connections):
                if frame < len(connection.dot1.x_values) and frame < len(
                    connection.dot2.x_values
                ):
                    coord1_x = connection.dot1.x_values[frame]
                    coord1_y = connection.dot1.y_values[frame]
                    coord2_x = connection.dot2.x_values[frame]
                    coord2_y = connection.dot2.y_values[frame]

                conn_lines[i].set_data([coord1_x, coord2_x], [coord1_y, coord2_y])

            # 4. Lösche die vorherigen Punkte der `movingdots` und plotte nur den aktuellen Punkt
            for i, movingdot in enumerate(self.movabledots):
                x = movingdot.x_values[frame]
                y = movingdot.y_values[frame]

                if i >= len(movingdot_lines):
                    (movingdot_line,) = ax.plot([], [], "bo")
                    movingdot_lines.append(movingdot_line)

                # Setze nur den aktuellen Punkt
                movingdot_lines[i].set_data([x], [y])

            for i, swivel in enumerate(self._swivels):
                x = swivel.x_values[frame]
                y = swivel.y_values[frame]

                if i >= len(swivel_lines):
                    (swivel_line,) = ax.plot([], [], "bo")
                    swivel_lines.append(swivel_line)

                # Setze nur den aktuellen Punkt
                swivel_lines[i].set_data([x], [y])

            # 5. Passe die Achsen an
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
        # plt.show()
        ani.save("src/Animation.gif", writer="pillow", fps=30)
        print("Animation saved as 'src/Animation.gif'")

    def create_bom(self):  # Bill of Materials
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

        # Convert the data dictionary to a pandas DataFrame
        df = pd.DataFrame(data)

        # Create the PDF with ReportLab
        pdf_filename = "src/bom.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        width, height = letter  # Dimensions for the letter page size
        margin = 50
        y_position = height - margin

        # Add title
        c.setFont("Helvetica-Bold", 20)
        c.drawString(width / 2 - 60, y_position, "Bill of Materials")
        y_position -= 30

        # Define column widths
        col_widths = {"Checked": 60, "Object": 120, "Quantity": 60, "Description": 275}

        # Draw the table headers
        c.setFont("Helvetica-Bold", 10)
        table_headers = df.columns.tolist()
        x_position = margin
        for header in table_headers:
            c.setFillColor(HexColor("#7bb0e0"))  # Set header background color
            c.rect(x_position, y_position, col_widths[header], 15, fill=1)
            c.setFillColor(HexColor("#000000"))  # Set text color to black
            c.drawString(x_position + 5, y_position + 3, header)
            x_position += col_widths[header]  # Adjust column width based on dictionary
        y_position -= 15

        # Draw the table rows
        c.setFont("Helvetica", 10)
        for index, row in df.iterrows():
            x_position = margin
            # Alternate row colors for readability
            if index % 2 == 0:
                row_color = HexColor("#a8a7a2")  # Light grey for even rows
            else:
                row_color = HexColor("#ffffff")  # White for odd rows

            # Draw row background color
            c.setFillColor(row_color)
            c.rect(x_position, y_position, sum(col_widths.values()), 15, fill=1)

            # Draw the content in each cell
            for i, value in enumerate(row):
                c.setFillColor(HexColor("#000000"))  # Set text color to black
                c.drawString(x_position + 5, y_position + 3, str(value))
                x_position += col_widths[
                    table_headers[i]
                ]  # Adjust column width based on dictionary

            # Draw horizontal line for the row
            c.setStrokeColor(HexColor("#000000"))
            c.setLineWidth(0.5)
            c.line(margin, y_position, margin + sum(col_widths.values()), y_position)

            y_position -= 15

            # Add page if we reach the bottom of the page
            if y_position < margin:
                c.showPage()
                c.setFont("Helvetica-Bold", 10)
                y_position = height - margin  # Reset y position for the new page

        c.setStrokeColor(HexColor("#000000"))
        c.setLineWidth(0.5)
        c.line(margin, y_position, margin + sum(col_widths.values()), y_position)
        c.drawString(
            margin,
            y_position - 20,
            f"Generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}",
        )

        # Save the PDF
        c.save()
        print(f"BOM saved as {pdf_filename}")

    def __str__(self):
        return f"Calculation: dots:{self._dots}\nconnections:{self._connections}\nfixeddots:{self._fixeddots}\nswivels:{self._swivels}\n"


if __name__ == "__main__":
    d0 = fixeddot(0, 0, "d0")
    d1 = movabledot(10, 35, "d1")
    # d2 = movabledot(5,10)
    s1 = swivel(-30, 0, (5**2 + 10**2) ** 0.5, math.atan(10 / 5), "s1")

    c1 = connectionlinks(d0, d1)
    c2 = connectionlinks(d1, s1)
    # c3 = connectionlinks(d2, s1)
    # c4 = connectionlinks(d2, d0)
    calc = Calculation()
    calc.create_bom()
    calc.static_plot()
    # print(c4.calc_length())
    # print(c3.calc_length())
    calc.trajectory()
    calc.animate_plot(d1)
    calc.save_csv("test.csv", d1)
    # angles = np.linspace(0, 2 * math.pi, 360)  # 1000 Werte zwischen 0 und 2π

    # calc.save_csv("C:/Schule_24-25/Python_Schule/AbschlussProjekt/Ebene_Mechanismen/src/test.csv", d2)

    # Plot für X- und Y-Werte
    # plt.figure(figsize=(8, 6))
    # plt.plot( x_values,y_values, color="blue")
    # plt.xlim(-40, 20)
    # plt.ylim(-10, 40)
    # plt.show()
