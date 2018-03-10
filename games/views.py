from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.reverse import reverse

from games.models import Game, GameCategory, Player, PlayerScore
from games.permissions import IsOwnerOrReadOnly
from games.serializers import GameSerializer, GameCategorySerializer, PlayerSerializer, PlayerScoreSerializer, \
    UserSerializer


class ApiRoot(generics.GenericAPIView):
    """
    This class is used for browsing APIs.
    """
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'players': reverse(PlayerList.name, request=request),
            'game-categories': reverse(GameCategoryList.name, request=request),
            'games': reverse(GameList.name, request=request),
            'scores': reverse(PlayerScoreList.name, request=request),
            'users': reverse(UserList.name, request=request),
        })


class GameCategoryList(generics.ListCreateAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-list'


class GameCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GameCategory.objects.all()
    serializer_class = GameCategorySerializer
    name = 'gamecategory-detail'


class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """
        This code is for setting owner field. You can pass extra fields of model using keyword parameters.
        
        This method is from mixins.CreateModelMixin.
        :param serializer: 
        :return: 
        """
        serializer.save(owner=self.request.user)


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    name = 'game-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-list'


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    name = 'player-detail'


class PlayerScoreList(generics.ListCreateAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-list'


class PlayerScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PlayerScore.objects.all()
    serializer_class = PlayerScoreSerializer
    name = 'playerscore-detail'


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'
