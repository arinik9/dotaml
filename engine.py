from k_nearest_neighbors.k_nearest_neighbors import D2KNearestNeighbors, my_distance, poly_weights_recommend, poly_weights_evaluate
#from logistic_regression.logistic_regression import D2LogisticRegression
from dota2py import api
import os

# Initialize DOTA2 Web API
key = os.environ.get('DOTABOT_API_KEY')
api.set_api_key(key)
heroes = api.get_heroes()['result']['heroes']

def get_hero_human_readable(hero_id):
    for hero in heroes:
        if hero['id'] == hero_id:
            return hero['localized_name']
    return 'Unknown hero: %d' % hero_id

def main():
    # Fill these out using hero IDs (see web API)

    #Example: match_id = 415285235
    #radiant = OD, lifestealer, venomancer, clockwerk, visage
    my_team = [76, 54]
    #dire = CM, razor, TA, wisp, puck
    their_team = [5, 15, 46, 91, 13]

    print 'My Team: %s' % [get_hero_human_readable(hero_id) for hero_id in my_team]
    print 'Their Team: %s' % [get_hero_human_readable(hero_id) for hero_id in their_team]
    print 'Recommend:'
    engine = Engine(D2KNearestNeighbors())
    #engine = Engine(D2LogisticRegression())
    recommendations = engine.recommend(my_team, their_team)
    print recommendations
    #print '\n'.join([str(element) for element in recommendations])

class Engine:
    def __init__(self, algorithm):
        self.algorithm = algorithm

    def get_candidates(self, my_team, their_team):
        '''Returns a list of hero IDs to consider for recommending.'''
        # TODO use web api result to make this more robust
        return [i for i in range(1, 109) if i not in my_team and i not in their_team and i not in [24, 104, 105, 108]]

    def recommend(self, my_team, their_team, human_readable=False):
        '''Returns a list of (hero, probablility of winning with hero added) recommended to complete my_team.'''
        assert len(my_team) <= 5
        assert len(their_team) <= 5

        hero_candidates = self.get_candidates(my_team, their_team)
        return self.algorithm.recommend(my_team, their_team, hero_candidates)

    def predict(self, dream_team, their_team):
        '''Returns the probability of the dream_team winning against their_team.'''
        return self.algorithm.predict(dream_team, their_team)

if __name__ == "__main__":
    main()