console.log('app.js is running...');
// $( document ).ready(function() {
// 	console.log($('.progress-bars-class').children().length)


// });


// on page load...
moveProgressBar();
// on browser resize...
$(window).resize(function() {
	moveProgressBar();
});

// console.log($('.progress-wrap'))[0]
// moveProgressBar(i)
// console.log(i);


// SIGNATURE PROGRESS
function moveProgressBar() {
	// console.log("moveProgressBar");
	for (let i=0; i<$('.progress-bars-class').children().length; i++) {
		let color = '#'+Math.floor(Math.random()*16777215).toString(16);
		$('.wrap-class' + i).css({'background-color': color})
		let getPercent = ($('.wrap-class' + i).data('progress-percent') / 100);
		let getProgressWrapWidth = $('.wrap-class' + i).width();
		let progressTotal = getPercent * getProgressWrapWidth;
		let animationLength = 2500 * getPercent*2;

		// on page load, animate percentage bar to data percentage length
		// .stop() used to prevent animation queueing
		$('.bar-class' + i).stop().animate({
			left: progressTotal
		}, animationLength);
	}
}