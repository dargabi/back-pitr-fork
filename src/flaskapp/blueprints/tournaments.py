from flask import Blueprint, request, abort
from models.user import User
from models.tournament_stats import Tournament_stats
from models.tournament import Tournament
from flaskapp.auth import login_required
from swagger_generator import generator
import business.tournaments as tournaments_business
from flask import jsonify

tournaments_bluerprint = Blueprint('tournaments', __name__)

# Get tournaments
@generator.query_parameters([{ 'name': 'active', 'type': 'String', 'description': 'Filter by active' }])
@generator.response(status_code=200, schema={ 'id': 10, 'start_date': '2020-01-01', 'end_date': '2020-01-01', 'name': 'Torneo de prueba', 'description': 'Torneo de prueba', 'server': 'EUW', 'team_size': 5 })
@tournaments_bluerprint.get('/tournaments')
def get_tournaments():
    # Get parameters
    active = request.args.get('active')
    
    # Check if active is valid
    valid_actives = ['true', 'false']
    if active != None and active not in valid_actives:
        abort(400, 'Invalid active parameter')
    
    if active != None:
        active = active == 'true'

    # Get tournaments
    tournaments = tournaments_business.get_tournaments_info(active)

    return jsonify(tournaments), 200


# Get tournament stats
@generator.query_parameters([{ 'name': 'player-id', 'type': 'Integer', 'description': 'Filter by player id' }, { 'name': 'sort-by', 'type': 'String', 'description': 'Sort by username, wins, losses, score, rank' }, { 'name': 'order-by', 'type': 'String', 'description': 'Order by asc or desc' }])
@generator.response(status_code=200, schema={ 'tournament_id': 10, 'wins': 0, 'losses': 0, 'wr': 0.0, 'score': 0, 'rank': 0, 'username': 'dargabi', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q', 'user_id': 1})
@tournaments_bluerprint.get('/tournament-stats/<int:tournament_id>')
def get_tournament_stats(tournament_id):
    # Get parameters
    player_id = request.args.get('player-id')
    sort_by = request.args.get('sort-by')
    order_by = request.args.get('order-by')

    # Check if tournament exists
    if tournament_id != None:
        if Tournament.query.filter_by(id=tournament_id).first() is None:
            abort(404, 'Tournament not found')
    
    # Check if player exists
    if player_id != None:
        if User.query.filter_by(id=player_id).first() is None:
            abort(404, 'User not found')
    
    # Get stats
    stats = tournaments_business.get_player_tournament_stats(tournament_id, player_id)

    # Check if sort_by and order_by are valid
    valid_sorts = ['username', 'wins', 'losses', 'score', 'rank']
    valid_orders = ['asc', 'desc']
    if sort_by != None and sort_by not in valid_sorts:
        abort(400, 'Invalid sort-by parameter')
    
    if order_by != None and order_by not in valid_orders:
        abort(400, 'Invalid order-by parameter')

    # Sort
    if sort_by != None and order_by != None:
        stats.sort(key=lambda x: x[sort_by], reverse=order_by == 'desc')

    return jsonify(stats), 200
    

