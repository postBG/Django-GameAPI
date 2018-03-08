# Django-GameAPI
Explore django-rest-framework

## Note
### HTTP PATCH
* patch method는 자원의 특정 필드들만 변경할 수 있게 해주는 method.
* 이 예제에서는 generics를 사용하기 때문에 해당 patch의 구현이 RetrieveUpdateDestroyAPIView에 구현되어 있다.
* 좀 더 정확하게는 mixins.UpdateModelMixin에 정의되어 있으면 update 메서드를 호출하므로써 작동된다.
