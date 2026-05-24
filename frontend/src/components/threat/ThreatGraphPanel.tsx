import { useMemo } from "react";
import * as d3 from "d3";
import { Background, Controls, ReactFlow, type Edge, type Node } from "@xyflow/react";
import "@xyflow/react/dist/style.css";

import type { ThreatGraph } from "../../types/threatIntel";

interface ThreatGraphPanelProps {
  graph: ThreatGraph;
}

export function ThreatGraphPanel({ graph }: ThreatGraphPanelProps) {
  const { nodes, edges } = useMemo(() => {
    const color = d3.scaleOrdinal<string>().domain(["entity", "tactic"]).range(["#22d3ee", "#f59e0b"]);
    const nodes: Node[] = graph.nodes.slice(0, 60).map((node, index) => ({
      id: node.id,
      position: { x: (index % 8) * 170, y: Math.floor(index / 8) * 110 },
      data: { label: node.label },
      style: {
        border: `1px solid ${color(node.type)}`,
        background: "rgba(15, 23, 42, 0.92)",
        color: "#e5f2ff",
        borderRadius: 8,
        fontSize: 12,
      },
    }));
    const edges: Edge[] = graph.edges.slice(0, 90).map((edge) => ({ id: edge.id, source: edge.source, target: edge.target, label: edge.label, animated: true }));
    return { nodes, edges };
  }, [graph]);

  return (
    <div className="h-[520px] overflow-hidden rounded-lg border border-cyan-400/20 bg-surface-950">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background color="#1e293b" />
        <Controls />
      </ReactFlow>
    </div>
  );
}
