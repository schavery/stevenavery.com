// parameters for updating the search
var insta_tag_last_id = '',
	twitter_since_id = '';

// request destination
// var host = 'https://serene-beach-1750.herokuapp.com/';
var host = 'http://localhost:4567/';

// elements that matter
var cont = document.getElementById('container'),
	body = document.getElementsByTagName('body')[0];

// objects
var xhr = new XMLHttpRequest(),
	msnry = new Masonry('#container');

// hold the things that need to go on screen
var posts = [];

// the hashtag in question, in order to highlight it
// var tag = 'blovesn';

// DEMO =======================================================================

var profile_pic = 'demo/Shawn_Tok_Profile.jpg';
var image_list = [
	'demo/11225108_10156206214660257_6461576604644332838_o.jpg',
	'demo/11855837_10204657096002909_2555570191180092233_n.jpg',
	'demo/12183903_10156206236180257_4559201901775360494_o.jpg',
	'demo/12183989_10156206215260257_5642508232909661615_o.jpg',
	'demo/12184002_10156206177230257_543923336866587688_o.jpg',
	'demo/12184278_10156206208080257_1947477508731148769_o.jpg', // t
	'demo/12186259_10156206177420257_6656367180844550927_o.jpg',
	'demo/12186487_10156206177485257_1692291264539462008_o.jpg',
	'demo/12189440_10156206204635257_4263166718562650566_o.jpg',
	'demo/12191142_10156206211760257_8586050841528731043_o.jpg',
	'demo/12191212_10156206177220257_7981885594271904947_o.jpg', // t
	'demo/12195126_10156206209495257_8947080472793950984_o.jpg',
	'demo/905924_10156206215550257_2943535293042854503_o.jpg',
	'demo/EngagementNicoleBrendan0007.jpg',
	'demo/EngagementNicoleBrendan0223.jpg',
	'demo/EngagementNicoleBrendan0236.jpg',
	'demo/gallery-1.jpg',
	'demo/registry-bg.jpg',
];

var talls = [5, 10];

var post_text = 'Super cool wedding!';
var post_index = 0;

var demo = function() {
	// if (post_index < image_list.length) {

	if (post_index != 0 || post_index % 3 == 0) {
		setTimeout(do_demo, 2000);
	} else {
		do_demo();
	}
}

var do_demo = function() {
	var div = document.createElement('div');
	div.className = 'inst';
	div.innerHTML = "<div class='user'>" +
						"<img src='/wedding-demo/" + profile_pic + "' />" +
						"<span>Tycho Brahe</span>" +
					"</div>" +
					"<div class='body'>" +
						"<img class='instapic' src='/wedding-demo/" + image_list[post_index] + "' />" +
						"<span>Super Cool Wedding! <span class='party'>#blovesn</span></span>" +
					"</div>";
				// debugger;

		if (talls.indexOf(post_index) !== -1) {
			div.className += ' tall';
		}


	post_index = (post_index + 1) % image_list.length;
	posts.push(div);
}







// TWITTER ====================================================================

// form a request for new tweets
var tweet = function() {
	if(twitter_since_id.length) {
		xhr.open("GET", host + "twee?" + twitter_since_id, true);
	} else {
		xhr.open("GET", host + "twee", true);
	}

	xhr.onreadystatechange = tweet_callback;
	xhr.send();
}

// callback function for twitter statuses
var tweet_callback = function() {
	if (xhr.readyState === 4) {
		var d = JSON.parse(xhr.response);

		if(d.statuses.length) {
			twitter_since_id = d.search_metadata.max_id_str;
			for(var i = d.statuses.length; i > 0; i--) {
				var ele = tweet_template(d.statuses[i - 1])
				posts.push(ele);
			}
		}
	} else {
		// still not ready, try again later
	}
}

// format the status data into a html element
var tweet_template = function(stat) {
	var div = document.createElement('div');
	div.className = 'tweet';

	if(stat.entities.urls.length) {	} // not doing anything with that

	div.innerHTML = "<div class='user'>" +
						"<img src='" + stat.user.profile_image_url + "' />" +
						"<span>" + stat.user.name + "</span>" +
					"</div>" +
					"<span class='body'>" + highlight(stat)	+ "</span>";
	return div;
}

