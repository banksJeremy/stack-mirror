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
  </head>
  <body>
    %include
  </body>
</html>
