/* zrt-replace: "appUrl" tal"request/getApplicationURL" */
/* zrt-replace: "currUrl" tal"python:request.URL.get(-1) or request.getURL()" */
<script type="text/javascript">
    menu.onload = function (){
    menu.loadtree('appUrl/', 'currUrl/');
  };

  if (window.addEventListener)
      window.addEventListener("load", menu.onload, false);
  if (window.attachEvent)
      window.attachEvent("onload", menu.onload)
</script>
