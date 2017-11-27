#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from vk_api.acquirers import *
from vk_api.vk_items import *
from vk_api.helper import VKAPIHelper

import argparse
import time
import random
import json

SLEEP_MIN = 2
SLEEP_MAX = 4
TOKENFILE = "tokens.json"

def get_helper(token_id = None):
	tokenfile = json.loads(open(TOKENFILE).read())
	if token_id == None:
		token_id = tokenfile['default']
	return VKAPIHelper(tokenfile['tokens'][token_id])

def parseargs():
    parser = argparse.ArgumentParser(description="Ultimate autoliker tool for vk.com")
    parser.add_argument('target', metavar='target_id',
    	help='id of the page to like (only wall will be liked)', type=int, nargs='+')
    return parser.parse_args()


def likeAll(acquirers = []):
	print("Launched with " + str(len(acquirers)) + " acquirers")
	for acquirer in acquirers:
		print("Using acquirer " + str(acquirer))
		print("This one has " + str(acquirer.count()) + " posts")
		for post in acquirer.iterate():
			if not post.isLiked():
				print("Liking " + str(post.item_id))
				res = post.addLike()
				if "error" in res:
					raise Exception(res)
				time.sleep(random.randint(SLEEP_MIN, SLEEP_MAX))
			else:
				print(str(post.item_id) + " already liked, skipping...")

if __name__ == '__main__':
	args = parseargs()
	helper = get_helper()
	acquirers = []
	for target in args.target:
		acquirers.append(WallAcquirer(helper, str(target)))
	likeAll(acquirers)

