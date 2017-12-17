# -*- coding: utf-8 -*-

"""Main module."""

import os
import uuid
import shelve


class Task(object):
    """ The domain object """

    def __init__(self, title):
        self.id = uuid.uuid4()
        self.title = title

    def __str__(self, *args, **kwargs):
        """ Return a nice string for this object.

        >>> t = Task("test")
        >>> print(t)
        test
        """
        return self.title

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self.__dict__ == other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)



class CLI(object):
    """ The user interface """

    @staticmethod
    def handle_arguments(arguments):
        """ Triggers the domain logic depending on the CLI arguments.

        :param arguments: The CLI arguments dictionary created by 'docopt'.
        """
        mgmt = Manager()
        if arguments["create"]:
            t = mgmt.create(arguments["<title>"])
            print("created: %s | %s" % (t.id, t.title))
        elif arguments["list"]:
            tasks = mgmt.list_tasks()
            print("Current tasks:")
            if len(tasks) == 0:
                print("<empty>")
            else:
                for t in tasks:
                    print("* %s" % t.title)
        elif arguments["update"]:
            # id = arguments["<id>"]
            # new_values = arguments["<attr=value>"]
            print("TODO - implement me")



class Manager(object):
    """ The domain logic between user interface and persistence """

    def __init__(self):
        self.persistence = Persistence()

    def create(self, title):
        t = Task(title)
        self.persistence.save(t)
        return t

    def update(self, task):
        return self.persistence.update(task)

    def list_tasks(self):
        return self.persistence.list_tasks()


class Persistence(object):
    """ The persistence layer """

    FILE_NAME = "tasks.db"

    def update(self, task):
        """ Update the given task

        :param task: The task which should be updated.
        :return: True when updated. Otherwise False.
        :rtype: bool
        :raise NotImplementedError: Not yet done
        """
        raise NotImplementedError("TODO - implement me")

    def clear(self):
        """ Clears all entries in the persistence layer.

        This makes only sense in testing scenarios.
        """
        if os.path.exists(Persistence.FILE_NAME):
            os.remove(Persistence.FILE_NAME)

    def save(self, t):
        db = shelve.open(Persistence.FILE_NAME, writeback=True)
        db[str(t.id)] = t
        db.close()

    def list_tasks(self):
        db = shelve.open(Persistence.FILE_NAME, writeback=True)
        tasks = db.values()                 # works in py27 only
        # tasks = [t for t in db.values()]  # works in py27 + py34
        db.close()
        return tasks

