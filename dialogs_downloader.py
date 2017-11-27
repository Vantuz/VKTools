from vk_api.helper import VKAPIHelper
from dialogs_downloader_lib.downloader import download_dialog
from dialogs_downloader_lib.htmler import make_html

import json
import os
import os.path

TOKENFILE = "tokens.json"
SETTINGS_FILE = "dialogs_downloader_lib/settings.json"
JSONFILES_DIR = "dialogs_downloader_files/json"
HTMLFILES_DIR = "dialogs_downloader_files/html"

MESSAGES_IN_ONE_HTML_FILE = 5000

tokenfile = json.loads(open(TOKENFILE).read())
settings = json.loads(open(SETTINGS_FILE).read())

for group in settings['dialogs_to_download']:
	helper = VKAPIHelper(tokenfile['tokens'][group['token']])
	print("Updating %s's dialogs" % group['token'])
	for dialog in group['dialogs']:
		print('Updating dialog "%s"' % dialog['name'])
		json_dir = "%s/%s" % (JSONFILES_DIR, group['token'])
		json_file = "%s/%s/%s_%s.json" % (JSONFILES_DIR, group['token'], group['token'], dialog['name'])
		html_dir = "%s/%s/%s_%s" % (HTMLFILES_DIR, group['token'], group['token'], dialog['name'])
		no_html_files = False
		if not os.path.exists(json_dir):
			os.makedirs(json_dir)
		if not os.path.exists(html_dir):
			os.makedirs(html_dir)
			no_html_files = True
		(oldCount, res) = download_dialog(helper, dialog['id'], json_file)
		messages = res['response']['items']
		if oldCount != len(messages) or no_html_files:
			cnt = 1
			for i in range(0, len(messages), MESSAGES_IN_ONE_HTML_FILE):
				html_file = "%s/%s_%s-%d.html" % (html_dir, group['token'], dialog['name'], cnt)
				force_rewrite = oldCount - i <= MESSAGES_IN_ONE_HTML_FILE
				make_html(html_file, messages[i : i + MESSAGES_IN_ONE_HTML_FILE], force_rewrite)
				cnt += 1