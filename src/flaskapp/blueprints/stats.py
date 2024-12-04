from flask import Blueprint, request, abort
from models.user import User
from models.user_stats import User_stats
from swagger_generator import generator
from flask import jsonify
import business.stats as st

stats_bluerprint = Blueprint('stats', __name__)

# Get user stats
@generator.query_parameters([{'name': 'user-id', 'type': 'Integer', 'description': 'Filter by user id'}, {'name': 'sort-by', 'type': 'String', 'description': 'Sort by username, wins, losses, wr, kills, deaths, assists, kda, score, rank'}, {'name': 'order-by', 'type': 'String', 'description': 'Order by asc or desc'}])
@generator.response(status_code=200, schema={'username': 'dargabi', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q', 'user_id':1, 'wins': 0, 'losses': 0, 'wr': 0.0, 'kills': 0, 'deaths': 0, 'assists': 0, 'kda': 0.0, 'score': 0, 'rank': 0, 'champions_played': ['yasuo'], 'role': 'jungle'})
@stats_bluerprint.get('/user-stats')
def get_user_stats():
    # Get parameters
    user_id = request.args.get('user-id')
    sort_by = request.args.get('sort-by')
    order_by = request.args.get('order-by')

    # Check if user exists
    if user_id != None:
        if User.query.filter_by(id=user_id).first() is None:
            abort(404, 'User not found')

    # Get stats
    stats = st.get_player_stats(user_id)

    # Check if sort_by and order_by are valid
    valid_sorts = ['username', 'wins', 'losses', 'wr', 'kills', 'deaths', 'assists', 'kda', 'score', 'rank']
    valid_orders = ['asc', 'desc']
    if sort_by != None and sort_by not in valid_sorts:
        abort(400, 'Invalid sort-by parameter')
    
    if order_by != None and order_by not in valid_orders:
        abort(400, 'Invalid order-by parameter')

    # Sort
    if sort_by != None and order_by != None:
        stats.sort(key=lambda x: x[sort_by], reverse=order_by == 'desc')

    return jsonify(stats), 200
