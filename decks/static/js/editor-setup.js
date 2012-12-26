function setupMarkdownEditor() {
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
    editor.run();

    // editor2 - back of card
    var editor2 = new Markdown.Editor(converter, "-back");
    editor2.hooks.chain("onPreviewRefresh", function() {
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    });
    editor2.hooks.chain("onPreviewRefresh", prettyPrint);
    editor2.run();

    // tab indent
    // tabIndent.renderAll();
    tabIndent.config.tab = '    ';
    var front = document.getElementById('wmd-input-front');
    var back = document.getElementById('wmd-input-back');
    tabIndent.render(front);
    tabIndent.render(back);
}
