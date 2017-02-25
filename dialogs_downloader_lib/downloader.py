import codecs
import json
import os.path

COUNT_TO_REQUEST = 200

def download_dialog(helper, dialog_id, path, update = True):
	res = None
	changed = False
	oldCount = None
	if not (update and os.path.isfile(path)):
		changed = True
		res = helper.apiRequest("messages.getHistory", {
				'offset': 0,
				'count': COUNT_TO_REQUEST,
				'peer_id': dialog_id,
				'rev': 1
			})
		print("Need to download %d messages" % res['response']['count'])
		offset = COUNT_TO_REQUEST
		count = res['response']['count'] - COUNT_TO_REQUEST
		oldCount = 0
		while count > 0:
			newRes = helper.apiRequest("messages.getHistory", {
				'offset': offset,
				'count': COUNT_TO_REQUEST,
				'peer_id': dialog_id,
				'rev': 1
			})
			print("%d left" % count)
			offset += COUNT_TO_REQUEST
			count -= COUNT_TO_REQUEST
			res['response']['items'] += newRes['response']['items']
	else:
		f = codecs.open(path, 'r', "utf-8")
		res = json.load(f)
		last_msg_id = res['response']['items'][-1]['id'] if len(res['response']['items']) > 0 else 0
		oldCount = res['response']['count']
		newRes = helper.apiRequest("messages.getHistory", {
				'offset': -COUNT_TO_REQUEST,
				'count': COUNT_TO_REQUEST,
				'peer_id': dialog_id,
				'start_message_id': last_msg_id
			})
		newCount = newRes['response']['count']
		res['response']['count'] = newCount
		res['response']['in_read'] = newRes['response']['in_read']
		res['response']['out_read'] = newRes['response']['out_read']
		print("Need to download %d messages" % (newCount - oldCount))
		changed = newCount != oldCount
		offset = -COUNT_TO_REQUEST * 2
		while len(newRes['response']['items']) > 0:
			res['response']['items'] += newRes['response']['items'][::-1]
			newRes = helper.apiRequest("messages.getHistory", {
				'offset': offset,
				'count': COUNT_TO_REQUEST,
				'peer_id': dialog_id,
				'start_message_id': last_msg_id
			})
			offset -= COUNT_TO_REQUEST

	if changed:
		print("Writing json file")
		f = codecs.open(path, 'w', "utf-8")
		json.dump(res, f, ensure_ascii=False)
	return (oldCount, res)