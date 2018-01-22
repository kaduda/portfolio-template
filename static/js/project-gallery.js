
document.getElementById('img-gallery').onclick = function (event) {
    event = event || window.event;
    event.preventDefault();
    var target = event.target || event.srcElement,
        link = target.src ? target.parentNode : target,
        options = {
            index: link,
            event: event,
            preloadRange: 0
        },
        links = this.getElementsByTagName('a');

    var list = to_blueimp_array(links);
    blueimp.Gallery(list, options);
};


function to_blueimp_array(html_collection) {
    var list = [];
    for (var i = 0; i < html_collection.length; i++) {
        var link = html_collection[i];
        list.push({
            title: link.title,
            href: link.href,
            type: 'image/jpeg',
            thumbnail: link.getElementsByTagName('img')[0].src
        });
    };
    return list;
}