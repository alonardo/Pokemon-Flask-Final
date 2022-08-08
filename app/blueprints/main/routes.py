from calendar import c
from hashlib import new
from flask import render_template, request, redirect, url_for, flash
import requests
from flask_login import login_user, login_required, logout_user, current_user
from app.blueprints.auth.forms import EditProfileForm, LoginForm, RegisterForm
from . import bp as main
from .forms import PokemonForm
from ...models import Pokemon


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = PokemonForm()
    if request.method == 'POST':
        # poke_name = form.poke_name.name
        # print(poke_name)        
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string, form=form)
        
        data = response.json()
        poke_dict={
            "name": data['name'].title(),
            "ability":data['abilities'][0]["ability"]["name"].title(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"]
        }
        
        return render_template('pokemon.html.j2', pokemon=poke_dict)
        
    else:
        error = 'error'
        return render_template('pokemon.html.j2', poke=error)

@main.route('/catch_pokemon', methods=['GET', 'POST'])
@login_required
def catch_pokemon():
    form = PokemonForm()
    if request.method == 'POST':
        name = request.form.get('name')
        url = f'https://pokeapi.co/api/v2/pokemon/{name}/'
        response = requests.get(url)
        if not response.ok:
            error_string = "Invalid selection, try again."
            return render_template('pokemon.html.j2', error=error_string)
        
        data = response.json()
        poke_dict={
            "name": data['name'].lower(),
            "ability":data['abilities'][0]["ability"]["name"].lower(),
            "base_experience":data['base_experience'],
            "attack_base_stat": data['stats'][1]['base_stat'],
            "hp_base_stat":data['stats'][0]['base_stat'],
            "defense_stat":data['stats'][2]["base_stat"],
            "photo":data['sprites']['other']['home']["front_default"],
            "user_id": current_user.id
        }
        
        new_pokemon = Pokemon()
        new_pokemon.from_dict(poke_dict)
        new_pokemon.save_poke()

        poke2 = Pokemon.query.filter_by(name=name.lower()).first()
        if len(current_user.pokemon.all()) == 5:
            print('You already have 5 Pokemon. Release one before cathing more!')
            flash('You already have 5 Pokemon. Release one before cathing more!', 'warning')
            return render_template('search.html.j2', pokemon=poke_dict)
        else:
            current_user.pokemon.append(poke2)
            current_user.save()
            poke2.save_poke()
            flash(f'You caught {poke2.name.title()}!', 'success')
        
        return render_template('search.html.j2', pokemon=poke_dict)

    else:
        error = 'error'
        return render_template('search.html.j2', poke=error)

@main.route("/view_pokemon")
@login_required
def view_pokemon():
    
    if len(current_user.pokemon.all()) == 0:
        flash("You don't have any Pokemon!", "danger")
        error = 'error'
        return render_template('search.html.j2', poke=error)
    else:
        for poke in current_user.pokemon.all():
            print(poke.name.title())
            print(poke.ability)
            print(poke.photo)
        flash("Here's your Pokemon!", "success")
        return render_template('view_pokemon.html.j2', current_user=current_user)
    
@main.route("/release")
@login_required
def release():
    name = current_user.query.get('pokemon.id')
    if current_user.pokemon.delete(name):
        print('success')
    return render_template('release.html.j2')



# method sqlalchemy.orm.Query.delet
# https://docs.sqlalchemy.org/en/14/orm/query.html
