$(document).ready(function()
{
	$.fn.getValues = function()
	{
		return {
			"session_id": "889d64e0-93fc-4db3-9b18-81919bb5bd1d",
			"user_ip": "89.36.68.198",
			"user_userAgent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
			"user_deviceOrientation": "PT",
			"user_innerHeight": 250,
			"user_innerWidth": 150,
			"user_innerHTML": true,
			"user_touchEvent": true,
			"user_buttonTouch": 3,
			"user_keyDown": 10,
			"user_mouseDown": 8,
			"user_accelleration": 0.6,
			"user_locale": "en_GB",
			"user_timeZone": "CET",
			"user_selenium":
			{
				"user_cdc": false,
				"user_wdc": false,
				"user_seleniumKW": false
			},
			"user_product": " ",
			"user_hashVal":"3cbcbe16c003ccf41c8bad1849ef88f3c582bbf0ad96a851d04f07bb17d2b659"
		};
	};

	var values = $.fn.getValues();

	console.log(values);

	if (document.cookie.indexOf("BDetect=") >= 0) {
	  	// They've been here before.

		$.ajax(
		{
			url: "/storefront/api/isValid/",
			type: "GET",
			dataType: "json",
			success: function(resultData)
			{
				console.log(resultData)

				if (resultData.success == false)
				{
					$.ajax(
					{
						type: 'POST',
						url: "/api/setCookie/",
						data: values,
						dataType: "text",

					}).fail(function(data)
					{
						console.log(data)
					});
				}


			}
		});
	}
	else 
	{
		$.ajax(
		{
			type: 'POST',
			url: "/storefront/api/setCookie/",
			data: values,
			dataType: "text",

		}).fail(function(data)
		{
			console.log(data)
		})
	}


});
