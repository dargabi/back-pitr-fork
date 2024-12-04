from models.user import User
from models.tournament import Tournament
from models.tournament_stats import Tournament_stats
import sys

sys.path.append('..')
from database import Base, db_session

def get_tournaments_info(is_active = None):
    tournaments = Tournament.query.all()
    data = []
    for tournament in tournaments:
        if is_active != None and tournament.is_active() != is_active:
            print('continue')
            continue

        tournament_data = {}
        tournament_data['id'] = tournament.id
        tournament_data['start_date'] = tournament.start_date
        tournament_data['end_date'] = tournament.end_date
        tournament_data['name'] = tournament.name
        tournament_data['description'] = tournament.description
        tournament_data['server'] = tournament.server
        tournament_data['team_size'] = tournament.team_size
        data.append(tournament_data)
    return data


def get_player_tournament_stats(tournament_id = None, player_id = None):
    data = []
    
    # Filter by tournament only
    if player_id == None and tournament_id != None:
        tournament_stats = Tournament_stats.query.filter_by(tournament_id=tournament_id).all()
    #Filter by player only
    elif player_id != None and tournament_id == None:
        tournament_stats = Tournament_stats.query.filter_by(user_id=player_id).all()
    # Filter by both
    elif player_id != None and tournament_id != None:
        tournament_stats = [Tournament_stats.query.filter_by(tournament_id=tournament_id, user_id=player_id).first()]
    # No filter
    else:
        tournament_stats = Tournament_stats.query.all()

    for tournament_stat in tournament_stats:
        tournament_stat_data = {}
        # From tournament_stats
        tournament_stat_data['tournament_id'] = tournament_stat.tournament_id
        tournament_stat_data['wins'] = tournament_stat.wins
        tournament_stat_data['losses'] = tournament_stat.losses
        if tournament_stat.wins + tournament_stat.losses == 0:
            tournament_stat_data['wr'] = 0.0
        else:
            tournament_stat_data['wr'] = tournament_stat.wins / (tournament_stat.wins + tournament_stat.losses)
        tournament_stat_data['score'] = tournament_stat.score
        tournament_stat_data['rank'] = tournament_stat.rank

        # From user
        user = tournament_stat.user_object
        tournament_stat_data['username'] = user.username
        tournament_stat_data['user_id'] = tournament_stat.user_id
        tournament_stat_data['puuid'] = user.puuid

        data.append(tournament_stat_data)
        
    return data