<script setup lang="ts">
type GraphNode = {
  x: number
  y: number
  label: string
  size: number
}

const nodes: GraphNode[] = [
  { x: 50, y: 30, label: 'LSM', size: 8 },
  { x: 75, y: 55, label: 'Sentimento', size: 10 },
  { x: 30, y: 65, label: 'Comportamento', size: 9 },
  { x: 55, y: 80, label: 'Score', size: 14 },
]

const connections: [number, number][] = [
  [0, 3],
  [1, 3],
  [2, 3],
  [0, 1],
  [1, 2],
]
</script>

<template>
  <div class="graph">
    <svg viewBox="0 0 100 100" preserveAspectRatio="xMidYMid meet">
      <line
        v-for="([from, to], index) in connections"
        :key="`line-${index}`"
        :x1="nodes[from]?.x ?? 0"
        :y1="nodes[from]?.y ?? 0"
        :x2="nodes[to]?.x ?? 0"
        :y2="nodes[to]?.y ?? 0"
        class="graph__line"
      />

      <g v-for="(node, index) in nodes" :key="`node-${index}`">
        <circle
          :cx="node.x"
          :cy="node.y"
          :r="node.size / 2"
          :class="index === 3 ? 'graph__node graph__node--score' : 'graph__node'"
        />
        <text :x="node.x" :y="node.y + node.size / 2 + 6" text-anchor="middle" class="graph__label">
          {{ node.label }}
        </text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.graph {
  width: 100%;
  height: 12rem;
  display: grid;
  place-items: center;
}

.graph svg {
  width: 82%;
  height: 82%;
}

.graph__line {
  stroke: color-mix(in srgb, var(--color-tertiary) 28%, transparent);
  stroke-width: 0.7;
}

.graph__node {
  fill: #18b5a8;
  opacity: 0.92;
}

.graph__node--score {
  fill: #4dd5c7;
}

.graph__label {
  fill: color-mix(in srgb, var(--token-text) 48%, transparent);
  font-size: 3.2px;
}
</style>
