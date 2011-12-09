<div class="post {{type}}" id{{post_id}}>
  % if get("heading")
    {{!heading}}
  % end
  
  <div class="score">
    <span class="value">{{score}}</span>
    <span class="unit">votes</span>
    
    % if get("views") is not None
      <br>
      <span class="value">{{views}}</span>
      <span class="unit">views</span>
    % 
    
    % if get("accepted")
      <span class="annotation accepted">accepted</span>
    % end
    
    % if get("deleted")
      <span class="annotation deleted">deleted</span>
    % end
  </div>
  
  % if get("tags")
    <p class="implied-by-style">
      Tags:
    </p>
    
    <ul class="tags">
      % for tag in tags
        <li><a href="/tags/{tag}">{tag}</a></li>
      % end
    </ul>
  % end
  
  <div class="col">
    <div class="body">
      {{!body}}
    </div>
    
    % for attribution in get("attributions", {}).items()
        <div class="attribution {{attribution["type"]}}">
          <a href="{{permalink}}">{{attribution["type"]}}</a> by
          <a href="{{attribution["url"]}}">{{attribution["name"]}}<img src="http://www.gravatar.com/avatar/{{attribution["avatar_hash"]}}?d=identicon&amp;s=32" /></a>
          on {{date}}<br />
          at {{time}}<br />
        </div>
      </div>
    % end  
  <div style="clear: both;"></div>
</div>
