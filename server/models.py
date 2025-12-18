from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        """
        Ensure that the author has a non-empty and unique name.
        """
        # Normalize input
        if not value or not value.strip():
            raise ValueError("Author must have a name")

        value = value.strip()

        existing_author = Author.query.filter(Author.name == value).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author name must be unique")

        return value
    
    @validates('phone_number')
    def validate_phone_number(self, key, value):
        """
        Ensure that the phone number consists of exactly ten digits.
        """
        if not value:
            raise ValueError("Phone number is required")

        # Allow only digits
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")

        # Must be exactly 10 digits
        if len(value) != 10:
            raise ValueError("Phone number must be exactly ten digits")

        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('category')
    def validate_category(self, key, value):
        """
        Ensure category is one of the allowed values.
        """
        if value is None:
            raise ValueError("Post must have a category")

        value = value.strip()

        allowed = {"Fiction", "Non-Fiction"}
        if value not in allowed:
            raise ValueError("Post category must be Fiction or Non-Fiction")

        return value

    @validates('title')
    def validate_title(self, key, value):
        """
        Ensure that each post has a non-empty, non-clickbait title.
        """
        if not value or not value.strip():
                raise ValueError("Post must have a title")

        value = value.strip()

        clickbait_starts = ("Why", "Top", "Guess")
        for word in clickbait_starts:
            if value.startswith(word):
                raise ValueError("Post title cannot be clickbait")

        return value

    @validates('content')
    def validate_content(self, key, value):
        """
        Ensure that content is at least 250 characters long.
        """
        if not value:
            raise ValueError("Post content is required")

        # Keep the original content, but enforce minimum length
        if len(value) < 250:
            raise ValueError("Post content must be at least 250 characters")
        
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        """
        Ensure that summary is no more than 250 characters long.
        """
        
        if value is None:
            return value

        if len(value) > 250:
            raise ValueError("Post summary must be 250 characters or fewer")

        return value

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
