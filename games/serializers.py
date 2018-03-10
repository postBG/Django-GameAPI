from django.contrib.auth.models import User
from rest_framework import serializers
from games.models import Game, GameCategory, PlayerScore, Player


class GameSerializer(serializers.HyperlinkedModelSerializer):
    """
    slug_field is set to name which means related GameCategory's name will be rendered.
    queryset is used to search related game_category object.
    
    We want to print just username of owner.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    game_category = serializers.SlugRelatedField(queryset=GameCategory.objects.all(), slug_field='name')

    class Meta:
        model = Game
        depth = 4
        fields = ('url', 'owner', 'game_category', 'name', 'release_date', 'played')


class GameCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    GameCategory don't know about Game. So we should explicitly include games.
    """
    games = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='game-detail')

    class Meta:
        model = GameCategory
        fields = ('url', 'pk', 'name', 'games')


class ScoreSerializer(serializers.HyperlinkedModelSerializer):
    """
    game field is set to GameSerializer object. It will be rendered by PlayScore object's game value.
    and we did not include player field because we don't want to serialize information of player.
    """
    game = GameSerializer()

    class Meta:
        model = PlayerScore
        fields = ('url', 'pk', 'score', 'score_date', 'game')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """
    scores field is set to ScoreSerializer. 
    When we try to render Player, Player object will use 'scores (declared by related_name in PlayerScore Model)' to 
    find and render scores.
    
    gender_description's source keyword variable is set to 'get_gender_display'. This 'get + gender + display' will make 
    serializer render not GENDER_CHOICE's char but description string.
    """
    scores = ScoreSerializer(many=True, read_only=True)
    gender = serializers.ChoiceField(choices=Player.GENDER_CHOICES)
    gender_description = serializers.CharField(source='get_gender_display', read_only=True)

    class Meta:
        model = Player
        fields = ('url', 'name', 'gender', 'gender_description', 'scores')


class PlayerScoreSerializer(serializers.ModelSerializer):
    player = serializers.SlugRelatedField(queryset=Player.objects.all(), slug_field='name')
    game = serializers.SlugRelatedField(queryset=Game.objects.all(), slug_field='name')

    class Meta:
        model = PlayerScore
        fields = ('url', 'pk', 'score', 'score_date', 'player', 'game')


class UserGameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    games = GameSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('url', 'pk', 'username', 'games')
