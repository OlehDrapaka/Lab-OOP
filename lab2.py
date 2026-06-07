import asyncio
import random
import time
import networkx as nx
import matplotlib.pyplot as plt


class Packet:
    def __init__(self, src, dest, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []


class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
            node.connections.append(self)

    async def send(self, packet, network):
        await asyncio.sleep(random.uniform(0.05, 0.3))
        if random.random() < network.loss_rate:
            network.packets_lost += 1
            return
        await self.forward(packet, network)

    async def forward(self, packet, network):
        if self == packet.dest:
            return
        if self in packet.visited:
            return

        packet.visited.append(self)
        for node in self.connections:
            if node not in packet.visited:
                await node.send(packet, network)

class Router(Node):
    pass


class TCPProtocol:
    name = "TCP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)


class UDPProtocol:
    name = "UDP"

    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)


class Network:
    def __init__(self, name):
        self.name = name
        self.nodes = []
        self.loss_rate = random.uniform(0.10, 0.15)

        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=10):
        print(f"\n[{self.name}] Початок симуляції ({protocol.name})...")
        tasks = []
        for _ in range(packets):
            src, dest = random.sample(self.nodes, 2)
            self.packets_sent += 1
            start_time = time.time()

            async def send_and_track(s, d, p, st):
                await p.transmit(s, d, self)
                self.total_time += (time.time() - st)

            tasks.append(send_and_track(src, dest, protocol, start_time))

        await asyncio.gather(*tasks)

    def analyze(self):
        if self.packets_sent == 0:
            return

        avg_time = self.total_time / self.packets_sent  # [cite: 429]
        loss_percentage = (self.packets_lost / self.packets_sent) * 100  # [cite: 430]
        bandwidth = (
        self.packets_sent - self.packets_lost) / self.total_time if self.total_time > 0 else 0

        print(f"--- Результати для {self.name} ---")
        print(f"Середній час передачі: {avg_time:.4f} с")
        print(f"Втрати пакетів: {loss_percentage:.2f}%")
        print(f"Пропускна здатність: {bandwidth:.2f} пак/с")

    def visualize(self):
        G = nx.Graph()
        for node in self.nodes:
            G.add_node(node.name)
            for conn in node.connections:
                G.add_edge(node.name, conn.name)

        plt.figure(figsize=(6, 4))
        nx.draw(G, with_labels=True, node_color="skyblue", node_size=2500, font_size=10, font_weight="bold")
        plt.title(f"Топологія: {self.name}")
        plt.show()


async def main():
    star_net = Network("Зіркова (Star)")
    router = Router("Router")
    star_pcs = [Node(f"PC{i}") for i in range(1, 6)]
    star_net.nodes = [router] + star_pcs
    for pc in star_pcs:
        router.connect(pc)

    mesh_net = Network("Сіткова (Mesh)")
    mesh_pcs = [Node(f"M_PC{i}") for i in range(1, 6)]
    mesh_net.nodes = mesh_pcs
    for i in range(len(mesh_pcs)):
        for j in range(i + 1, len(mesh_pcs)):
            mesh_pcs[i].connect(mesh_pcs[j])

    await star_net.simulate(TCPProtocol, packets=30)
    star_net.analyze()
    star_net.visualize()

    await mesh_net.simulate(UDPProtocol, packets=30)
    mesh_net.analyze()
    mesh_net.visualize()


if __name__ == "__main__":
    asyncio.run(main())