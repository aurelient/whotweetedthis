/*
 * jQuery Twitter Flying Bird
 *
 * Copyright (c) 2010 VivekV.com
 * http://www.vivekv.com
 * http://blog.vivekv.com
 * Email: vivekv@vivekv.com
 *
 *
 *
 * Usage *
 **********
 *
 *
<script type="text/javascript"> 
var twitter_username = "enter_your_twitter_username" ; 
</script>
<script src="jquery.twitterbird.js"></script>
*
*
* Place the above code on anywhere in your website
 
*/




$(function(){

$('body').prepend( '<div id="twitterbird"></div>' );
$("#twitterbird").css({"display" : "block","height" : "64px" , "left" : 0, "width" : "64px", "position" : "absolute" , "z-index" : 10001,"cursor": "pointer" });
$("#twitterbird").click(function(){
	window.location = "http://twitter.com/" + twitter_username;
	});
	
	
$("#twitterbird").hover(
  function () {
   window.clearInterval(t);
   $("#twitterbird").css("background",'url("../img/twitter.png") no-repeat scroll 0 0 transparent');
  },
  function () {
	fly();

  }
);

	
});
var round = left = 1 ;

function fly(){
t= setInterval(function() {
	FlyBird(round);
	round++ ;
	if(round == 5 )
	round = 2 ;
}, 100);
}
fly();
function FlyBird(round)	
{
	if(round == 1) 
	{
		startpx = 0 ;
		stoppx = '-145px' ;
	}
	
	if(round == 2) 
	{
		startpx = '-65px' ;
		stoppx = '-130px' ;
	}
	
	if(round == 3) 
	{
		startpx = '-130px' ;
		stoppx = '-130px' ;
	}
	
	if(round == 4) 
	{
		startpx = '-195px' ;
		stoppx = '-130px' ;
	}

$("#twitterbird").css("background",'url("twitter.png") no-repeat scroll ' + startpx + ' ' + stoppx + ' transparent').css("left", left).css("top",top);
if( left > (window.innerWidth - 70))
{	top = Math.ceil((window.innerHeight- 100 )*Math.random())
	left = 0 ; 
}
else
left = left + 10 ;
}

	
		