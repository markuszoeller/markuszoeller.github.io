.. graphviz::
   :align: center
   :caption: This is a graph
   :graphviz_dot: neato

   digraph lifecycle {
      graph [
         rankdir="BT"
      ]

      edge [
         len="1.25"
      ]

      node [
         color=lightblue,
         style=filled,
         shape=box,
         fixedsize=true,
         width=0.9
      ]

      contribute -> source;

      subgraph cluster_2 {
         source -> build;
         build -> release;
         release -> deploy;
         deploy -> upgrade;
         upgrade -> operate;
         operate -> change;
         change -> source;
      }

      deploy -> remove;
   }