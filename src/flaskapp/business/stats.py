from models.user import User
from models.user_stats import User_stats
from models.roles_played import Roles_played
from models.champions_played import Champions_played
from models.tournament import Tournament
from models.tournament_stats import Tournament_stats
import json
import sys

sys.path.append('..')
from database import Base, db_session

def update_ranking():
    # Set rank to index of user in sorted list by score
    users_stats = User_stats.query.all()
    users_stats.sort(key=lambda x: x.score, reverse=True)
    for i in range(len(users_stats)):
        users_stats[i].rank = i + 1
    db_session.commit()


def get_player_stats(player_id = None):
    if player_id == None:
        stats = User_stats.query.all()
    else:
        stats = [User_stats.query.filter_by(user_id=player_id).first()]
    data = []
    for stat in stats:
        user_data = {}
        # From user
        user_data['username'] = stat.user_object.username
        user_data['puuid'] = stat.user_object.puuid
        user_data['user_id'] = stat.user_id

        # From user_stats
        user_data['wins'] = stat.wins
        user_data['losses'] = stat.losses
        if stat.wins + stat.losses == 0:
            user_data['wr'] = 0.0
        else:
            user_data['wr'] = stat.wins / (stat.wins + stat.losses)
        user_data['kills'] = stat.kills
        user_data['deaths'] = stat.deaths
        user_data['assists'] = stat.assists
        if stat.deaths == 0:
            user_data['kda'] = (stat.kills + stat.assists) / 1
        else:
            user_data['kda'] = (stat.kills + stat.assists) / stat.deaths
        user_data['score'] = stat.score
        user_data['rank'] = stat.rank

        # From champions_played
        champions_played = stat.user_object.champions_played
        if champions_played != None:
            champions_played.sort(key=lambda x: x.games, reverse=True)
            champions_played = champions_played[:5]
            user_data['champions_played'] = [x.champion for x in champions_played]

        # From roles_played
        roles_played = stat.user_object.roles_played
        if roles_played != None:
            if(len(roles_played) >= 1):
                roles_played.sort(key=lambda x: x.games, reverse=True)
                roles_played = roles_played[0]
                user_data['role'] = roles_played.role
            else:
                user_data['role'] = None


        data.append(user_data)
    return data


# Call this function when a game ends to update the stats of the players
def update_player_stats(user_id, tournament_id, won, kills, deaths, assists, tournament_score, champion, role):
    # Get user stats
    user_stats = User_stats.query.filter_by(user_id=user_id).first()

    # Update user stats
    if won:
        user_stats.wins += 1
    else:
        user_stats.losses += 1

    user_stats.kills += kills
    user_stats.deaths += deaths
    user_stats.assists += assists

    # Updaate tournament stats
    tournament_stats = Tournament_stats.query.filter_by(user_id=user_id, tournament_id=tournament_id).first()
    if tournament_stats == None:
        tournament_stats = Tournament_stats(user_id=user_id, tournament_id=tournament_id)
    if won:
        tournament_stats.wins += 1
    else:
        tournament_stats.losses += 1
    tournament_stats.score += tournament_score

    # Update champions played
    champion_played = Champions_played.query.filter_by(user_id=user_id, champion=champion).first()
    if champion_played == None:
        champion_played = Champions_played(user_id=user_id, champion=champion)
    champion_played.games += 1
    if won:
        champion_played.wins += 1
    else:
        champion_played.losses += 1
    champion_played.kills += kills
    champion_played.deaths += deaths
    champion_played.assists += assists

    # Update roles played
    role_played = Roles_played.query.filter_by(user_id=user_id, role=role).first()
    if role_played == None:
        role_played = Roles_played(user_id=user_id, role=role)
    role_played.games += 1
    if won:
        role_played.wins += 1
    else:
        role_played.losses += 1
    role_played.kills += kills
    role_played.deaths += deaths
    role_played.assists += assists

    # Save
    user_stats.save()
    champion_played.save()
    role_played.save()

    # Update ranking
    update_ranking()