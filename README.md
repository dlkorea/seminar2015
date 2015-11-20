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

