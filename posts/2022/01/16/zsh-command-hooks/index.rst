
.. post:: January 16, 2022
   :tags: shell, zsh
   :category: operations
   :title: Command Hooks with the zsh Shell



================================
Command Hooks with the zsh Shell
================================

This post shows a small example how command hooks of the *zsh* shell can be used to print
timestamps before and after a command execution. This can be helpful in postmortems of
operations when it can be important to know exactly when you've seen a specific output or how
long a command took.



.. contents::
    :local:
    :backlinks: top



.. list-table:: Change history:
   :widths: 1 5
   :header-rows: 1

   * - Date
     - Change description
   * - 2022-01-16
     - The first release



Example
=======

.. asciinema:: zsh_hook_3768E4.json
   :poster: npt:0:05


Note the two lines which contain ``command start`` and ``command end`` which surround the command
execution and its output. For postmortems, I copy and paste the whole block into whatever
document we use to collect the details.


Implementation
==============

When you add the code below to the ``~/.zshrc`` and call ``source ~/.zshrc``
you get what you've seen before.

.. code-block:: zsh
   :linenos:
   :emphasize-lines: 0

   preexec() {
       echo "=== `date -Is --utc` command start ===\n"
       CMD_EXEC_TS=`date +%s`
       # $2 resolves aliases
       echo "$ $1"
   }

   precmd() {
       if [[ ! -z "$CMD_EXEC_TS" ]]; then
           CMD_EXEC_D=$((`date +%s`-CMD_EXEC_TS))
           echo "\n=== `date -Is --utc` (${CMD_EXEC_D}s) command end ==="
       fi
       unset CMD_EXEC_TS
   }

The *zsh* shell makes this possible by offering these command hooks:

* ``preexec``: Gets called **before** your command gets executed
* ``precmd``: Gets called **before** the prompt for the next command gets shown which looks like
  it's happening right after your command gets executed.

The rest of the code in short:

* ``date -Is --utc``: Show the date in ISO 8601 format, with seconds, for UTC-0. Using UTC-0
  makes it easier to compare output from different members of your global team.
* ``CMD_EXEC_TS=`date +%s```: Save the date in seconds in a variable
* ``CMD_EXEC_D=$((`date +%s`-CMD_EXEC_TS))``: Calculate the duration of the command in seconds

You can adjust this to whatever you need though.


Feedback
========

Feedback and questions with
`Github Discussions <https://github.com/markuszoeller/markuszoeller.github.io/discussions/46>`_
