from textwrap import dedent
from typing import Iterable, TypedDict

from html5tagger import E

from .base import BasePage


class FileInfo(TypedDict):
    icon: str
    file_name: str
    file_access: str
    file_size: str


class AutoIndex(BasePage):  # no cov
    EXTRA_STYLE = dedent(
        f"""
        #breadcrumbs a:hover {{ text-decoration: underline; }}
        #breadcrumbs .path-0 a {{ text-decoration: none; }}
        #breadcrumbs span::after {{
            content: "/"; text-decoration: none; padding: 0 0.25em;
        }}
        #breadcrumbs .path-0 a::before {{ content: "🏠"; }}
        #breadcrumbs > span > a {{ color: {BasePage.ACCENT}; }}
        main a {{ color: inherit; font-weight: bold; }}
        table.autoindex {{ width: 100%; font-family: monospace; }}
        table.autoindex tr {{ display: flex; }}
        table.autoindex tr:hover {{ background-color: #ddd; }}
        table.autoindex td {{ margin: 0 0.5rem; }}
        table.autoindex td:first-child {{ flex: 1; }}
        table.autoindex td:nth-child(2) {{ text-align: right; }}
        table.autoindex td:last-child {{  text-align: right; }}
        @media (min-width:  915px) {{
            table.autoindex {{ font-size: 1.75vw; }}
        }}
        @media (min-width:  1600px) {{
            table.autoindex {{ font-size: 1.75rem; }}
        }}
        @media (prefers-color-scheme: dark) {{
            table.autoindex tr:hover {{ background-color: #222; }}
        }}
        """
    )
    TITLE = "File Browser"

    def __init__(
        self, files: Iterable[FileInfo], url: str, debug: bool
    ) -> None:
        super().__init__(debug)
        self.files = files
        self.url = url

    def _body(self) -> None:
        with self.doc.main:
            self._headline()
            files = list(self.files)
            if files:
                self._file_table(files)
            else:
                self.doc.p("The folder is empty.")

    def _headline(self):
        """Implement a heading with the current path, combined with
        breadcrumb links"""
        with self.doc.h1(id="breadcrumbs"):
            p = self.url.split("/")[:-1]
            for i in reversed(range(len(p))):
                self.doc.span(class_=f"path-{i}").__enter__()
            for i, part in enumerate(p):
                path = "/".join(p[: i + 1]) + "/"
                self.doc.a(part, href=path)
                self.doc.__exit__(None, None, None)

    def _file_table(self, files: Iterable[FileInfo]):
        with self.doc.table(class_="autoindex container"):
            for f in files:
                self._file_row(**f)

    def _file_row(
        self,
        icon: str,
        file_name: str,
        file_access: str,
        file_size: str,
    ):
        first = E.span(icon, class_="icon").a(file_name, href=file_name)
        self.doc.tr.td(first).td(file_size).td(file_access)