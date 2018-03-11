from django_filters import NumberFilter, DateTimeFilter, AllValuesFilter
from django_filters import rest_framework as filters

from games.models import PlayerScore


class PlayerScoreFilter(filters.FilterSet):
    min_score = NumberFilter(name='score', lookup_expr='gte')
    max_score = NumberFilter(name='score', lookup_expr='lte')
    from_score_date = DateTimeFilter(name='score_date', lookup_expr='gte')
    to_score_date = DateTimeFilter(name='score_date', lookup_expr='lte')
    player_name = AllValuesFilter(name='player__name')
    game_name = AllValuesFilter(name='game__name')

    class Meta:
        model = PlayerScore
        fields = ('score', 'from_score_date', 'to_score_date', 'min_score', 'max_score', 'player_name', 'game_name')
