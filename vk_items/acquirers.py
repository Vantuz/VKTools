from vk_items.items import WallPost

BLOCK_SIZE = 100

class WallAcquirer(object):
	def __init__(self, api_helper, owner_id):
		self.api_helper = api_helper
		self.owner_id = owner_id

	def __repr__(self):
		return "WallAcquirer(" + self.owner_id + ")"

	def count(self):
		return self.api_helper.apiRequest("wall.get", {
			"owner_id": self.owner_id,
			"count": 1,
			"extended": 1
			})['response']['count']

	def iterate(self):
		offset = 0
		posts_amount = 1
		while offset <= posts_amount:
			response = self.api_helper.apiRequest("wall.get", {
				"owner_id": self.owner_id,
				"count": BLOCK_SIZE,
				"offset": offset,
				"extended": 1
				})
			posts_amount = response['response']['count']
			posts = response['response']['items']
			for post in posts:
				yield WallPost(self.api_helper, post['owner_id'], post['id'], post['likes']['user_likes'])
			offset += BLOCK_SIZE


