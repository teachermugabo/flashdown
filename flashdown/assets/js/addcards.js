(function() {
    var inputFront = $('#wmd-input-front'),
        inputBack = $('#wmd-input-back'),
        previewFront = $('#wmd-preview-front'),
        previewBack = $('#wmd-preview-back');

    // focus on card front when page loads
    inputFront.focus();

    // show / hide previews if user clicks checkbox
    $('#show-preview').change(function() {
        $('.wmd-preview').toggle();
    });

    $('#show-controls').change(function() {
        $('#wmd-button-bar-front').toggle();
        $('#wmd-button-bar-back').toggle();
    });

   $('#new-card-form').submit(function() {
        var data = {'deck-id': $('#deck-id-input').val(),
                     front: inputFront.val(),
                     back: inputBack.val()
                    };
        var self = this;
        $.post($(this).attr("action"), data, function() {
            // clear card data
            inputFront.val('');
            inputBack.val('');

            // clear previews
            previewFront.html('');
            previewBack.html('');

            // focus on front card textarea
            inputFront.focus();

            // resize previews
            matchPreviewHeights();

            alert("success! now add that recently added section jackass.");
            // show recently added cards to right of addcard area

        }); // TODO; handle / log errors
        return false; // prevents default submit behavior, which would
        // cause a broken pipe in our ajax app
     });


   // looks nicer if preview divs both line up
    function matchPreviewHeights() {
        return;
        previewFront.css('height', 'auto');
        previewBack.css('height', 'auto');
        var height = Math.max(previewFront.outerHeight(), previewBack.outerHeight());
        previewFront.css('height', height);
        previewBack.css('height', height);
    }

    // set the wmd input heights to the max of each's scroll height
    function matchInputHeights(el) {
        if (el.attr('id') == 'wmd-input-front') {
            var scrollHeight = getScrollHeight(inputBack.get(0));
            var maxHeight = Math.max(inputFront.outerHeight(), scrollHeight);
            inputBack.height(maxHeight);
            if (inputFront.outerHeight() < maxHeight) // guard against minHeight changes
                inputFront.height(maxHeight);
        }
        else if (el.attr('id') == 'wmd-input-back') {
            var scrollHeight = getScrollHeight(inputFront.get(0));
            var maxHeight = Math.max(inputBack.outerHeight(), scrollHeight);
            inputFront.height(maxHeight);
            if (inputBack.outerHeight() < maxHeight) // guard against minheight changes
                inputBack.height(maxHeight);
        }
    }

    // prevent size mismatch upon first use
    form_autosize(inputFront);
    form_autosize(inputBack);

    // similar to the autosize function below except it doesn't resize the element
    function getScrollHeight(el) {
         //Catch the current scroll position to stop it from jumping about in some browsers
        var this_scroll = $(window).scrollTop(),
            oldHeight = $(el).css('height'),
            height;
        //Clear any existing height settings
        $(el).css('height', '');
        //Set the textarea to scroll so that you can capture its height
        $(el).css('overflow', 'scroll');

        // get the scroll height
        height = $(el).prop('scrollHeight');
        //Set the element height back to the old height
        $(el).height(oldHeight);
        //Hide the scrollbars
        $(el).css('overflow', 'hidden');
        //Re-apply the scroll position
        $(window).scrollTop(this_scroll);

        return height + 10;
    }

    // auto expand textareas and keep them in sync
    function form_autosize(el){
        //Catch the current scroll position to stop it from jumping about in some browsers
        var this_scroll = $(window).scrollTop();
        //Clear any existing height settings
        $(el).css('height', '');
        //Set the textarea to scroll so that you can capture its height
        $(el).css('overflow', 'scroll');
        //Set the element height to the current scroll height
        $(el).height($(el).prop('scrollHeight') + 10);
        //Hide the scrollbars
        $(el).css('overflow', 'hidden');
        //Re-apply the scroll position
        $(window).scrollTop(this_scroll);

        // match heights
        matchInputHeights(el);
    }

    inputFront.on('keyup change paste', function() { form_autosize(inputFront) });
    inputBack.on('keyup change paste', function() { form_autosize(inputBack) });



    Markdown.Extra.setup({fencedCodeBlocks: {highlighter:"prettify"}});

    var converter = new Markdown.Converter(); // allow only whitelisted tags & close all tags
    converter.hooks.chain("preConversion", Markdown.Extra.tables);
    converter.hooks.chain("preConversion", Markdown.Extra.fencedCodeBlocks);

    // editor1 - front of card
    var editor = new Markdown.Editor(converter, "-front");
    editor.hooks.chain("onPreviewRefresh", function() {
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    });
    editor.hooks.chain("onPreviewRefresh", prettyPrint);
    editor.hooks.chain("onPreviewRefresh", matchPreviewHeights);
    editor.run();

    // editor2 - back of card
    var editor2 = new Markdown.Editor(converter, "-back");
    editor2.hooks.chain("onPreviewRefresh", function() {
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    });
    editor2.hooks.chain("onPreviewRefresh", prettyPrint);
    editor2.hooks.chain("onPreviewRefresh", matchPreviewHeights);
    editor2.run();

    // tab indent
    // tabIndent.renderAll();
    /* Remove this until issue #1 is closed
    tabIndent.config.tab = '    ';
    var front = document.getElementById('wmd-input-front');
    var back = document.getElementById('wmd-input-back');
    tabIndent.render(front);
    tabIndent.render(back);
    */
})();

