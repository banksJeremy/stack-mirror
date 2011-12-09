<table class="questions">
  <thead>
    <th class="score">
      Score
    </th>
    <th class="views">
      Views
    </th>
    <th class="title">
      Title
    </th>
    <th class="author">
      Author
    </th>
  <tbody>
    % alt = False
    % for question in questions:
      <tr class="{{"alt" if alt else ""}}">
        <td class="score">
          {{!kspan(question["score"])}}
        </td>
        <td class="views">
          {{!kspan(question["views"])}}
        </td>
        <td class="title">
          <a href="{{question["url"]}}">{{question["title"]}}</a>
        </td>
        <td class="creator">
          <a href="/users/{{question["creator_id"]}}">{{question["creator_name"]}}</a>
        </td>
      </tr>
      % alt = not alt
    % end
    </tbody>
  </table>
</ul>

%rebase page title="High-scoring Questions", active="questions"
