<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>

# template 문법 관련
실 서비스를 만들때 대부분의 경우 하나의 메뉴는 하나의 레이 아웃을 공유합니다. 
이 때 매 템플릿마다 레이아웃 작업을 중복해서 할 필요 없이 하나의 레이아웃 파일을 만들어 두고 반복 사용할 수 있습니다.

레이 아웃 작업을 해둔 템플릿 파일이 index.html 이고 내용은 아래와 같다고 합시다.

```
<!DOCTYPE html>
<head>
  헤드 내용
</head>
<body>
  <div id="header">
    안녕하세요
  </div>
  <div id="main">
    {% block main %}
    {% endblock %}
  </div>
</body>
```

이때 id가 header인 div 영역의 내용은 사이트 전체 메뉴에서 공통으로 보이고, id가 main인 영역만 변경하려고 한다면, 다른 템플릿 파일을

```
{% extends index.html %}

{% block main %}
코딩~~~
{% endblock %}
```

과 같은 형태로 만들어 index.html에서 {% block main %}{% endblock %} 영역만 덮어씌워주면 됩니다.


# Bootstrap 
실서비스용 사이트를 만들 때 css 디자인을 일일이 하기란 쉽지 않습니다. 우리가 서버를 구축할 때 모든걸 직접 만들지 않고 flask 등을 이용하여 만들듯 프론트 작업에서는 보통 Bootstrap이라는 프레임워크를 많이 사용합니다. Bootstrap은 트위터 개발팀에서 만들어 시중에 무료 배포한 프론트 프레임워크인데요. 요즘 홈페이지에서 많이 쓰는 버튼 디자인, 팝업 메뉴 등등의 프론트 코딩을 미리 해두었기에 html 태그에 단순히 클래스를 추가하는 것만으로 쉽게 사용할 수 있다는 장점이 있습니다. 

버튼을 예를 들어 살펴봅시다. html에서 기본 제공하는 버튼은 실서비스에 사용하기에는 너무 투박합니다. Bootsrap에서는 몇가지 버튼 형태를 기본적으로 제공합니다. 사용하기 위해서는 앞서 말씀드렸듯이 클래스만 추가해주시면 됩니다. 아래의 예를 참고하세요.

기본 버튼
<button>글쓰기</button>
```
<button class="btn btn-lg btn-primary">글쓰기</button>
```
위 코드로 생성된 버튼
<button class="btn btn-lg btn-primary">글쓰기</button>

Bootstrap을 개발중인 사이트에 적용하기 위해서는 크게 두가지 방법이 있습니다. 하나는 Bootstrap을 개발중인 폴더에 직접 저장하여 불러오는 방법, 다른 하나는 Bootstrap에서 기본 제공하는 CDN 서버에서 불러오는 방법입니다. 홈페이지(http://bootstrapk.com)에 시작하기 메뉴를 살펴보시면 자세한 설명이 나와있는데요. 일단은 CDN 서버에서 불러오는 방법을 사용해봅시다.

```
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
</head>
<body>
  사이트 내용
</body>
</html>
```

레이아웃 작업을 해둔 템플릿 파일은 위와 같은 구조를 가집니다. 여기서 <head> 태그 내에 다음 내용을 삽입해주시면 부트스트랩을 사용할 준비는 끝납니다.

```
<!-- 합쳐지고 최소화된 최신 CSS -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css">

<!-- 부가적인 테마 -->
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap-theme.min.css">

<!-- 합쳐지고 최소화된 최신 자바스크립트 -->
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/js/bootstrap.min.js"></script>
```

(<!-- ㄴㅇㄹ --> 과 같은 형태는 html 내의 주석에 해당하므로 굳이 삽입하지 않으셔도 무방합니다.)

나머지 내용들은 Bootstrap 홈페이지(http://bootstrapk.com)에서 직접 공부해보세요. 기본적으로 html 태그에 class만 추가하는 방식이므로 조금만 익숙해지시면 큰 어려움 없이 사용하실 수 있을겁니다. 차후 시간 여유가 생긴다면 자주 쓰는 몇가지 기능들은 이곳에 정리해드리겠습니다.
