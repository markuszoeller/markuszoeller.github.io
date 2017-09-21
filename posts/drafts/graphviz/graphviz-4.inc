.. graphviz::
   :align: center
   :caption: This is a graph
   :graphviz_dot: neato

   digraph lifecycle {
      overlap=false;
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