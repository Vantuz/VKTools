class WallPost(object):
	def __init__(self, api_helper, owner_id, item_id, user_likes):
		self.api_helper = api_helper
		self.owner_id = owner_id
		self.item_id = item_id
		self.user_likes = user_likes

	def isLiked(self):
		return self.user_likes == 1

	def addLike(self):
		return self.api_helper.apiRequest("likes.add", {
			"type": "post",
			"owner_id": self.owner_id,
			"item_id": self.item_id
			})