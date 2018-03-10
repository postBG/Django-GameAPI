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

### Authentication

#### Basic
DRF를 사용하면 Pagination과 같이 간단한 설정만으로 인증기능을 사용할 수 있음.
settings.py에 글로벌 설정을 할 수 있고, 각 view마다 추가적으로 인증체계를 오버라이드 할 수도 있다.

DRF는 아래의 3가지 인증 클래스를 기본으로 제공한다.
* BasicAuthentication: 사용자의 이름과 암호에 대한 HTTP 기본 인증을 제공. 실제로 서비스에서 사용할 경우에는 HTTPS에서만 사용 가능해야한다.
* SessionAuthentication: 인증을 위해 Django의 Session Framework와 함께 작동한다.
* TokenAuthentication: 토큰 기반 인증을 제공한다. request의 Authorization HTTP 헤더에 Token 필드에 user의 token값이 지정되어 있어야한다.

참고로 만약에 이 예제와 같이 2가지 이상의 인증 클래스를 설정한다면 첫번째로 지정된 인증 클래스는
아래의 두가지 property들의 값을 사용하게 된다.
* request.user: Django의 User 모델 인스턴스
* request.auth: 인증 토큰과 같이 인증에 사용되는 추가적인 정보들

#### User Defined Object Level Permission
새로운 Permission 객체를 생성할 때는 반드시 BasePermission을 상속받고 has_object_permission 메서드를
오버라이드해야한다.