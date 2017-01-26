from vk_api.helper import VKAPIHelper

import os.path
import time

TEMPLATE_FILE = "dialogs_downloader_lib/template.html"

users_map = {
	0: {
		"id": 0,
		"first_name": "Unknown",
		"last_name": "User",
		"photo_100": "https://vk.com/images/deactivated_100.png"
	}
}

emojiTable = ["D83DDE0A", "D83DDE03", "D83DDE09", "D83DDE06", "D83DDE1C", "D83DDE0B", "D83DDE0D", "D83DDE0E", "D83DDE12",
"D83DDE0F", "D83DDE14", "D83DDE22", "D83DDE2D", "D83DDE29", "D83DDE28", "D83DDE10", "D83DDE0C", "D83DDE20", "D83DDE21",
"D83DDE07", "D83DDE30", "D83DDE32", "D83DDE33", "D83DDE37", "D83DDE1A", "D83DDE08", "2764", "D83DDC4D", "D83DDC4E",
"261D", "270C", "D83DDC4C","26BD", "26C5", "D83CDF1F", "D83CDF4C", "D83CDF7A", "D83CDF7B", "D83CDF39", "D83CDF45",
"D83CDF52", "D83CDF81", "D83CDF82", "D83CDF84", "D83CDFC1", "D83CDFC6", "D83DDC0E", "D83DDC0F", "D83DDC1C", "D83DDC2B",
"D83DDC2E", "D83DDC03", "D83DDC3B", "D83DDC3C", "D83DDC05", "D83DDC13", "D83DDC18", "D83DDC94", "D83DDCAD", "D83DDC36",
"D83DDC31", "D83DDC37", "D83DDC11", "23F3", "26BE", "26C4", "2600", "D83CDF3A", "D83CDF3B", "D83CDF3C",
"D83CDF3D", "D83CDF4A", "D83CDF4B", "D83CDF4D", "D83CDF4E", "D83CDF4F", "D83CDF6D", "D83CDF37", "D83CDF38", "D83CDF46",
"D83CDF49", "D83CDF50", "D83CDF51", "D83CDF53", "D83CDF54", "D83CDF55", "D83CDF56", "D83CDF57", "D83CDF69", "D83CDF83",
"D83CDFAA", "D83CDFB1", "D83CDFB2", "D83CDFB7", "D83CDFB8", "D83CDFBE", "D83CDFC0", "D83CDFE6", "D83DDC00", "D83DDC0C",
"D83DDC1B", "D83DDC1D", "D83DDC1F", "D83DDC2A", "D83DDC2C", "D83DDC2D", "D83DDC3A", "D83DDC3D", "D83DDC2F", "D83DDC5C",
"D83DDC7B", "D83DDC14", "D83DDC23", "D83DDC24", "D83DDC40", "D83DDC42", "D83DDC43", "D83DDC46", "D83DDC47", "D83DDC48",
"D83DDC51", "D83DDC60", "D83DDCA1", "D83DDCA3", "D83DDCAA", "D83DDCAC", "D83DDD14", "D83DDD25"]

helper = VKAPIHelper()

def getUserInfo(user_id):
	if user_id < 0:
		user_id = 0
	if not user_id in users_map:
		effective_id = user_id
		users_map[user_id] = helper.apiRequest("users.get", {
			"user_ids": str(effective_id),
			"fields": 'photo_100'
		})['response'][0]
	return users_map[user_id]

def replaceEmoji(symbol):
	symbol_hex_str = hex(ord(symbol))[2::].upper()
	if symbol_hex_str in emojiTable:
		return '<img src="http://vk.com/images/emoji/%s.png" alt="%s" />' % (symbol_hex_str, symbol)
	else:
		return symbol

def getMsgBody(message):
	if message['body'] != "":
		msg = message['body']
		msg = '<div class="msg_body">%s</div>' % msg \
			.replace("<", "&lt") \
			.replace(">", "&gt") \
			.replace("\n", "<br/>") 
		if 'emoji' in message and message['emoji'] == 1:
			msg = "".join(map(replaceEmoji, msg))
		return msg
	else:
		return ""

def getForward(message):
	ret_str = ""
	if "fwd_messages" in message:
		ret_str = ""

		ret_str += '<div class="att_head"><div class="att_ico att_fwd"></div> Forwarded messages: </div><div class="fwd">'
		for i in message['fwd_messages']:
			ret_str += getMessage(i, False)
		ret_str += "</div>"

	return ret_str