// put a b around the tag mentions
var highlight = function(stat) {
	// loop through stat.entities.hashtags looking for a match on text, insert b at the indices
	var retstring = stat.text;
	for(var i = 0; i < stat.entities.hashtags.length; i++) {
		if(stat.entities.hashtags[i].text == tag) {
			
			for(var ii = 0; ii < stat.entities.hashtags[i].indices.length; ii = ii * 2) {
				if(ii == 0) {
					retstring = stat.text.substring(0, stat.entities.hashtags[i].indices[ii])
						+ '<b class="party">#' + stat.entities.hashtags[i].text + '</b>';
					ii++;
				} else {
					retstring += stat.text.substring(
									stat.entities.hashtags[i].indices[ii - 1],
									stat.entities.hashtags[i].indices[ii])
								+ '<b class="party">' + stat.entities.hashtags[i].text + '</b>';
				}
			}
		}
	}

	return retstring;
}


// INSTAGRAM ==================================================================

// form a request for instagram posts
var insta = function() {
	// if(insta_tag_last_id.length) {
	// 	xhr.open("GET", host + "insta?" + insta_tag_last_id, true);
	// } else {
		xhr.open("GET", host + "insta", true);
	// }

	xhr.onreadystatechange = insta_callback;
	xhr.send();
}

// insta callback receiver
var insta_callback = function() {
	if (xhr.readyState === 4) {
		var d = JSON.parse(xhr.response);
		var arr = [];

		if(d.data.length) {
			for(var i = d.data.length; i > 0; i--) {
				if(d.data[i - 1].id.split('_')[0] > insta_tag_last_id) {
					// we haven't seen it yet
					arr.push(d.data[i - 1]);
				}
			}

			for(var i = arr.length; i > 0; i--) {
				if(arr[i - 1].type == 'image') {
					var ele = insta_template(arr[i - 1])
					posts.push(ele);
				}
			}

			insta_tag_last_id = arr[arr.length-1].id.split('_')[0];
		}
	} else {
	// still not ready
	}
}

var insta_template = function(ip) {
	var div = document.createElement('div');
	div.className = 'inst';
	div.innerHTML = "<div class='user'>" +
						"<img src='" + ip.user.profile_picture + "' />" +
						"<span>" + ip.user.full_name + "</span>" +
					"</div>" +
					"<div class='body'>" +
						"<img class='instapic' src='" + ip.images.low_resolution.url + "' />" +
						"<span>" + insta_highlight(ip.tags) + "</span>" +
					"</div>";
	return div;
}

var insta_highlight = function(tags) {
	var retstring = '';
	for(var i = 0; i < tags.length; i++) {
		if(tags[i] == tag) {
			retstring += "<b class='party'>#" + tags[i] + "</b>";
		} else {
			retstring += "#" + tags[i]
		}
		retstring += ' ';
	}

	return retstring;
}

var render_interval;

var main = function() {
	if(document.readyState == 'complete') {
// 		tweet();

// 		var tweet_interval = window.setInterval(tweet, 30000);
// 		var insta_interval;

// 		setTimeout(function() {
// 			insta();
// 			insta_interval = window.setInterval(insta, 30000);
// 		}, 10000);


		render_interval = setInterval(render, 3000);
	}
}

// take one of the elements in the posts array and add it to the page
var render = function() {
	demo();
	if(posts.length > 0) {
			var index = Math.floor(Math.random() * posts.length);
		var ele = posts[index];
		posts.splice(index, 1);


		ele.style.height = ele.offsetHeight + 'px';

		cont.insertBefore(ele, cont.firstChild);

		msnry.prepended(ele);
		msnry.layout();
		// setTimeout(function() {
		// 	window.scrollTo(0, document.body.scrollHeight);
		// }, 200);
	}
}

msnry.on('layoutComplete', function() {
	$('.inst').css('height', 'auto');
});
document.addEventListener('readystatechange', main);
