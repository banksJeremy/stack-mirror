<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    
    <title>{{title}}</title>
    
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
      <a href="/" class="site-name">so.wut.ca</a>
      <a href="/questions" class="active">questions</a><sub><a href="" class="active">123</a></sub>
      <a href="/answers">answers</a>
      <a href="/users">users</a>
      <a href="/comments">comments</a>
      <a href="/others">others</a>
    </div>
    <div class="wrapper">
      %include
    </div>
    <div class="footer">
      <a href="/">so.wut.ca: an unofficial Stack Overflow mirror indexing deleted questions</a> (<a href="https://github.com/jeremybanks/stack-mirror">source on GitHub</a>)
    </div>
  </body>
</html>
