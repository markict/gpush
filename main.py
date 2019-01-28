#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'''
this script is used to push my notes to github
'''

import os
import argparse
import time
import asyncio

HOME_DIR = os.environ['HOME']
DOCS_DIR = os.path.join(HOME_DIR, 'Documents')
Notes_DIR_NAME = 'Notes'

class GPush(object):

    def __init__(self):
        self.docs_dir = DOCS_DIR
        self.notes_dir_list = []
        self._load_notes_dir()

    def _load_notes_dir(self):

        dir_and_files = [os.path.join(self.docs_dir, n) for n in os.listdir(self.docs_dir)]
        main_dirs = filter(os.path.isdir, dir_and_files)
        #convert <filter object> to <list object>
        main_dirs = list(main_dirs)



        for d in main_dirs:
            if os.path.exists(os.path.join(d, Notes_DIR_NAME)):
                self.notes_dir_list.append(os.path.join(d, Notes_DIR_NAME))

        return len(self.notes_dir_list)

    def convert_path(self, input_path):
        '''
        convert input path to absolute path
        :param input_path: relative path or absolute path
        :return: the absolute path
        '''
        p = os.path.abspath(input_path)
        if os.path.exists(p):
            return p
        else:
            print(f"The path <{input_path}> is invalid!")
            return False




    async def push(self, target_dir, comment):
        target_dir = self.convert_path(target_dir)
        #determine if the dir contains .git
        if not os.path.exists(os.path.join(target_dir, '.git')):
            print(f'Directory: < {target_dir} > is not a git Dir!')
            return False
        try:
            print(f'\n \nDirectory----> {target_dir}')
            os.chdir(target_dir)

            print(f'git adding...')
            os.system('git add -A')

            print(f'git commiting...   Comment: <{comment}>')
            os.system(f'git commit -m "{comment}"')

            print(f'git pushing...')
            await os.system('git push origin master')
            return True

        except Exception as e:
            print(e)

    def push_all(self, comment):
        task_list = []
        for target_dir in self.notes_dir_list:
            coroutine = self.push(target_dir, comment)
            task = asyncio.ensure_future(coroutine)
            task_list.append(task)
        print(f"tasks status is {task_list}")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task_list))
        print(f"tasks status is {task_list}")
        loop.close()
        return len(self.notes_dir_list)


def main():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Push all notes to github', action='store_true')
    parser.add_argument('-d', '--dir', help='The target Dir you want to push', default='.')
    parser.add_argument('comment', help='The git commit comments', nargs='?', default=f'Commit at {current_time}')
    args = parser.parse_args()



    gpush = GPush()

    if args.all:
        gpush.push_all(args.comment)
    else:
        gpush.push(args.dir,args.comment)


if __name__ == '__main__':
    main()

