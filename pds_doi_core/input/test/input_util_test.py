import os
import logging
import unittest
from pds_doi_core.util.config_parser import DOIConfigUtil
from pds_doi_core.input.input_util import DOIInputUtil
from pds_doi_core.util.general_util import get_logger


logger = get_logger()


class MyTestCase(unittest.TestCase):
    def test_read_bundle(self):

        doi_input_util = DOIInputUtil()
        doi_config_util = DOIConfigUtil()

        # Get the default configuration from external file.  Location may have to be absolute.
        #xml_config_file = '.' + os.path.sep + 'config' + os.path.sep + 'default_config.xml'
        xml_config_file = os.path.join(os.getcwd(), 'config', 'default_config.xml')

        dict_configList = {}
        dict_fixedList = {}
        (dict_configList, dict_fixedList) = doi_config_util.GetConfigFileMetaData(xml_config_file)

        appBasePath = os.path.abspath(os.path.curdir)
        # ------------------------------
        # Set the values for the common parameters
        # ------------------------
        root_path = dict_configList.get("root_path")
        pds_uri = dict_fixedList.get("pds_uri")

        dict_fileName_matched_status = {}
        dict_siteURL = {}
        dict_ConditionData = {}
        dict_LIDVID_submitted = {}

        i_filepath = '.' + os.path.sep + 'input' + os.path.sep + 'DOI_Reserved_GEO_200318.xlsx'
        # o_num_files_created = doi_input_util.ParseSXLSFile(appBasePath,i_filepath,dict_fixedList=dict_fixedList,dict_configList=dict_configList,dict_ConditionData=dict_ConditionData);
        # print(function_name,"o_num_files_created",o_num_files_created);

        i_filepath = os.path.join(os.getcwd(), 'input','DOI_Reserved_GEO_200318.csv')
        o_num_files_created = doi_input_util.ParseCSVFile(appBasePath, i_filepath, dict_fixedList=dict_fixedList,
                                                        dict_configList=dict_configList,
                                                        dict_ConditionData=dict_ConditionData)
        logger.info(f"o_num_files_created {o_num_files_created}")


if __name__ == '__main__':
    unittest.main()