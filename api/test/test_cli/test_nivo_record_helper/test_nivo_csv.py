import io
from csv import DictReader
from datetime import datetime

import pytest
import responses
from pkg_resources import resource_stream, resource_filename
from requests import HTTPError

from nivo_api.cli.nivo_record_helper import NivoCsv, NivoDate


class TestNivoCsv:
    @responses.activate
    def test_fetch_wrong_file(self):
        responses.add(
            responses.GET, "http://example.com", content_type="text/html", status=302
        )
        date = NivoDate(False, datetime.now())
        a = NivoCsv(date, "http://example.com")
        assert a.download_url == "http://example.com"
        assert a.nivo_date == date.nivo_date
        with pytest.raises(HTTPError) as ex:
            a.fetch_and_parse()
        assert str(ex.value) == "Cannot found Nivo record"

    @responses.activate
    def test_fetch(self):
        with resource_stream(
            "test", "test_cli/test_nivo_record_helper/test_data/nivo.wrong_data.csv"
        ) as f:
            responses.add(
                responses.GET, "http://test", body=f.read(), content_type="text/plain"
            )
            date = NivoDate(False, datetime.now())
            a = NivoCsv(date, "http://test")
            assert a.download_url == "http://test"
            assert a.nivo_date == date.nivo_date

    def test_wrong_file_normalize(self):
        file = resource_filename(
            "test", "test_cli/test_nivo_record_helper/test_data/nivo.wrong_data.csv"
        )
        date = NivoDate(False, datetime.now())
        a = NivoCsv(date, "http://test")
        a.nivo_csv = DictReader(file, delimiter=";")
        with pytest.raises(KeyError) as e:
            a.normalize()

        assert str(e.value) == "'nr_numer_sta'"


class TestArchiveNicoCsv:
    def test_decompress_gzip(self):
        raise NotImplementedError()

    def test_wrong_zip(self):
        raise NotImplementedError()

    def test_wrong_data(self):
        raise NotImplementedError()

    def test_multiple_files_in_gzip(self):
        raise NotImplementedError()
