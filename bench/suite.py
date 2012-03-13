from vbench.api import Benchmark, GitRepo
from datetime import datetime

import os

setup = """
from pymaging import Image
"""

stmt = ("Image.open_from_path('testimage.png')."
        "flip_left_right().save_to_path('benchimage.png')")

pymaging_benchmark = Benchmark(stmt, setup)

benchmarks = [pymaging_benchmark]

HOME = os.path.expanduser('~')
TMP_DIR = os.path.join(HOME, 'tmp/vb_pymaging')
DB_PATH = os.path.join(HOME, 'code/repos/pymaging/bench/benchmarks.db')
REPO_URL = '..'
REPO_PATH = '..'

START_DATE = datetime(2012, 2, 27)
repo = GitRepo(REPO_PATH)

from vbench.api import BenchmarkRunner

def run_process():
    runner = BenchmarkRunner(benchmarks, REPO_PATH, REPO_URL,
                             '', DB_PATH, TMP_DIR, '',
                             run_option='all', start_date=START_DATE,
                             module_dependencies=[])
    runner.run()

if __name__ == '__main__':
    run_process()
