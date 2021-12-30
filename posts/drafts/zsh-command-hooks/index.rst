.. todo:: date, tags and title

.. post::
   :tags: template
   :title: zsh command hooks


Use zsh hooks for printing timestamps and duration:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   preexec() {
       echo "=== `date -Is` command start ===\n"
       CMD_EXEC_TS=`date +%s`
       # $2 resolves aliases
       echo "$ $1"
   }
   precmd() {
       if [[ ! -z "$CMD_EXEC_TS" ]]; then
           CMD_EXEC_D=$((`date +%s`-CMD_EXEC_TS))
           echo "\n=== `date -Is` (${CMD_EXEC_D}s) command end ==="
       fi
       unset CMD_EXEC_TS
   }

Example:

.. code-block:: bash
   :linenos:
   :emphasize-lines: 0

   $ sleep 2
   === 2021-10-15T10:08:20+00:00 command start ===

   $ sleep 2

   === 2021-10-15T10:08:23+00:00 (3s) command end ===
