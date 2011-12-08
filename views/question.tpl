  <div class="wrapper">
    <div class="question post" id="12830">
      <h1>{{question["title"]}}</h1>
    
      <div class="score">
        <span class="value">{{question["score"]}}</span>
        <span class="unit">votes</span>
        <br>
        <span class="value">{{question["views"]}}</span>
        <span class="unit">views</span>
      </div>
      
      <div class="col">
        <div class="body">
          {{question["body"]}}
        </div>
        
        <div class="attribution">
          asked by <a href="http://stackoverflow.com/users/224/vzczc">Some User<img src="http://www.gravatar.com/avatar/1887903198095d29f1bb9624898e9bc5?s=32" /></a>  <br>
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
          <li><a href="/tags/language-agnostic">language-agnostic</a></li>
          <li><a href="/tags/fun">fun</a></li></li>
          <li><a href="/tags/fun">fun</a></li></li>
          <li><a href="/tags/fun">fun</a></li></li>
          <li><a href="/tags/fun">fun</a></li></li>
        </ul>
      </div>
      
      <div style="clear: both;"></div>
    </div>
    
    <div class="source-header">
      This was <a href="#">originally posted</a> on <a href="http://stackoverflow.com/">Stack Overflow</a>, but it has been deleted.
    </div>
    
    <h2 class="answers">
      38 Answers
    </h2>
    
    % for answer in answers:
      <div class="answer post" id="12833">
        <div class="score">
          <span class="value">{{answer["score"]}}</span>
          <span class="unit">votes</span>
        
          <span class="annotation">accepted</span>
        </div>
      
        <div class="col">
          <div class="body">
            {{answer["body"]}}
          </div>
        
        
          <div class="attribution">
            answered by <a href="http://stackoverflow.com/users/1318/jacobko">jacobko<img src="http://www.gravatar.com/avatar/86ed1705aaba3586de55f6a7690aabae?s=32" /></a>  <br>
            on August 15, 2008<br>
            at 22:22 UTC<br>
          </div>
        
        </div>
      
        <div style="clear: both;"></div>
      </div>
    % end
  </div>  
    
  <div class="footer">
    <a href="/">so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions</a> (<a href="https://github.com/jeremybanks/stack-mirror">source on GitHub</a>)
  </div>
  
%rebase page title=question["title"] + " - so.wut.ca mirror", canonical=canonical
