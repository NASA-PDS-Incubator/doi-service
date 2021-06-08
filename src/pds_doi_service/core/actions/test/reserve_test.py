#!/usr/bin/env python

import os
from os.path import abspath, dirname, join
import unittest
from unittest.mock import patch

import pds_doi_service.core.outputs.osti
from pds_doi_service.core.actions.reserve import DOICoreActionReserve
from pds_doi_service.core.entities.doi import DoiStatus
from pds_doi_service.core.outputs.osti import DOIOstiRecord, DOIOstiJsonWebParser
from pds_doi_service.core.outputs.doi_record import CONTENT_TYPE_XML, CONTENT_TYPE_JSON


class ReserveActionTestCase(unittest.TestCase):

    db_name = 'doi_temp.db'

    def setUp(self):
        # This setUp() function is called for every test.
        self._action = DOICoreActionReserve(db_name=self.db_name)
        self.test_dir = abspath(dirname(__file__))  # FIXME: use pkg_resources
        self.input_dir = abspath(
            join(self.test_dir, os.pardir, os.pardir, os.pardir, os.pardir, os.pardir, 'input')
        )

    def tearDown(self):
        if os.path.isfile(self.db_name):
            os.remove(self.db_name)

    def webclient_submit_patch(self, payload, url=None, username=None,
                               password=None, content_type=CONTENT_TYPE_XML):
        """
        Patch for DOIOstiWebClient.webclient_submit_existing_content().

        Allows a non dry-run reserve to occur without actually submitting
        anything to the OSTI test server.
        """
        # Parse the DOI's from the input label, update status to 'reserved',
        # and create the output label
        dois, _ = DOIOstiJsonWebParser.parse_dois_from_label(payload)

        for doi in dois:
            doi.status = DoiStatus.Reserved

        o_doi_label = DOIOstiRecord().create_doi_record(
            dois, content_type=CONTENT_TYPE_JSON
        )

        return dois, o_doi_label

    def test_reserve_xlsx_dry_run(self):
        """
        Test Reserve action with a local excel spreadsheet, using the
        dry run flag to avoid submission to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir,
                       'DOI_Reserved_GEO_200318_with_corrected_identifier.xlsx'),
            node='img', submitter='my_user@my_node.gov',
            dry_run=True, force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 3)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved_not_submitted
                             for doi in dois]))

    @patch.object(
        pds_doi_service.core.outputs.osti.DOIOstiWebClient,
        'submit_content', webclient_submit_patch)
    def test_reserve_xlsx_and_submit(self):
        """
        Test Reserve action with a local excel spreadsheet, submitting the
        result to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir,
                       'DOI_Reserved_GEO_200318_with_corrected_identifier.xlsx'),
            node='img', submitter='my_user@my_node.gov',
            dry_run=False, force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 3)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved
                             for doi in dois]))

    def test_reserve_csv_dry_run(self):
        """
        Test Reserve action with a local CSV file, using the dry run flag
        to avoid submission to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir, 'DOI_Reserved_GEO_200318.csv'),
            node='img', submitter='my_user@my_node.gov', dry_run=True,
            force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 3)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved_not_submitted
                             for doi in dois]))

    @patch.object(
        pds_doi_service.core.outputs.osti.DOIOstiWebClient,
        'submit_content', webclient_submit_patch)
    def test_reserve_csv_and_submit(self):
        """
        Test Reserve action with a local CSV file, submitting the result to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir, 'DOI_Reserved_GEO_200318.csv'),
            node='img', submitter='my_user@my_node.gov', dry_run=False,
            force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 3)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved
                             for doi in dois]))

    def test_reserve_json_dry_run(self):
        """
        Test Reserve action with a local JSON file, using the dry run flag
        to avoid submission to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir, 'DOI_Release_20210216_from_reserve.json'),
            node='img', submitter='my_user@my_node.gov', dry_run=True,
            force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 1)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved_not_submitted
                             for doi in dois]))

    @patch.object(
        pds_doi_service.core.outputs.osti.DOIOstiWebClient,
        'submit_content', webclient_submit_patch)
    def test_reserve_json_and_submit(self):
        """
        Test Reserve action with a local CSV file, submitting the result to OSTI.
        """
        o_doi_label = self._action.run(
            input=join(self.input_dir, 'DOI_Release_20210216_from_reserve.json'),
            node='img', submitter='my_user@my_node.gov', dry_run=False,
            force=True
        )

        dois, errors = DOIOstiJsonWebParser.parse_dois_from_label(o_doi_label)

        self.assertEqual(len(dois), 1)
        self.assertEqual(len(errors), 0)
        self.assertTrue(all([doi.status == DoiStatus.Reserved
                             for doi in dois]))


if __name__ == '__main__':
    unittest.main()