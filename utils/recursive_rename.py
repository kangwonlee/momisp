import os
import sys


def main(path, ext, new_char, prev_char=' '):
    # recursive loop
    for root, dirnames, filenames in os.walk(path):
        if 'ipynb_checkpoints' not in root:
            # files loop
            for old_name in filenames:
                if ext in os.path.splitext(old_name)[-1]:
                    # if undesirable char included
                    if prev_char in old_name:
                        new_name = old_name.replace(prev_char, new_char)
                        os.rename(os.path.join(root, old_name),
                                  os.path.join(root, new_name), )


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
