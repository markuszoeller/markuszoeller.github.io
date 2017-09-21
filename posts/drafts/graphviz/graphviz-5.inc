.. graphviz::
   :align: center
   :caption: This is a graph
   :graphviz_dot: neato

   digraph lifecycle {
      // graph [ranksep="0.05", nodesep="0.01"];
      edge [len="1.25"];
      node [color=lightblue, style=filled, shape=box, fixedsize=true, width=0.9];

      contribute -> source;
      source -> build;
      build -> deploy;
      deploy -> upgrade;
      upgrade -> operate;
      operate -> change;
      change -> source;
      operate -> remove;
   }