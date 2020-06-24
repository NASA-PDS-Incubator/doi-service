#!/bin/python
#
#  Copyright 2020, by the California Institute of Technology.  ALL RIGHTS
#  RESERVED. United States Government Sponsorship acknowledged. Any commercial
#  use must be negotiated with the Office of Technology Transfer at the
#  California Institute of Technology.
#
# ------------------------------
import os

from pds_doi_core.util.cmd_parser import create_cmd_parser
from pds_doi_core.util.general_util import get_logger
from pds_doi_core.input.exeptions import UnknownNodeException
from pds_doi_core.actions.reserve import DOICoreActionReserve
from pds_doi_core.actions.draft import DOICoreActionDraft
from pds_doi_core.actions.list import DOICoreActionList

# Get the common logger and set the level for this file.
logger = get_logger('pds_doi_core.cmd.pds_doi_cmd')


def main():
    parser = create_cmd_parser()
    arguments = parser.parse_args()
    action_type = arguments.action
    # Moved many argument parsing to each action class.
    
    logger.info(f"run_dir {os.getcwd()}")

    try:
        if action_type == 'draft':
            draft = DOICoreActionDraft()
            o_doi_label = draft.run(draft._input_location, draft._node_id, draft._submitter_email)
            print(o_doi_label)

        elif action_type == 'list':
            list_obj = DOICoreActionList() # The token 'list' is a reserved word so we are using list_obj instead.
            # The 'list' action does not take node_id as a parameter since it is part of the query_criterias dictionary as a list.
            o_doi_list = list_obj.run(list_obj._output_format,
                                      list_obj._query_criterias)
            print(o_doi_list)

        elif action_type == 'reserve':
            reserve = DOICoreActionReserve()
            o_doi_label = reserve.run(reserve._input_location,
                                      reserve._node_id,
                                      reserve._submitter_email,
                                      submit_label_flag=True)
            # By default, submit_label_flag=True if not specified.
            # By default, write_to_file_flag=True if not specified.
            print(o_doi_label)
        else:
            logger.error(f"Action {action_type} is not supported yet.")
            exit(1)
    except UnknownNodeException as e:
        logger.error(e)
        exit(1)


if __name__ == '__main__':
    main()
