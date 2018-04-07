# Django-GameAPI
Explore django-rest-framework
python version: 3.6.x

## 구현되어 있는 기능 목록
* 가능한 request들은 API root로 들어가서 보면 됨.
* limit & offset 기반의 pagination (max_limit=10)
* game의 owner만 game에 대한 write 권한을 주기
* 인증되지 않은 사용자는 시간당 최대 5개의 요청만 허용하기
* 인증된 사용자는 시간당 최대 20개의 요청만 허용하기
* 인증여부와 상관없이 게임 카테고리 관련 뷰에는 시간당 100건의 요청만 허용하기

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

### Throttling
글로벌 설정은 아래와 같이 한다.
```python
{
    # ...
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        # period can be one of sec, min, hour, day  
        'anon': '5/hour',
        'user': '20/hour',
        'game-categories': '30/hour'
    }
    # ...
}

```

DRF는 아래에서 서술할 3가지의 스로틀 클래스를 제공한다. 
이 클래스들은 모두 BaseThrottle과 SimpleRateThrottle 클래스의 서브클래스이다.

* AnonRateThrottle: 익명 사용자의 요청 속도를 제한. request의 IP 주소를 캐시 키로 사용.
* UserRateThrottle: 특정 사용자의 요청 속도를 제한. 인증된 사용자의 경우 ID가 캐시 키가 되며, 익명의 사용자의 경우 IP주소가 캐시 키가 된다.
* ScopedRateThrottle: trottle_scope 속성에 할당된 값으로 식별되는 API의 특정 부분에 대한 요청 비율을 제한. 주로 API의 특정 부분에 대한 접근을 다른 비율로 제한할 경우(즉, 다른 스로틀 설정을 override할 때)에 유용.

각 View들은 자신의 본문을 실행하기 전 Throttle 정책에 대한 검토를 먼저 시행한다. 
만일 Throttle 될 경우, Throttled exception이 발생한다.

### Filter
django-filter를 설치해주면, DRF는 filtering도 간단하다.
기본으로 사용할 글로벌 설정은 다음과 같이 해주면 된다.
```python
{
    # ...
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBacked',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ),
    # ...
}
```

우리가 이 예제에서 사용할 Filter에 대해 간단히 소개하자면 다음과 같다.
* DjangoFilterBacked: 필드 필터링 기능을 제공. 필터링할 수 있는 필드 세트를 지정하거나, 사용자가 정의한 FilterSet을 통해 뷰와 연결할 수 있다.
* SearchFilter: 단일 쿼리 매개 변수 기반 검색 기능을 제공하며 장고 admin의 검색 함수에 기반을 둔다.
검색에 포함할 필드를 지정할 수 있고, 클라이언트는 단일 쿼리로 이 필드를 섬색하는 쿼리를 만들어 항목을 필터링 할 수 있다.
요청에서 단일 쿼리로 여러 필드를 검색할 경우 유용하다.
* OrderingFilter: 검색 결과를 정렬하는 방법을 제어.

참고로, 제너릭 뷰의 filter_backends 속성에 위의 필터를 지정하면 클래스마다 filter를 다르게 적용할 수도 있다.

### UnitTest
```bash
python manage.py test -v 2
converage report -m
coverage html
```
