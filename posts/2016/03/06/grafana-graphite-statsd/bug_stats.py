#!/usr/bin/env python

from launchpadlib.launchpad import Launchpad

import os
import statsd


class BugStatsCollector(object):
    """Collect bug stats by Launchpad project name """

    LP_OPEN_STATUSES = ["New", "Incomplete", "Confirmed",
                        "Triaged", "In Progress"]

    LP_IMPORTANCES = ["Undecided", "Wishlist", "Low",
                      "Medium", "High", "Critical"]

    def __init__(self, project_name):
        self.project_name = project_name

        cachedir = os.path.expanduser("~/.launchpadlib/cache/")
        if not os.path.exists(cachedir):
            os.makedirs(cachedir, 0o700)
        launchpad = Launchpad.login_anonymously('bugstats',
                                                'production',
                                                cachedir)
        self.project = launchpad.projects[self.project_name]

    def get_open_by_importance(self):
        """Return the stats for open bugs, separated by importance.

        :rtype: list of 2-tuple key-value pairs
        """
        importance_stats = []
        for importance in BugStatsCollector.LP_IMPORTANCES:
            bug_tasks = self.project.searchTasks(
                status=BugStatsCollector.LP_OPEN_STATUSES,
                importance=importance,
                omit_duplicates=True)
            stats_key = self._get_valid_stat_key_name(importance)
            stats_value = self._count_bug_tasks(bug_tasks)
            stat =(stats_key, stats_value)
            importance_stats.append(stat)
        return importance_stats

    def _get_valid_stat_key_name(self, name):
        stat_key = name
        stat_key = stat_key.replace(" ", "").lower()
        stat_key = stat_key.replace("(", "-")
        stat_key = stat_key.replace(")", "")
        return stat_key

    def _count_bug_tasks(self, bug_tasks):
        return int(bug_tasks._wadl_resource.representation['total_size'])


def push_to_statsd(metric_name, bug_stats):
    """push bug statistics to statsd on this host machine

    :param metric_name: The name of the metric
    :param bug_stats: list of 2-tuple key-value pairs to push
    """
    print("metric name: " + metric_name)
    gauge = statsd.Gauge(metric_name)
    for bug_stat in bug_stats:
        print("%s:%s" % (bug_stat[0], bug_stat[1]))
        gauge.send(bug_stat[0], bug_stat[1])


if __name__ == '__main__':
    projects = ['nova', 'python-novaclient', 'cinder', 'neutron']
    for project_name in projects:
        collector = BugStatsCollector(project_name)
        metric_name = 'launchpad.bugs.%s.open-by-importance' % project_name
        bug_stats = collector.get_open_by_importance()
        push_to_statsd(metric_name, bug_stats)
