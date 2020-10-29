#!/usr/bin/env python

"""
Restore a CloudSQL backup to another CloudSQL Database.
"""

import datetime as dt
import json
from os import environ
from subprocess import run
from sys import exit as sys_exit


class Restorer:
    """
    Restore a CloudSQL backup to another CloudSQL Database.
    """

    def __init__(self,
                 project_id: str,
                 backup_instance: str,
                 restore_instance: str):

        self.backup_instance = backup_instance
        self.current_time = dt.datetime.now(dt.timezone.utc)
        self.project_id = project_id
        self.restore_instance = restore_instance

    @classmethod
    def from_environment(cls):
        """
        Gather necessary environmnet variables or raise error and exit.
        """

        try:
            project_id = environ['project_id']
            backup_instance = environ['backup_instance']
            restore_instance = environ['restore_instance']
        except KeyError as env_err:
            print(f'Missing environment variable(s): {env_err}')
            sys_exit(3)

        return cls(project_id, backup_instance, restore_instance)

    def get_recent_backup(self) -> str:
        """
        Get this most recent CloudSQL backup.
        """

        gcloud_cmd = ('/usr/local/bin/gcloud '
                      'sql backups list '
                      f'-i {self.backup_instance} '
                      f'--project {self.project_id} '
                      '--format=json')

        return max(json.loads(self._run_cmd(gcloud_cmd).stdout),
                   key=lambda backup: backup["endTime"])

    def restore_backup(self, backup_id: str):
        """
        Create a string from the arguments and run
        """

        gcloud_cmd = ('/usr/local/bin/gcloud '
                      'sql backups restore '
                      f'{backup_id} '
                      f'--restore-instance={self.restore_instance} '
                      f'--project {self.project_id} '
                      f'--backup-instance={self.backup_instance} '
                      '--async --quiet')

        return self._run_cmd(gcloud_cmd)

    @staticmethod
    def _run_cmd(cmd: str) -> object:
        """
        Given a string split and execute with subprocess.run.
        """

        return run(cmd.split(' '),
                   capture_output=True,
                   check=True,
                   text=True)

    def verify_backup(self, backup: dict) -> None:
        """
        Check that the returned CloudSQL has been completed and is successful.

        The gcloud command should return and endTime and a status.

        Datetime format from gloud command
        2019-12-13T02:48:49.121000+00:00
        """

        date_obj = dt.datetime.strptime(backup['endTime'],
                                        '%Y-%m-%dT%H:%M:%S.%f%z')

        assert (backup["status"].lower() == "successful"
                and date_obj < self.current_time)


if __name__ == '__main__':

    restorer = Restorer.from_environment()
    recent_backup = restorer.get_recent_backup()
    restorer.verify_backup(recent_backup)
    restorer.restore_backup(recent_backup['id'])
