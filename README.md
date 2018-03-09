# Django-GameAPI
Explore django-rest-framework

## Note
### HTTP PATCH
* patch method는 자원의 특정 필드들만 변경할 수 있게 해주는 method.
* 이 예제에서는 generics를 사용하기 때문에 해당 patch의 구현이 RetrieveUpdateDestroyAPIView에 구현되어 있다.
* 좀 더 정확하게는 mixins.UpdateModelMixin에 정의되어 있으면 update 메서드를 호출하므로써 작동된다.

### Pagination
mixins를 사용하여 만들었다면 global 설정을 통해 pagination 기능을 추가할 수 있다.
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5
}
```
* pagination은 limit와 offset을 통해 조작할 수 있으며, DRF는 next와 previous라는 속성을 통해 다음/이전 페이지의 정보를 제공해준다.
* request: /games/?limit=5&offset=5