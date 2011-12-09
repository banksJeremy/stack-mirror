<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    
    <title>{{title}} - SO.wut</title>
    
    <link rel="stylesheet" media="all" href="/static/style.css" />
    
    % if get("canonical") is not None:
      <link rel="canonical" href="{{canonical}}" />
    % end
    
    % if get("robots") is not None:
      <meta name="robots" content="{{robots}}" />
    % end
    
    <script type="text/javascript">
      var _gaq = _gaq || [];
      _gaq.push(['_setAccount', 'UA-27568016-1']);
      _gaq.push(['_setDomainName', 'wut.ca']);
      _gaq.push(['_trackPageview']);
      
      (function() {
        var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
        ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
      })();
    </script>
  </head>
  <body>
    <div class="navbar">
      <a href="/" class="site-name">SO.wut</a>
      % active = get("active")
      % active_id = get("active_id")
      % for category in ["questions", "answers", "users", "comments", "others"]:
        % if category == active:
          <a href="/{{category}}" class="active">{{category}}</a>
          % if active_id is not None:
            <sub><a href="" class="active">{{active_id}}</a></sub>
          % end
        % else:
          <a href="/{{category}}">{{category}}</a>
        % end
      % end
    </div>
    <div class="wrapper">
      %include
    </div>
    <div class="footer">
      <a href="/">SO.wut</a> is an unofficial mirror of <a href="http://stackoverflow.com/">Stack Overflow</a> including much deleted content. The source is <a href="https://github.com/jeremybanks/stack-mirror">available on GitHub</a>.<br />
      Posts are owned by their authors and used the terms of <a href="http://creativecommons.org/licenses/by-sa/2.5/">the CC BY-SA 2.5 license</a> and <a href="http://blog.stackoverflow.com/2009/06/attribution-required/">the Stack Exchange attribution policy</a>.
    </div>
  </body>
</html>
