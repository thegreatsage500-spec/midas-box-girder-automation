#!/usr/bin/env python3
"""
Box Girder Bridge Model Generator for Midas Civil
Specifications:
- Length: 54.9m
- Deck width: 12m
- Overall depth: 3.225m
- Cantilever end: 2.75m
- Bottom width (outer): 4m
- Webs: Inclined
"""

import math

class BoxGirderGenerator:
    def __init__(self):
        # Main parameters
        self.length = 54.9
        self.deck_width = 12.0
        self.overall_depth = 3.225
        self.cantilever_length = 2.75
        self.bottom_width = 4.0
        
        # Derived parameters
        self.span_length = self.length - 2 * self.cantilever_length  # 49.4m
        self.overhang_left = self.cantilever_length
        self.overhang_right = self.cantilever_length
        
        # Web inclination angle (degrees) - adjust as needed
        self.web_inclination = 10  # degrees
        
        # Node and element counters
        self.node_id = 1
        self.element_id = 1
        self.nodes = {}
        self.elements = []
        
    def calculate_web_offset(self, depth):
        """Calculate horizontal offset of web due to inclination"""
        return depth * math.tan(math.radians(self.web_inclination))
    
    def generate_deck_nodes(self):
        """Generate nodes for top deck"""
        nodes_data = []
        web_offset = self.calculate_web_offset(self.overall_depth)
        
        # Deck corners - longitudinal divisions every 1m
        for i in range(int(self.length) + 1):
            x = i
            
            # Left edge
            y = -self.deck_width / 2
            z = self.overall_depth
            self.nodes[f"deck_L_{i}"] = (self.node_id, x, y, z)
            nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
            self.node_id += 1
            
            # Right edge
            y = self.deck_width / 2
            self.nodes[f"deck_R_{i}"] = (self.node_id, x, y, z)
            nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
            self.node_id += 1
        
        return nodes_data
    
    def generate_bottom_nodes(self):
        """Generate nodes for bottom slab"""
        nodes_data = []
        web_offset = self.calculate_web_offset(self.overall_depth)
        
        for i in range(int(self.length) + 1):
            x = i
            
            # Left edge (outer)
            y = -(self.bottom_width / 2)
            z = 0
            self.nodes[f"bottom_L_{i}"] = (self.node_id, x, y, z)
            nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
            self.node_id += 1
            
            # Right edge (outer)
            y = self.bottom_width / 2
            self.nodes[f"bottom_R_{i}"] = (self.node_id, x, y, z)
            nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
            self.node_id += 1
        
        return nodes_data
    
    def generate_web_nodes(self):
        """Generate nodes for inclined webs"""
        nodes_data = []
        
        for i in range(int(self.length) + 1):
            x = i
            web_offset = self.calculate_web_offset(self.overall_depth)
            
            # Left web - bottom
            y = -(self.bottom_width / 2)
            z = 0
            
            # Left web - top (offset due to inclination)
            y_top = -(self.deck_width / 2)
            z_top = self.overall_depth
            
            # Nodes along left web
            for j in range(3):  # 3 nodes per web section
                t = j / 2.0
                y = -(self.bottom_width / 2) + (y_top - (-(self.bottom_width / 2))) * t
                z = 0 + (z_top - 0) * t
                self.nodes[f"web_L_{i}_{j}"] = (self.node_id, x, y, z)
                nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
                self.node_id += 1
            
            # Right web
            for j in range(3):
                t = j / 2.0
                y = (self.bottom_width / 2) + ((self.deck_width / 2) - (self.bottom_width / 2)) * t
                z = 0 + (z_top - 0) * t
                self.nodes[f"web_R_{i}_{j}"] = (self.node_id, x, y, z)
                nodes_data.append(f"Node {self.node_id}: ({x}, {y}, {z})")
                self.node_id += 1
        
        return nodes_data
    
    def generate_elements(self):
        """Generate shell elements for box girder"""
        elements_data = []
        
        # Top deck elements
        for i in range(int(self.length)):
            node1 = self.nodes[f"deck_L_{i}"][0]
            node2 = self.nodes[f"deck_L_{i+1}"][0]
            node3 = self.nodes[f"deck_R_{i+1}"][0]
            node4 = self.nodes[f"deck_R_{i}"][0]
            self.elements.append((self.element_id, node1, node2, node3, node4))
            elements_data.append(f"Element {self.element_id}: Quad {node1}-{node2}-{node3}-{node4}")
            self.element_id += 1
        
        # Bottom slab elements
        for i in range(int(self.length)):
            node1 = self.nodes[f"bottom_L_{i}"][0]
            node2 = self.nodes[f"bottom_L_{i+1}"][0]
            node3 = self.nodes[f"bottom_R_{i+1}"][0]
            node4 = self.nodes[f"bottom_R_{i}"][0]
            self.elements.append((self.element_id, node1, node2, node3, node4))
            elements_data.append(f"Element {self.element_id}: Quad {node1}-{node2}-{node3}-{node4}")
            self.element_id += 1
        
        return elements_data
    
    def generate_supports(self):
        """Generate support nodes at main and end supports"""
        supports_data = []
        
        # Support locations (at 0m, 27.45m, 54.9m for 3-span configuration)
        support_locations = [self.overhang_left, self.overhang_left + self.span_length / 2, self.length - self.overhang_right]
        
        for loc in support_locations:
            idx = int(loc)
            if idx < int(self.length):
                node_id = self.nodes[f"bottom_L_{idx}"][0]
                supports_data.append(f"Support at Node {node_id} (x={loc}m): Fixed")
        
        return supports_data
    
    def export_to_text(self):
        """Export model data to readable text format"""
        output = []
        output.append("="*70)
        output.append("BOX GIRDER BRIDGE MODEL - MIDAS CIVIL")
        output.append("="*70)
        output.append("")
        
        output.append("SPECIFICATIONS:")
        output.append(f"  Total Length: {self.length}m")
        output.append(f"  Deck Width: {self.deck_width}m")
        output.append(f"  Overall Depth: {self.overall_depth}m")
        output.append(f"  Cantilever Length: {self.cantilever_length}m (each end)")
        output.append(f"  Main Span: {self.span_length}m")
        output.append(f"  Bottom Width (outer-to-outer): {self.bottom_width}m")
        output.append(f"  Web Inclination: {self.web_inclination}°")
        output.append("")
        
        output.append("NODES:")
        output.append(f"  Total Nodes: {self.node_id - 1}")
        output.append("")
        
        output.append("ELEMENTS:")
        output.append(f"  Total Elements: {self.element_id - 1}")
        output.append("")
        
        output.append("SUPPORTS:")
        supports = self.generate_supports()
        for support in supports:
            output.append(f"  {support}")
        output.append("")
        
        output.append("="*70)
        output.append("NEXT STEPS:")
        output.append("1. Import nodes and elements into Midas Civil")
        output.append("2. Define material properties")
        output.append("3. Apply loads (self-weight, live load, etc.)")
        output.append("4. Run analysis")
        output.append("="*70)
        
        return "\n".join(output)
    
    def generate(self):
        """Generate complete model"""
        print("Generating deck nodes...")
        self.generate_deck_nodes()
        
        print("Generating bottom slab nodes...")
        self.generate_bottom_nodes()
        
        print("Generating web nodes...")
        self.generate_web_nodes()
        
        print("Generating elements...")
        self.generate_elements()
        
        print(f"Total nodes created: {self.node_id - 1}")
        print(f"Total elements created: {self.element_id - 1}")
        
        return self.export_to_text()


if __name__ == "__main__":
    generator = BoxGirderGenerator()
    result = generator.generate()
    print(result)
    
    # Save to file
    with open("box_girder_model.txt", "w") as f:
        f.write(result)
    print("\nModel exported to: box_girder_model.txt")
