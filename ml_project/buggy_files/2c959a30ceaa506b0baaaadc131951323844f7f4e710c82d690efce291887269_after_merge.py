def hlink(title: str, url: str) -> str:
    """
    Format URL (HTML)

    :param title:
    :param url:
    :return:
    """
    return html_decoration.link(value=html_decoration.quote(title), link=url)