#!/bin/env python3

from jinja2 import Environment, FileSystemLoader
import tarfile
import os
import sys
import pyinotify
import hashlib


SOSREPORT_ARCHIVE_DIR = '/sosreports'
SOSREPORT_EXTRACT_DIR = '/sosreports_extract'
PROMTAIL_CONFIG_DIR = '/promtail_configs'


"""
Assumptions:
    * All files in an archive are in a unique subdir that is named the same as the base archive file.
      i.e. abc123.tar.xv should have a subdir abc123 in the root of the archive with all the files in it.
      ^^ We should create a random subdir in the extract dir to drop the above assumption.
"""

class SOSEvent():
    SKIP_DIRS = ('proc', 'sys',)
    EXTRACT_BASE_DIR = SOSREPORT_EXTRACT_DIR
    PROMTAIL_CONFIG_BASE_DIR = PROMTAIL_CONFIG_DIR

    def __init__(self, archive_abs_path):
        self._archive_abs_path = os.path.normpath(archive_abs_path)
        self._extract_abs_path = None
        self._promtail_config_abs_path = None
        self._fingerprint = None
        # Starting useful directory
        self._root_abs_path = None
        self._tar_files_to_extract = []
        self._tar_files_total = 0
        self._tar_files_skipped = 0

    def _tar_files_perc(self, count):
        total_to_extract = len(self._tar_files_to_extract)
        return int((count / total_to_extract) * 100)

    def init(self):
        self._fingerprint = hashlib.md5(open(self._archive_abs_path, 'rb').read()).hexdigest()
        self._extract_abs_path = os.path.join(self.EXTRACT_BASE_DIR, self._fingerprint)
        self._promtail_config_abs_path = os.path.join(self.PROMTAIL_CONFIG_BASE_DIR, f'promtail_{self._fingerprint}.yml')

        try:
            os.mkdir(self._extract_abs_path)
        except FileExistsError:
            print(f"Failed to create dir because it exists {self._extract_abs_path}", file=sys.stderr)


        with tarfile.open(self._archive_abs_path) as tar:
            for member in tar.getmembers():
                p = os.path.normpath(member.name).split(os.sep)
                if len(p) == 1:
                    self._root_abs_path = os.path.join(self._extract_abs_path, p[0])
                if len(p) > 1 and p[1] in self.SKIP_DIRS:
                    prepend = 'SKIP '
                else:
                    self._tar_files_to_extract.append(member)

        if not self._root_abs_path:
            raise ValueError("Root abs path not found")

    def extract(self):
        print(f"Started extracting {self._archive_abs_path}")
        with tarfile.open(self._archive_abs_path) as tar:
            for count, member in enumerate(self._tar_files_to_extract):
                perc = self._tar_files_perc(count)
                p = os.path.normpath(member.name).split(os.sep)
                tar.extract(member=member, path=self._extract_abs_path)
                #print(f'Progress {perc}% {member.name}', file=sys.stderr)
                count += 1
            print("Extraction complete")

    def generate_promtail_config(self):
        environment = Environment(loader=FileSystemLoader("/app/"))
        template = environment.get_template("promtail_config.yml.j2")

        # TODO: read hostname from path/hostname
        template_vars = {
            'hostname': 'xxx',
            'sosreport_dir': f'{self._root_abs_path}'
        }

        content = template.render(
            **template_vars
        )
        # TODO: generate a randomish string for the promtail config filename
        # maybe from the hostname, maybe from the sosreport filename
        with open(self._promtail_config_abs_path, mode="w", encoding="utf-8") as message:
            message.write(content)

    def run(self):
        self.init()
        self.extract()
        self.generate_promtail_config()


class SOSDetect():
    @classmethod
    def run(cls, watch_dir=SOSREPORT_ARCHIVE_DIR):
        class EventHandler(pyinotify.ProcessEvent):
            def process_default(self, event):
                print(f"Callback called {event}")
                SOSEvent(event.pathname).run()

            def process_IN_CLOSE_WRITE(self, event):
                self.process_default(event)

        wm = pyinotify.WatchManager()
        notifier = pyinotify.Notifier(wm, EventHandler())
        mask = pyinotify.IN_CREATE # | pyinotify.IN_CLOSE_WRITE | pyinotify.ALL_EVENTS
        #wm.add_watch(watch_dir, pyinotify.IN_CLOSE_WRITE)
        wm.add_watch(watch_dir, mask)
        notifier.loop()



SOSDetect.run()
#do_extract_sosreport('sosreport-awx1-2023-08-10-namgxyy.tar.xz')
