import re
import fire


def convert(input_filename, output_filename="index.html"):

    HTML = f"""---
layout: tutorial
---
<h1>{input_filename}</h1>
"""

    with open(input_filename) as f:
        full_text = f.read()

    comment_regex = r"[ ]*(#.*)\n"

    parts = re.split(comment_regex, full_text)

    # remove newlines, then triple quotes, then more newlines
    HTML += parts[0].strip().strip('"""').strip()

    # it's possible we have ending HTML as well
    if parts[-1].strip().startswith('"""') and \
            parts[-1].strip().endswith('"""'):
        FINAL_HTML = parts[-1].strip().strip('"""').strip()
        parts = parts[:-1]
    else:
        FINAL_HTML = ""

    parts = parts[1:]

    pre_comments = parts[::2]
    pre_codes = parts[1::2]

    comments = []
    codes = []
    to_be_continued = False

    for comment, code in zip(pre_comments, pre_codes):
        # Remove pounds
        comment = comment.strip("####").strip()
        if not to_be_continued:
            # this is a new comment
            comments.append("")

        comments[-1] += " " + comment

        if code:
            codes.append(code)
            to_be_continued = False
        else:
            to_be_continued = True

    HTML += """<div id="annotated-code">
<!-- Code Blocks -->
<div class="annotated-code__pane annotated-code__pane--code-container">
"""

    for i, code in enumerate(codes):
        code = code.rstrip("\n")
        HTML += f"""<div class="annotated-code__code-block" id="c{i}">
{{% highlight python %}}
{code}
{{% endhighlight %}}
</div>
"""

    HTML += """</div>
<!-- END Code Blocks -->

<!-- Annotations -->
<div class="annotated-code__pane annotated-code__pane--annotations-container">
    <ul id="annotated-code__annotations">
"""

    for i, comment in enumerate(comments):
        comment = comment.strip()
        HTML += f"""<li class="annotation" id="a{i}">{comment}</li>
"""

    HTML += """</ul>
</div><!-- END Annotations -->
</div><!-- END Annotated Code -->
"""

    HTML += FINAL_HTML

    with open(output_filename, 'w') as f:
        f.write(HTML)


if __name__ == "__main__":
    fire.Fire(convert)
