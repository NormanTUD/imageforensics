function log (...msg) {
	console.log(msg);
}

window.onload = () => {
	$('#sendbutton').click(() => {
		$("#result").html("Die Analyse kann bis zu 5 Minuten dauern. Bitte einfach warten. Der Rechner piept 1x kurz, wenn das Ergebnis da ist.");
		input = $('#imageinput')[0]
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			log("fd", formData)
			$.ajax({
				url: "analyze", // fix this to your liking
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					$("#result").html(data.responseText);
					console.log("upload error" , data);
					console.log(data);
				},
				success: function(data){
					log("success", data);
					$("#result").html(data);
				}
			});
		}
	});
};



function readUrl(input){
	if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
		}
		reader.readAsDataURL(input.files[0]);
	}

	
}

function toc () {
    var toc = "";
    var level = 0;

    document.getElementById("contents").innerHTML =
        document.getElementById("contents").innerHTML.replace(
            /<h([\d])>([^<]+)<\/h([\d])>/gi,
            function (str, openLevel, titleText, closeLevel) {
                if (openLevel != closeLevel) {
                    return str;
                }

                if (openLevel > level) {
                    toc += (new Array(openLevel - level + 1)).join("<ul>");
                } else if (openLevel < level) {
                    toc += (new Array(level - openLevel + 1)).join("</ul>");
                }

                level = parseInt(openLevel);

                var anchor = titleText.replace(/ /g, "_");
                toc += "<li><a href=\"#" + anchor + "\">" + titleText
                    + "</a></li>";

                return "<h" + openLevel + "><a name=\"" + anchor + "\">"
                    + titleText + "</a></h" + closeLevel + ">";
            }
        );

    if (level) {
        toc += (new Array(level + 1)).join("</ul>");
    }

    document.getElementById("toc").innerHTML += toc;
};

