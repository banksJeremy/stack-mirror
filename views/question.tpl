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
      <a href="">asked</a> by <a href="http://stackoverflow.com/users/224/vzczc">Some User<img src="http://www.gravatar.com/avatar/1887903198095d29f1bb9624898e9bc5?s=32" /></a>  <br>
      on August 15th, 2008<br>
      at 22:17 UTC
    </div>
    
    <div class="attribution">
      edited by <a href="http://stackoverflow.com/users/224/vzczc">Some User<img src="http://www.gravatar.com/avatar/1887903198095d29f1bb9624898e9bc5?s=32" /></a>  <br>
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
      <a href="http://stackoverflow.com/q/{{question["post_id"]}}">original</a>
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
        <a href="#{{answer["post_id"]}}">answered</a> by <a href="http://stackoverflow.com/users/1318/jacobko">jacobko<img src="http://www.gravatar.com/avatar/86ed1705aaba3586de55f6a7690aabae?s=32" /></a>  <br>
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

%rebase page title=question["title"] + " - so.wut.ca mirror", canonical=canonical