def getAttachments(message):
	ret_str = ""
	if "attachments" in message:
		ret_str += '<div class="attacments"><b>Attachments:</b></div>'
		for i in message['attachments']:
			ret_str += getAttachment(i)
		return ret_str
	return ret_str

def getAttachment(attach):
	ret_str = ""
	if attach['type'] == "photo":
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_photo"></div>'
		photo_name = "photo" + str(attach['photo']['owner_id']) + "_" + str(attach['photo']['id'])
		ret_str += '<a target="_blank" href="%s">%s</a>' % (getAttachmentPhotoUrl(attach), photo_name)
		ret_str += '</div>'
		return ret_str
	elif attach['type'] == "doc":
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_doc"></div>'
		ret_str += '<a target="_blank" href="%s">%s</a>' % (attach['doc']['url'], attach['doc']['title'])
		ret_str += '</div>'
	elif attach['type'] == "audio":
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_audio"></div>'
		audio_name = attach['audio']['artist'] + " — " + attach['audio']['title']
		if attach['audio']['url'] != "":
			ret_str += '<a target="_blank" href="%s">%s</a>' % (attach['audio']['url'], audio_name)
		else:
			ret_str += audio_name
		ret_str += '</div>'
	elif attach['type'] == "video":
		video_url = "https://vk.com/video%s_%s" % (attach['video']['owner_id'], attach['video']['id'])
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_video"></div>'
		ret_str += '<a target="_blank" href="%s">%s</a>' % (video_url, attach['video']['title'])
		ret_str += '</div>'
	elif attach['type'] == "wall":
		post_id = attach['wall']['id']
		owner_id = attach['wall']['from_id']
		name = "wall%s_%s" % (owner_id, post_id)
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_wall"></div>'
		ret_str += '<a target="_blank" href="http://vk.com/%s">%s</a>' % (name, name)
		ret_str += '</div>'
	elif attach['type'] == "link":
		ret_str += '<div class="attacment">'
		ret_str += '<div class="att_ico att_link"></div>'
		ret_str += '<a target="_blank" href="%s">%s</a>' % (attach['link']['url'], attach['link']['url'])
		ret_str += '</div>'
	elif attach['type'] == "sticker":
		ret_str += '<img src="%s">' % attach['sticker']['photo_128']
	return ret_str

def getAttachmentPhotoUrl(attach):
	photo_resolutions = [2560, 1280, 807, 604, 130, 75]
	for i in photo_resolutions:
		if "photo_" + str(i) in attach['photo']:
			return attach['photo']['photo_' + str(i)]

def getMessage(message, isNotFwd):
	user_info = None
	if isNotFwd:
		user_info = getUserInfo(message['from_id'])
	else:
		user_info = getUserInfo(message['user_id'])
	name = user_info['first_name'] + " " + user_info['last_name']

	msg_str = ""
	if isNotFwd:
		msg_str += '<div id="msg%s" class="msg_item">' % str(message['id'])
	else:
		msg_str += '<div class="msg_item">'
	msg_str += '<div class="upic"><img src="%s" alt="[photo_100]"/></div>' % user_info['photo_100']
	msg_str += '<div class="from">'
	msg_str += '<a href="https://vk.com/id%s" target="_blank"><b>%s</b></a> ' % (user_info['id'], name)
	if isNotFwd:
		msg_str += '<a href="#msg%s">%s</a>' % (message['id'], time.ctime(message['date']))
	else:
		msg_str += time.ctime(message['date'])
	msg_str += '</div>'
	msg_str += getMsgBody(message)
	msg_str += getForward(message)
	msg_str += getAttachments(message)
	msg_str += '</div>'
	msg_str += '<br clear="all"/>'

	return msg_str

def make_html(filename, messages, rewrite = False):
	if rewrite or (not os.path.isfile(filename)):
		print("Writing html file")
		f_template = open(TEMPLATE_FILE, "r")
		f_out = open(filename, "w", encoding="utf-8")
		for l in f_template:
			l = l.rstrip()
			if l.replace(" ", "") != "$body$":
				f_out.write(l + "\n")
			else:
				for message in messages:
					f_out.write(getMessage(message, True))
		f_template.close()
		f_out.close()