import os
from stat import S_IREAD
import datetime

if __name__ == "__main__":
    start_time = datetime.datetime.now()

    all_files = os.walk('.')
    all_count = 0
    for root, dirs, files in all_files:
        all_count += len(files)
        for a_file in files:
            os.chmod(os.path.join(root, a_file), S_IREAD)

    time_in_sec = datetime.datetime.now() - start_time
    print("Processed {c} files in {t} seconds.".format(c=all_count,t=time_in_sec))
