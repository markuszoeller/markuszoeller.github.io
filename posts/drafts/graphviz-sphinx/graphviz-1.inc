.. graphviz::
   :align: center
   :caption: This is a graph

   digraph lifecycle {
      contribute -> source;
      source -> build;
      build -> deploy;
      deploy -> upgrade;
      upgrade -> operate;
      operate -> change;
      change -> source;
      operate -> remove;
   }