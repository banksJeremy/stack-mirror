<h1>S.O. Mirror</h1>

<ul>
  % for question in questions:
    <li>
      <a href="{{question["url"]}}">{{question["title"]}}</a>
    </li>
  % end
</ul>

%rebase page title="S.O. Mirror"
