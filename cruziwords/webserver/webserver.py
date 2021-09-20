import argparse
import cgi
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

from cruziwords.scoring import score_puzzle
from cruziwords.search import search_puzzle
from cruziwords.view.html import render_puzzle
from cruziwords.words import WordsCorpus

LOGGER = logging.getLogger(__file__)


class CruziwordsHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        with open("cruziwords/webserver/index.html", "r", encoding="utf-8") as f:
            output = f.read()
        self.wfile.write(output.encode())

    def parse_csv_from_post_request(self) -> str:
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
        if ctype != "multipart/form-data":
            raise ValueError("Unexpected Content-Type")

        pdict_bytes = {key: bytes(value, "utf-8") for key, value in pdict.items()}
        multipart_data = cgi.parse_multipart(self.rfile, pdict_bytes)
        form_file: bytes = multipart_data.get("file")[0]  # type: ignore
        return form_file.decode("utf-8")

    def do_POST(self) -> None:
        if self.path.endswith("/cruziwords"):
            csv_string = self.parse_csv_from_post_request()

            words = WordsCorpus.from_csv_string(csv_string)
            winning_puzzle = search_puzzle(words, score_puzzle)
            html_out = render_puzzle(winning_puzzle)

            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_out.encode())


def parse_args() -> argparse.Namespace:
    argp = argparse.ArgumentParser("Cruziwords webserver!")
    argp.add_argument("port", nargs="?", type=int, default=8000, help="Port number where the server should run")
    return argp.parse_args()


def start_server() -> None:
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")

    args = parse_args()
    port = args.port
    server = HTTPServer(("", port), CruziwordsHandler)
    LOGGER.info("Server starting on port %d", port)
    server.serve_forever()


if __name__ == "__main__":
    start_server()
