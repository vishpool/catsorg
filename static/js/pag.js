$('.petPag > a').click(function(){
	
	var offset = 
	var address = '/svc/adoptions/' + offset + '.html';

	$.ajax({
		url: address,
		context: document.body,
		success: function(){
			$(this).addClass("done");
		}
	});	


});



