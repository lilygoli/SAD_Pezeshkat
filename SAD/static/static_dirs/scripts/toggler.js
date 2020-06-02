 AOS.init({
        offset: 200, //default 120
        delay: 50, //default 0
    });
    $('a[data-toggle="pill"]').on("shown.bs.tab", e => {
        AOS.refresh();
    })
