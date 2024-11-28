import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Classe base para corpos celestes
class Body:
    def __init__(self, name, mass, position, velocity):
        self.name = name
        self.mass = mass
        self.position = position  # [x, y] em metros
        self.velocity = velocity  # [vx, vy] em m/s
        self.force = [0, 0]  # Força acumulada [Fx, Fy]

    def update_position(self, dt):
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def update_velocity(self, dt):
        ax = self.force[0] / self.mass
        ay = self.force[1] / self.mass
        self.velocity[0] += ax * dt
        self.velocity[1] += ay * dt

    def reset_force(self):
        self.force = [0, 0]

    def type_info(self):
        return "Generic Body"

# Classe para estrelas
class Star(Body):
    def __init__(self, name, mass, position, velocity, temperature):
        super().__init__(name, mass, position, velocity)
        self.temperature = temperature  # Temperatura da estrela em Kelvin

    def type_info(self):
        return "Star"

# Classe para planetas
class Planet(Body):
    def __init__(self, name, mass, position, velocity, has_atmosphere):
        super().__init__(name, mass, position, velocity)
        self.has_atmosphere = has_atmosphere  # Indica se o planeta tem atmosfera

    def type_info(self):
        return "Planet"

# Classe para satélites
class Satellite(Body):
    def __init__(self, name, mass, position, velocity, parent_body):
        super().__init__(name, mass, position, velocity)
        self.parent_body = parent_body  # Corpo ao qual o satélite orbita

    def type_info(self):
        return "Satellite"

# Classe de simulação
class Simulation:
    def __init__(self, bodies, G=6.67430e-11):
        self.bodies = bodies
        self.G = G
        self.traces = {body.name: [[], []] for body in bodies}  # Rastros para visualização

    def compute_gravitational_forces(self):
        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    dx = body2.position[0] - body1.position[0]
                    dy = body2.position[1] - body1.position[1]
                    distance = math.sqrt(dx**2 + dy**2)
                    if distance == 0:
                        continue
                    force_magnitude = self.G * body1.mass * body2.mass / distance**2
                    fx = force_magnitude * dx / distance
                    fy = force_magnitude * dy / distance
                    body1.force[0] += fx
                    body1.force[1] += fy

    def update(self, dt):
        self.compute_gravitational_forces()
        for body in self.bodies:
            body.update_velocity(dt)
            body.update_position(dt)
            self.traces[body.name][0].append(body.position[0])  # Atualiza rastro x
            self.traces[body.name][1].append(body.position[1])  # Atualiza rastro y
            body.reset_force()

# Função para criar visualização
def visualize_simulation(sim, steps, dt):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_xlim(-2e11, 2e11)  # Ajustar o tamanho do gráfico conforme o sistema
    ax.set_ylim(-2e11, 2e11)
    ax.set_title("Orbital Simulation")
    ax.set_xlabel("X Position (m)")
    ax.set_ylabel("Y Position (m)")

    # Elementos gráficos
    points = {body.name: ax.plot([], [], 'o', label=body.name)[0] for body in sim.bodies}
    traces = {body.name: ax.plot([], [], '-', alpha=0.5)[0] for body in sim.bodies}

    def init():
        for point in points.values():
            point.set_data([], [])
        for trace in traces.values():
            trace.set_data([], [])
        return list(points.values()) + list(traces.values())

    def update(frame):
        sim.update(dt)
        for body in sim.bodies:
            x, y = body.position
            points[body.name].set_data(x, y)
            traces[body.name].set_data(sim.traces[body.name][0], sim.traces[body.name][1])
        return list(points.values()) + list(traces.values())

    ani = FuncAnimation(fig, update, frames=steps, init_func=init, blit=True, interval=50)
    ax.legend()
    plt.show()

# Criando objetos
sun = Star("Sun", 1.989e30, [0, 0], [0, 0], temperature=5778)
earth = Planet("Earth", 5.972e24, [1.496e11, 0], [0, 29780], has_atmosphere=True)
moon = Satellite("Moon", 7.348e22, [1.496e11 + 384400000, 0], [0, 29780 + 1022], parent_body=earth)

# Configurando simulação
sim = Simulation([sun, earth, moon])

# Visualizar simulação
visualize_simulation(sim, steps=500, dt=3600)  # 500 passos, cada um com 1 hora de duração
