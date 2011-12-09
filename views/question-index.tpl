% from server import kspan, aurl

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
    % for row in rows:
      % print row.keys()
      <tr class="{{"alt" if alt else ""}}">
        <td class="score">
          {{!kspan(row["question.Score"])}}
        </td>
        <td class="views">
          {{!kspan(row["question.ViewCount"])}}
        </td>
        <td class="title">
          <a href="{{aurl("questions", row["question.Id"], row["question.Title"])}}">{{row["question.Title"]}}</a>
        </td>
        <td class="creator">
          <a href="{{aurl("users", row["owner.Id"], row["owner.DisplayName"])}}">{{row["owner.DisplayName"]}}</a>
        </td>
      </tr>
      % alt = not alt
    % end
    </tbody>
  </table>
</ul>

%rebase page title="High-scoring Questions", active="questions"
