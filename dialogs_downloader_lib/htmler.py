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

def getMsgBody(message):
	if message['body'] != "":
		return '<div class="msg_body">%s</div>' % message['body'] \
			.replace("<", "&lt") \
			.replace(">", "&gt") \
			.replace("\n", "<br/>") 
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
		f_template = open(TEMPLATE_FILE, "r")
		f_out = open(filename, "w", encoding="utf-8")
		for l in f_template:
			l = l.rstrip()
			if l.replace(" ", "") != "$body$":
				f_out.write(l + "\n")
			else:
				for message in messages:
					f_out.write(getMessage(message, True))