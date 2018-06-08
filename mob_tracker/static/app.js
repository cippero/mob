$(document).ready(function(){
	const csrftoken = Cookies.get('csrftoken');
	$('.modal').modal();

	$('.modal-submit-class').on('click', (e) => {
		e.preventDefault();
		let modal = e.target.getAttribute("data-modal");
		let title_clean = $('#title' + modal).val().replace(/[^A-Z0-9]/ig, "");
		let data = {
			title: $('#title' + modal).val(),
			category: $('#category' + modal).val(), 
			subcategory: $('#subcategory' + modal).val(), 
			description: $('#description' + modal).val()}
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

// on page load...
moveProgressBar();
// on browser resize...
$(window).resize(function() {
	moveProgressBar();
});

// SIGNATURE PROGRESS
function moveProgressBar() {
	for (let i=0; i<$('.progress-bars-class').children().length; i++) {
		let color = '#'+Math.floor(Math.random()*16777215).toString(16);
		$('.wrap-class' + i).css({'background-color': color})
		let getPercent = ($('.wrap-class' + i).data('progress-percent') / 100);
		let getProgressWrapWidth = $('.wrap-class' + i).width();
		let progressTotal = getPercent * getProgressWrapWidth;
		let animationLength = 2500*getPercent*2;

		// on page load, animate percentage bar to data percentage length
		// .stop() used to prevent animation queueing
		$('.bar-class' + i).stop().animate({
			left: progressTotal
		}, animationLength);
	}
}