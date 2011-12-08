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
    %include
  </body>
</html>
