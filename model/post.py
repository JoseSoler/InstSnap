from datetime import timedelta


class Post:

    def __init__(self, _id, user_id, created_on, text, image_url, expires_in_hours):
        self._id = _id
        self.user_id = user_id
        self.created_on = created_on
        self.text = str(text)
        self.image_url = str(image_url)
        self.expires_in_hours = expires_in_hours

    def __str__(self):
        string = "Post created by: \t " + str(self.user_id) + "\n"
        string += "On: \t" + str(self.created_on) + "\n"
        string += "Content \t" + str(self.text) + "\n"
        string += "Image at: \t" + str(self.image_url) + "\n"
        string += "Expires in: \t" + str(self.expires_in_hours) + "\n"
        return string

    def to_dictionary(self):
        return {'_id': str(self._id),
                'user_id': self.user_id,
                'created_at': self.created_on,
                'expires_at': self.created_on + timedelta(hours=self.expires_in_hours),
                'ttl_in_hours': self.expires_in_hours,
                'text': self.text,
                'image_url': self.image_url}
