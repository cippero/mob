$(document).ready(function(){
	const csrftoken = Cookies.get('csrftoken');
	
	$('#category').autocomplete({data: categories})

	$('.modal').modal();
	$('#entry-submit').on('click', (e) => {
		e.preventDefault();
		console.log('something is happening');
		// let modal = e.target.getAttribute("data-modal");
		let title_clean = $('#title').val().replace(/[^A-Z0-9]/ig, "");
		let data = {
			title: $('#title').val(),
			category: $('#category').val(), 
			subcategory: $('#subcategory').val(), 
			description: $('#description').val()}
		$.ajax({
			type: "POST",
			headers: {'Content-Type': 'application/x-www-form-urlencoded',
						'X-CSRFToken': csrftoken},
			url: `/entry/${title_clean}/`,
			data: $.param(data),
			// success: success,
			error: error
		})
		.done(() => {
			console.log('SUCCESS POSTING\n');
			window.history.pushState("Details", "Title", `/entry/${title_clean}/`);
			location.reload();
		});
	});

	$('#reset-search').on('click', (e) => { window.history.pushState("Details", "Title", '/'); location.reload();});

	$('#addTip').on('submit', (e) => {
		e.preventDefault();
		let entry = e.target.getAttribute("data-title");
		console.log(entry);
		// let data = {body: $('#commentBody').val()}
		$.ajax({
			type: "POST",
			headers: {'Content-Type': 'application/x-www-form-urlencoded',
						'X-CSRFToken': csrftoken},
			url: `/tip/${entry}/`,
			data: $.param({body: $('#commentBody').val()}),
			success: success,
			error: error
		});
	});

	$('.vote').on('click', (e) => {
		e.preventDefault();
		let id = e.target.getAttribute("data-id");
		let vote = e.target.getAttribute("data-vote");
		// console.log(vote);
		$.ajax({
			type: "POST",
			headers: {'Content-Type': 'application/x-www-form-urlencoded',
						'X-CSRFToken': csrftoken},
			url: `/tip/${id}/vote/`,
			data: $.param({'polarity': vote}),
			success: success,
			error: error
		});
	});

	// const select = document.getElementById("selectNumber"); 
	// const options = ["1", "2", "3", "4", "5"]; 

	// for (var i = 0; i < options.length; i++) {
	//     var opt = options[i];
	//     var el = document.createElement("option");
	//     el.text = opt;
	//     el.value = opt;
	//     select.add(el);
	// }

});

let success = function(data) {
	console.log('SUCCESS POSTING\n');
	// console.log('DATA:\n' + data);
	// setTimeout(function(){
	// 	location.reload();
	// }, 5000);
	location.reload();
}

let error = function(e) {
	console.log('FAIL POSTING\n' + e);
	// console.log('ERROR:\n' + e);
}

// // on page load...
// moveProgressBar();
// // on browser resize...
// $(window).resize(function() {
// 	moveProgressBar();
// });

// // SIGNATURE PROGRESS
// function moveProgressBar() {
// 	for (let i=0; i<$('.progress-bars-class').children().length; i++) {
// 		let color = '#'+Math.floor(Math.random()*16777215).toString(16);
// 		$('.wrap-class' + i).css({'background-color': color})
// 		let getPercent = ($('.wrap-class' + i).data('progress-percent') / 100);
// 		let getProgressWrapWidth = $('.wrap-class' + i).width();
// 		let progressTotal = getPercent * getProgressWrapWidth;
// 		let animationLength = 2500*getPercent*2;

// 		// on page load, animate percentage bar to data percentage length
// 		// .stop() used to prevent animation queueing
// 		$('.bar-class' + i).stop().animate({
// 			left: progressTotal
// 		}, animationLength);
// 	}
// }