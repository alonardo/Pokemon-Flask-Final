from enum import unique
from app import db, login
from flask_login import UserMixin # Only for user model
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash

user_poke = db.Table("user_poke",
    db.Column("pokemon_id", db.Integer, db.ForeignKey("pokemon.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True, index=True)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    icon = db.Column(db.Integer)
    pokemon = db.relationship(
        'Pokemon', 
        secondary=user_poke,  
        backref='user_poke',
        lazy='dynamic',
        )

    # pokemon = db.Column(db.Integer, db.ForeignKey('pokemon.id'))

    # This should return a unique id string
    def __repr__(self):
        return f'<User: {self.email}> | {self.id}'
    
    # For humans
    def __str__(self):
        return f'<User: {self.email}> | {self.first_name} {self.last_name}>'
    
    # Salt & hases our password to protect it
    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    # Compare user password to password provided in login
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.icon= data['icon']
    
    def get_icon(self):
        return f'https://avatars.dicebear.com/api/personas/{self.icon}.svg'

    def catch_pokemon(self, poke_dict):
        self.name = poke_dict['name']
        self.ability = poke_dict['ability']
        self.base_experience = poke_dict['base_experience']
        self.attack_base_stat = poke_dict['attack_base_stat']
        self.hp_base_stat = poke_dict['hp_base_stat']
        self.defense_stat = poke_dict['defense_stat']

    def view_pokemon(self):
        self_pokemon = self.pokemon
        collected = Pokemon.query.join(user_poke, (Pokemon.user_id == user_poke.c.user_id)).filter(user_poke.c.poke_id == self.id)
        user_pokemon = collected.union(self_pokemon).order_by(Pokemon.name)
        print(user_pokemon)
        return user_pokemon     

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Pokemon(db.Model):
    __tablename__ = 'pokemon'

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ability = db.Column(db.String)
    base_experience = db.Column(db.String)
    attack_base_stat = db.Column(db.String)
    hp_base_stat = db.Column(db.String)
    defense_stat = db.Column(db.String)
    photo = db.Column(db.String)

    def __repr__(self):
        return f'<Pokemon: {self.name}> | Id: {self.id}'

    def from_dict(self, poke_dict):
        self.name = poke_dict['name']
        self.ability = poke_dict['ability']
        self.base_experience = poke_dict['base_experience']
        self.attack_base_stat = poke_dict['attack_base_stat']
        self.hp_base_stat = poke_dict['hp_base_stat']
        self.defense_stat = poke_dict['defense_stat']
        self.photo = poke_dict['photo']  

    def save_poke(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_pokemon(self):
        db.session.delete(self)
        db.session.commit()
    
   
