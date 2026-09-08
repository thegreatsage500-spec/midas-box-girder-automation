#!/usr/bin/env python3
"""Export to Midas Civil MCT format"""
import struct

def export_mct(nodes, elements, filename="bridge.mct"):
    """Export to Midas binary format (simplified)"""
    with open(filename, 'wb') as f:
        f.write(b'MIDAS')
        f.write(struct.pack('I', len(nodes)))
        f.write(struct.pack('I', len(elements)))
        
        for node_id, x, y, z in nodes:
            f.write(struct.pack('I', node_id))
            f.write(struct.pack('fff', x, y, z))
        
        for elem_id, n1, n2, n3, n4 in elements:
            f.write(struct.pack('I', elem_id))
            f.write(struct.pack('IIII', n1, n2, n3, n4))
    
    print(f"Exported to {filename}")
