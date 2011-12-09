<div class="question post" id="12830">
  <h1>{{question["title"]}}</h1>

  <div class="score">
    {{!kspan(question["score"])}}
    <span class="unit">votes</span>
    <br>
    {{!kspan(question["views"])}}
    <span class="unit">views</span>
  </div>
  
  <div class="col">
    <div class="body">
      {{!question["body"]}}
    </div>
    
    <div class="attribution">
      asked by <a href="http://stackoverflow.com/users/1318/jacobko">some other user<img src="http://www.gravatar.com/avatar/ffefefe?d=http://so.wut.ca/static/so-icon.png&amp;s=32" width="32" heigth="32" /></a>  <br>
      on August 15th, 2008<br>
      at 22:17 UTC
    </div>
    
    <div class="attribution">
      edited by <a href="http://stackoverflow.com/users/1318/jacobko">some other user<img src="http://www.gravatar.com/avatar/ffefefe?d=http://so.wut.ca/static/so-icon.png&amp;s=32" width="32" heigth="32" /></a>  <br>
      on August 15th, 2008<br>
      at 22:17 UTC<br>
    </div>
    
    <p class="implied-by-style">
      Tags:
    </p>
    
    <ul class="tags">
      % for tag in question["tags"]:
        <li><a href="/tags/{{tag}}">{{tag}}</a></li></li>
      % end
    </ul>
    
    <div class="controls">
      <a href="/q/{{question["post_id"]}}">link</a> |
      <a href="http://stackoverflow.com/q/{{question["post_id"]}}">original</a> |
      <a href="#">show 5 comments</a> |
      <a href="#">revisions</a>
    </div>
  </div>
  
  <div style="clear: both;"></div>
</div>

<h2 class="answers">
  38 Answers
</h2>

% for answer in answers:
  <div class="answer post" id="{{answer["post_id"]}}">
    <div class="score">
      {{!kspan(answer["score"])}}
      <span class="unit">votes</span>
    
      <span class="annotation">accepted</span>
    </div>
  
    <div class="col">
      <div class="body">
        {{!answer["body"]}}
      </div>
    
    
      <div class="attribution">
        answered by <a href="http://stackoverflow.com/users/1318/jacobko">some other user<img src="http://www.gravatar.com/avatar/ffefefe?d=http://so.wut.ca/static/so-icon.png&amp;s=32" width="32" heigth="32" /></a> (search)  <br>
        on August 15, 2008<br>
        at 22:22 UTC<br>
      </div>
      
      <div class="controls">
        <a href="/a/{{answer["post_id"]}}">link</a> |
        <a href="http://stackoverflow.com/a/{{answer["post_id"]}}">original</a>
      </div>
    
    </div>
  
    <div style="clear: both;"></div>
  </div>
% end

%rebase page title=question["title"], canonical=canonical, active="questions", active_id=question["post_id"]
